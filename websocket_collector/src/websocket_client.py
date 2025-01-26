import asyncio
import json
import logging
import websockets
from typing import Optional
from datetime import datetime

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class PolymarketWebsocketClient:
    def __init__(self, clob_token_id: str, base_url: str):
        self.clob_token_id = clob_token_id
        self.url = base_url
        self.websocket: Optional[websockets.WebSocketClientProtocol] = None
        self.ping_task: Optional[asyncio.Task] = None
        self.last_pong_recieved = None

    async def connect(self) -> websockets.WebSocketClientProtocol:
        """Connect, ping and subscribe to the websocket."""
        # 1st, connect
        try:
            self.websocket = await websockets.connect(self.url)
        except Exception as e:
            logger.exception(f"Failed to connect to websocket for {self.clob_token_id}: {e}")
            raise

        # 2nd, initial ping
        try:
            await self.websocket.ping()
            logger.debug(f"Initial ping-pong success for {self.clob_token_id}")
        except Exception as e:
            logger.exception(f"Failed to send initial ping for {self.clob_token_id}: {e}")
            raise

        # 3rd, send subscription message
        subscription_message = {
            "assets_ids": [self.clob_token_id],
            "type": "Market",
        }

        # Send subscription message
        try:
            await self.websocket.send(json.dumps(subscription_message))
            logger.debug(f"Sent subscription message for {self.clob_token_id}")
        except Exception:
            logger.exception("Failed to send subscription message.")
        
        # Start ping task
        self.ping_task = asyncio.create_task(self._ping_loop())
        
        return self.websocket

    async def _ping_loop(self):
        """Send ping every 10 seconds to keep connection alive."""
        try:
            while True:
                if self.websocket: #and not self.websocket.closed:
                    pong_waiter = await self.websocket.ping()
                    await pong_waiter
                    self.last_pong_recieved = datetime.now()
                    logger.debug(f"Ping-pong successfull for {self.clob_token_id}")
                await asyncio.sleep(10)
        except Exception as e:
            logger.error(f"Error in ping loop for {self.clob_token_id}: {e}")

    async def close(self):
        """Close the websocket connection and cleanup."""
        if self.ping_task:
            self.ping_task.cancel()
            try:
                await self.ping_task
            except asyncio.CancelledError:
                pass

        if self.websocket:
            await self.websocket.close() 