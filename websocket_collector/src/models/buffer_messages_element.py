from datetime import datetime

class BufferMessageElement:
    def __init__(self, timestamp: datetime, message: dict):
        self.timestamp = timestamp
        self.message = message
