from orders import Order
from update_messages import PriceChangeMessage
from simulation_clock import SimulationClock
from dataclasses import dataclass
from orders import OrderType, Side, OrderStatus, Order
from sortedcontainers import SortedDict
from datetime import datetime

@dataclass
class OrderBookSnapshot:
    asks: SortedDict()
    bids: SortedDict()

class Orderbook:
    def __init__(self, clock: SimulationClock):
        self.orders = []
        self.asks = SortedDict()        
        self.bids = SortedDict()
        self.clock = clock        

    def process_message(self, message: PriceChangeMessage):
        print(f"OrderBook -- Processing message, current time: {self.clock.current_time}")
        for change in message.changes:
            if change.side == Side.BUY:
                self.bids[change.price] = change.size
            else:
                self.asks[change.price] = change.size
    
    def render_snapshot(self) -> tuple:
        return OrderBookSnapshot(
                    asks=self.asks,
                    bids=self.bids,
                )
