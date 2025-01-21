import os
import json
import asyncio
import redis
from dotenv import load_dotenv
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class DummyCollector:
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

    async def send_dummy_message(self):
        """Generate and send a dummy market data message."""
        dummy_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "market": "DUMMY-MARKET",
            "price": 100.00,
            "volume": 1000,
            "type": "test_message"
        }
        
        message = json.dumps(dummy_data)
        self.redis_client.publish(self.redis_channel, message)
        logger.info(f"Sent dummy message: {message}")

    async def start(self):
        """Start the dummy collector."""
        try:
            logger.info("Starting dummy collector...")
            while True:
                await self.send_dummy_message()
                await asyncio.sleep(5)  # Send a message every 5 seconds
                
        except Exception as e:
            logger.error(f"Error in dummy collector: {e}")
            raise
        finally:
            self.redis_client.close()

async def main():
    collector = DummyCollector()
    await collector.start()

if __name__ == "__main__":
    asyncio.run(main()) 