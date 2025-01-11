import time
import schedule
import logging
from datetime import datetime
from collector import collect_and_push_events_objects

def main():
    logging.info("Market data collector started")
    
    # Schedule the collect_market_data function to run every 5 seconds
    schedule.every(5).seconds.do(collect_and_push_events_objects)
    

    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    try:
        main()
    except KeyboardInterrupt:
        logging.info("Market data collector stopped by user")
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}") 