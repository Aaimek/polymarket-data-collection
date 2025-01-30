import pandas as pd
from src.simulation_clock import SimulationClock
from src.update_messages import PriceChangeMessage, PriceChange
import json
from src.orders import Side
from datetime import datetime
from src.orderbook import Orderbook
class HistoricalFeed:
    def __init__(self, simulation_clock: SimulationClock):
        self.simulation_clock = simulation_clock
        self.price_change_messages = []

    def load_messages(self):
        price_change_messages_df = pd.read_csv("../data/price_change_messages_202501302221.csv")
        
        for index, row in price_change_messages_df.iterrows():
            changes = json.loads(row['changes'])
            # timestamp = datetime.utcfromtimestamp(int(row['timestamp'])/1000)
            # print(row['timestamp'])
            timestamp = datetime.strptime(row['timestamp'], '%Y-%m-%d %H:%M:%S.%f %z')

            price_change_message = PriceChangeMessage(asset_id=row['asset_id'], timestamp=timestamp, changes=[])
            for change in changes:
                side = Side.BUY if change['side'] == 'BUY' else Side.SELL
                price_change_message.changes.append(PriceChange(side, change['price'], change['size']))
            self.price_change_messages.append(price_change_message)
    
    def replay(self, orderbook: Orderbook):
        for message in self.price_change_messages:
            self.simulation_clock.set_time(message.timestamp)
            orderbook.process_message(message)