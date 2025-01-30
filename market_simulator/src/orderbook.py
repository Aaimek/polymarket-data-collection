from src.orders import Order
from src.update_messages import PriceChangeMessage

class Orderbook:
    def __init__(self):
        self.orders = []

    def process_message(self, message: PriceChangeMessage):
        print(f'Orderbook processing message {message.timestamp}')
        for change in message.changes:
            print(f'Orderbook processing change {change.side} {change.price} {change.size}')
