from simulation_clock import SimulationClock
from orderbook import OrderBookSnapshot

class MarketMaker:
    def __init__(self, clock: SimulationClock):
        self.order_book_status: OrderBookSnapshot
        self.simulation_clock = clock
        self.orders = []
    
    def process_book_snapshot(self, orderbook_snapshot):
        print(f"Market Maker -- Processing orderbook snapshot, current time: {self.simulation_clock.current_time}")
