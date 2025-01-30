from sortedcontainers import SortedDict
from enum import Enum
from uuid import uuid4
from datetime import datetime

class OrderType(Enum):
    GTC = 'GTC' # Good Till Canceled
    GTD = 'GTD' # Good Till Date
    FOK = 'FOK' # Fill or Kill

class Side(Enum):
    BUY = 'BUY'
    SELL = 'SELL'

class OrderStatus(Enum):
    """
    This is the 'order status' polymarket returns when the order is placed:

        - live:	     order placed and live
        - matched:	 order matched (marketable)
        - delayed:	 order marketable, but subject to matching delay
        - unmatched: order marketable, but failure delaying, placement not successful
    """
    LIVE = 'LIVE'
    MATCHED = 'MATCHED'
    DELAYED = 'DELAYED'
    UNMATCHED = 'UNMATCHED'

class Order:
    def __init__(self, type: OrderType, side: Side, price: float, size: float, asset_id: str, expiration: datetime =  None):
        self.order_id = uuid4()
        self.status: OrderStatus = None
        self.type: OrderType = type
        self.side: Side = side
        self.price: float = price
        self.original_size = size
        self.remaining_size = size
        self.size_matched = 0
        self.asset_id = asset_id
        self.expiration = expiration
        self.created_at = datetime.now()