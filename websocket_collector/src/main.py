from collector import WebsocketCollector
from websocket_monitor import WebsocketMonitor
from polymarket_shared.database_conn.database_conn import DatabaseManager
import asyncio
import logging

async def main():
    # Initialize the collector
    collector = WebsocketCollector()
    collector.database_manager = DatabaseManager()
    collector.database_manager.initialize()

    # Initialize the monitor
    monitor = WebsocketMonitor(collector)

    collector_task = asyncio.create_task(collector.start())
    monitor_task = asyncio.create_task(monitor.display_connection_status())

    try:
        await asyncio.gather(collector_task, monitor_task)
    except KeyboardInterrupt:
        logging.info("Websocket collector stopped by user.")
    except Exception as e:
        logging.error(f"An error occured: {str(e)}")

    await collector.start()

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO
    )

    asyncio.run(main())