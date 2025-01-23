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

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

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

    async def handle_websocket(self, clob_token_id: str):
        """Handle individual websocket connection and messages."""
        try:
            client = PolymarketWebsocketClient(clob_token_id, self.base_ws_url)
            websocket = await client.connect()
            self.active_connections[clob_token_id] = client
            
            logger.info(f"Connected to websocket for {clob_token_id}")
            
            while True:
                message = await websocket.recv()
                # Parse the message as JSON to get the list
                message_list = json.loads(message)
                # Process each message in the list
                await asyncio.gather(*[self.process_message(msg) for msg in message_list])
                
        except Exception as e:
            logger.error(f"Error in websocket connection for {clob_token_id}: {e}")
        finally:
            if clob_token_id in self.active_connections:
                await self.active_connections[clob_token_id].close()
                self.active_connections.pop(clob_token_id, None)

    async def process_message(self, message: dict):
        """Process and publish websocket message to Redis."""

        logger.info(f"Message data (type: {type(message)}): {message}")

        try:
            self.redis_client.publish(self.redis_channel, json.dumps(message))
        except Exception as e:
            logger.error(f"Error in websocket collector publishing message: {e}")

    async def update_connections(self):
        """Update websocket connections based on the outcomes objects inside of the database."""
        while True:
            try:
                with self.database_manager.session_scope() as session:
                    outcomes = session.query(Outcome).order_by(Outcome.name.asc()).limit(100).all()
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
                        logger.info(f"Closed connection for {clob_token_id}")

                # Start new connections
                for clob_token_id in to_add:
                    task = asyncio.create_task(self.handle_websocket(clob_token_id))
                    self.active_tasks[clob_token_id] = task
                    logger.info(f"Started new connection for {clob_token_id}")

                self.current_clob_token_ids = new_clob_token_ids

            except Exception as e:
                logger.error(f"Error updating connections: {e}")

            await asyncio.sleep(0.1)  # Check for updates every minute

    async def start(self):
        """Start the websocket collector."""
        try:
            logger.info("Starting websocket collector...")
            update_task = asyncio.create_task(self.update_connections())
            # Keep the service running
            await asyncio.gather(update_task)
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