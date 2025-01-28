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

    def is_expired(self, current_time: datetime) -> bool:
        if self.type == OrderType.GTD:
            return current_time > self.expiration
        else:
            raise ValueError(f"Order type {self.type} does not have an expiration date")
        

    def fill(self, quantity):
        # Step 1: Update remaining size
        if quantity > self.remaining_size:
            raise ValueError("Fill quantity cannot be greater than remaining size")
        else:
            self.remaining_size -= quantity

        # Step 2: Update status
        if self.remaining_size == 0:
            self.status = OrderStatus.MATCHED

class Orderbook:
    def __init__(self):
        self.bids = SortedDict()
        self.asks = SortedDict()
        self.orders = SortedDict()

    def add_incoming_order(self, order):
        if order.price not in self.orders:
            self.orders[order.price] = [order]
        else:
            self.orders[order.price].append(order)
    
    def update_book(self):