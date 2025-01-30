from src.orders import Side
from dataclasses import dataclass
from datetime import datetime
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