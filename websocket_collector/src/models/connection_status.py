"""
This module contains the ConnectionStatus model.

Its goal is, for each of the Outcomes (=1 clob_toke_id = 1 orderbook), to keep track of the status of the websocket connection.
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional

class ConnectionStatus(Enum):
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    FAILED = "failed"
    CONNECTING = "connecting"

@dataclass
class ConnectionStatus:
    # clob_token_id: str
    status: ConnectionStatus
    connected_since: Optional[datetime] = None
    last_error: Optional[str] = None
    reconnect_attempts: int = 0
    last_message_received: Optional[datetime] = None


    def to_dict(self):
        return {
            # "clob_token_id": self.clob_token_id,
            "status": self.status.value,
            "connected_since": self.connected_since.isoformat() if self.connected_since else None,
            "last_error": self.last_error,
            "reconnect_attempts": self.reconnect_attempts,
            "last_message_received": self.last_message_received.isoformat() if self.last_message_received else None,
        }