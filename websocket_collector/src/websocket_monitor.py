import asyncio
import logging
from typing import Dict
from models.connection_status import ConnectionState, WebSocketStatus
from collector import WebsocketCollector

logger = logging.getLogger(__name__)

class WebsocketMonitor:
    def __init__(self, collector: WebsocketCollector):
        self.collector = collector

    async def display_connection_status(self) -> None:
        """Display the connection status for all of the orderbooks."""
        while True:
            statuses = self.collector.connection_statuses
            number_of_closed_connections = sum(1 for state in statuses.values() if state.status == ConnectionState.DISCONNECTED)
            number_of_failed_connections = sum(1 for state in statuses.values() if state.status == ConnectionState.FAILED)
            number_of_connecting_connections = sum(1 for state in statuses.values() if state.status == ConnectionState.CONNECTING)
            number_of_connected_connections = sum(1 for state in statuses.values() if state.status == ConnectionState.CONNECTED)

            total_number_of_recconections_attempts = sum(state.reconnect_attempts for state in statuses.values())

            logger.info("\033[H\033[J")  # Clear screen
            logger.info(f"Number of closed connections: {number_of_closed_connections}")
            logger.info(f"Number of failed connections: {number_of_failed_connections}")
            logger.info(f"Number of connecting connections: {number_of_connecting_connections}")
            logger.info(f"Number of connected connections: {number_of_connected_connections}")
            logger.info(f"Total number of reconnection attempts: {total_number_of_recconections_attempts}")
            logger.info(f"messages/s over the last minute: {len(self.collector.messages_buffer)/self.collector.buffer_duration.total_seconds()}")
            logger.info(f"Buffer size: {len(self.collector.messages_buffer)}")

            await asyncio.sleep(0.05)