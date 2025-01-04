import os
import json
import asyncio
import redis
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class MessageProcessor:
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
        self.pubsub = self.redis_client.pubsub()

    async def process_message(self, message):
        """Process incoming messages."""
        try:
            if message['type'] == 'message':
                data = json.loads(message['data'])
                logger.info(f"Processing message: {data}")
                # Add your message processing logic here
                # For example, storing in TimescaleDB, aggregating data, etc.
                
        except Exception as e:
            logger.error(f"Error processing message: {e}")

    async def start(self):
        """Start the message processor."""
        try:
            logger.info("Starting message processor...")
            self.pubsub.subscribe(self.redis_channel)
            
            while True:
                message = self.pubsub.get_message()
                if message:
                    await self.process_message(message)
                await asyncio.sleep(0.001)  # Prevent CPU overload
                
        except Exception as e:
            logger.error(f"Error in message processor: {e}")
            raise
        finally:
            self.pubsub.unsubscribe()
            self.redis_client.close()

async def main():
    processor = MessageProcessor()
    await processor.start()

if __name__ == "__main__":
    asyncio.run(main()) 