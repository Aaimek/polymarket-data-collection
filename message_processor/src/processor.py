import os
import json
import asyncio
import redis
from dotenv import load_dotenv
import logging
import datetime

from polymarket_shared.database_conn.database_conn import DatabaseManager

from polymarket_shared.schemas import BookMessage, PriceChangeMessage, TickSizeChangeMessage


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

        self.db = DatabaseManager()

    async def process_message(self, message):
        """Process incoming messages."""
        try:
            if message['type'] == 'message':
                data = json.loads(message['data'])
                logger.info(f"Processing message: {data}")

                event_type = data['event_type']

                # Strip the event_type from the data in order to make it fit 1:1 to the db schema
                data.pop('event_type', None)

                # Timestmap recieved is in ms (milliseconds), but postgres expects it in s (seconds) (UNIX standard)
                try:
                    data['timestamp'] = int(data['timestamp']) / 1000
                    data['timestamp'] = datetime.datetime.fromtimestamp(data['timestamp'], datetime.UTC)
                except Exception as e:
                    logger.error(f"Error parsing timestamp: {e}")
                    return

                # Step 1: Make the message into a sqlalchemy model
                try:
                    match event_type:
                        case 'book':
                            parsed_message = BookMessage(**data)
                        case 'price_change':
                            parsed_message = PriceChangeMessage(**data)
                        case 'tick_size_change':
                            parsed_message = TickSizeChangeMessage(**data)
                        case _:
                            logger.warning(f"Unknown event type: {event_type}")
                            return
                except Exception as e:
                    logger.error(f"Error parsing message data: {e}")
                    return

                # Step 2: Push the message to the database
                with self.db.session_scope() as session:
                    session.merge(parsed_message)

                
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