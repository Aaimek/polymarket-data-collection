import os
import json
import asyncio
import redis
import websockets
from dotenv import load_dotenv
import logging
from datetime import datetime
from typing import Dict, Set
from websocket_client import PolymarketWebsocketClient
from models.connection_status import ConnectionState, WebSocketStatus

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

from polymarket_shared.database_conn.database_conn import DatabaseManager
from polymarket_shared.schemas.outcome import Outcome

class WebsocketCollector:
    def __init__(self):
        self.redis_host = os.getenv('REDIS_HOST', 'redis')
        self.redis_port = int(os.getenv('REDIS_PORT', 6379))
        self.redis_db = int(os.getenv('REDIS_DB', 0))
        self.redis_channel = os.getenv('REDIS_CHANNEL', 'market_data')
        
        # Initialize Redis connection
        self.redis_client = redis.Redis(
            host=self.redis_host,
            port=self.redis_port,
            db=self.redis_db,
            decode_responses=True
        )
        
        self.base_ws_url = 'wss://ws-subscriptions-clob.polymarket.com/ws/market'
        self.active_connections: Dict[str, websockets.WebSocketClientProtocol] = {}
        self.active_tasks: Dict[str, asyncio.Task] = {}
        self.current_clob_token_ids: Set[str] = set()

        # Tracking of the connection status for all of the orderbooks
        self.connection_statuses: Dict[str, WebSocketStatus] = {}

    def get_connection_status(self) -> Dict[str, ConnectionState]:
        """
        Return the connection status for all of the orderbooks.
        """
        return {clob_token_id: status for clob_token_id, status in self.connection_statuses.items()}

    async def display_connection_status(self) -> None:
        """Display the connection status for all of the orderbooks."""

        while True:
            number_of_closed_connections = sum(1 for status in self.connection_statuses.values() if status.state == ConnectionState.DISCONNECTED)
            number_of_failed_connections = sum(1 for status in self.connection_statuses.values() if status.state == ConnectionState.FAILED)
            number_of_connecting_connections = sum(1 for status in self.connection_statuses.values() if status.state == ConnectionState.CONNECTING)
            number_of_connected_connections = sum(1 for status in self.connection_statuses.values() if status.state == ConnectionState.CONNECTED)

            logger.info(f"Number of closed connections: {number_of_closed_connections}")
            logger.info(f"Number of failed connections: {number_of_failed_connections}")
            logger.info(f"Number of connecting connections: {number_of_connecting_connections}")
            logger.info(f"Number of connected connections: {number_of_connected_connections}")

            await asyncio.sleep(5)

    async def handle_websocket(self, clob_token_id: str):
        """Handle individual websocket connection and messages."""

        status = WebSocketStatus(status=ConnectionState.CONNECTING)
        self.connection_statuses[clob_token_id] = status

        try:
            logger.debug(f"Connecting to websocket for {clob_token_id}...")
            client = PolymarketWebsocketClient(clob_token_id, self.base_ws_url)
            websocket = await client.connect()
            status.state = ConnectionState.CONNECTED
            status.connected_since = datetime.now()
            self.active_connections[clob_token_id] = client
            logger.debug(f"Connected to websocket for {clob_token_id}")
            
            while True:
                message = await websocket.recv()
                # Update the connection status
                self.connection_statuses[clob_token_id].last_message_received = datetime.now()
                # Parse the message as JSON to get the list
                message_list = json.loads(message)
                # Process each message in the list
                await asyncio.gather(*[self.process_message(msg) for msg in message_list])
                
        except Exception as e:
            # Update the connection status
            status.state = ConnectionState.FAILED
            status.last_error = str(e)
            status.reconnect_attempts += 1
            logger.error(f"Error in websocket connection for {clob_token_id}: {e}")
        finally:
            if clob_token_id in self.active_connections:
                await self.active_connections[clob_token_id].close()
                self.active_connections.pop(clob_token_id, None)
            
            # Update the connection status
            status.state = ConnectionState.DISCONNECTED

    async def process_message(self, message: dict):
        """Process and publish websocket message to Redis."""

        logger.debug(f"Message data (type: {type(message)}): {message}")

        try:
            self.redis_client.publish(self.redis_channel, json.dumps(message))
        except Exception as e:
            logger.error(f"Error in websocket collector publishing message: {e}")

    async def update_connections(self):
        """Update websocket connections based on the outcomes objects inside of the database."""
        BATCH_SIZE = 10
        BATCH_DELAY = 5
        while True:
            try:
                with self.database_manager.session_scope() as session:
                    outcomes = session.query(Outcome).order_by(Outcome.name.asc()).all()
                    new_clob_token_ids = {outcome.clob_token_id for outcome in outcomes}

                # Find connections to close
                to_remove = self.current_clob_token_ids - new_clob_token_ids
                # Find new connections to open
                to_add = new_clob_token_ids - self.current_clob_token_ids

                # Close obsolete connections
                for clob_token_id in to_remove:
                    if clob_token_id in self.active_tasks:
                        self.active_tasks[clob_token_id].cancel()
                        await self.active_tasks[clob_token_id]
                        del self.active_tasks[clob_token_id]
                        # If the Outcome is no longder in the db, we remove the connection status rather than having it as disconnected
                        self.connection_statuses.pop(clob_token_id, None)
                        logger.info(f"Closed connection for {clob_token_id}")

                # Start new connections, in batches
                to_add_list = list(to_add)
                for i in range(0, len(to_add_list), BATCH_SIZE):
                    batch = to_add_list[i:i+BATCH_SIZE]
                    logger.info(f"Starting {len(batch)} new connections")
                    for clob_token_id in batch:
                        task = asyncio.create_task(self.handle_websocket(clob_token_id))
                        self.active_tasks[clob_token_id] = task
                        logger.debug(f"Started new connection for {clob_token_id}")
                    
                    if i + BATCH_SIZE < len(to_add_list):
                        logger.info(f"Waiting for {BATCH_DELAY} seconds before starting next batch")
                        await asyncio.sleep(BATCH_DELAY)

                self.current_clob_token_ids = new_clob_token_ids

            except Exception as e:
                logger.error(f"Error updating connections: {e}")

            await asyncio.sleep(0.1)  # Check for updates every minute

    async def start(self):
        """Start the websocket collector."""
        try:
            logger.info("Starting websocket collector...")
            update_task = asyncio.create_task(self.update_connections())
            display_status_task = asyncio.create_task(self.display_connection_status())
            # Keep the service running
            await asyncio.gather(update_task, display_status_task)
        except Exception as e:
            logger.error(f"Error in websocket collector: {e}")
            raise
        finally:
            # Close all active connections
            for client in self.active_connections.values():
                await client.close()
            for task in self.active_tasks.values():
                task.cancel()
            await asyncio.gather(*self.active_tasks.values(), return_exceptions=True)
            self.redis_client.close()

async def main():
    collector = WebsocketCollector()
    # Initialize database manager
    collector.database_manager = DatabaseManager()
    collector.database_manager.initialize()
    await collector.start()

if __name__ == "__main__":
    asyncio.run(main())