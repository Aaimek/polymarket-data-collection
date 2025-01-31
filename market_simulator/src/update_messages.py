from orders import Side
from dataclasses import dataclass
from datetime import datetime

"""
Python models for the messages that are sent from the HistoricalFeed to the OrderBook and the MarketMaker.

NOTE: These models just represents the necessary part from the messages we would receive, for modeling purposes.
"""

@dataclass
class PriceChange:
    side: Side
    price: float
    size: float

@dataclass
class PriceChangeMessage:
    asset_id: str
    changes: list[PriceChange]
    timestamp: datetime