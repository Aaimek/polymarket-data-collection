from simulation_clock import SimulationClock
from orderbook import OrderBookSnapshot

class MarketMaker:
    """
    This class is in charge of implementing a simple market maker to test.
    See the README for more details.
    """
    def __init__(self, clock: SimulationClock):
        self.order_book_status: OrderBookSnapshot
        self.simulation_clock = clock
        self.orders = []
    
    def process_book_snapshot(self, orderbook_snapshot: OrderBookSnapshot):
        # TODO: Add in its arguments something about the status of his current orders
        # TODO: All the rest lmao
        print(f"Market Maker -- Processing orderbook snapshot, current time: {self.simulation_clock.current_time}")
