from src.orders import Order
from src.update_messages import PriceChangeMessage
from src.simulation_clock import SimulationClock

class Orderbook:
    def __init__(self, simulation_clock: SimulationClock):
        self.orders = []
        self.simulation_clock = simulation_clock
        
    def process_message(self, message: PriceChangeMessage):
        print(f'Orderbook processing message from: {message.timestamp}')

        for change in message.changes:
            print(f'Orderbook processing change {change.side} {change.price} {change.size}')
