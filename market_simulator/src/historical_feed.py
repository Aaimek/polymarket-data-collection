#!/usr/bin/env python

import pandas as pd
from simulation_clock import SimulationClock
from update_messages import PriceChangeMessage, PriceChange
import json
from orders import Side
from datetime import datetime
from orderbook import Orderbook
from market_maker import MarketMaker
import os

print(f"Historical feed: {os.getcwd()}")

class HistoricalFeed:
    def __init__(self, clock: SimulationClock):
        self.price_change_messages = []
        self.simulation_clock = clock 

    def load_messages(self):
        price_change_messages_df = pd.read_csv("../../data/price_change_messages_202501302221.csv")
        
        for index, row in price_change_messages_df.iterrows():
            changes = json.loads(row['changes'])
            timestamp = datetime.strptime(row['timestamp'], '%Y-%m-%d %H:%M:%S.%f %z')

            price_change_message = PriceChangeMessage(asset_id=row['asset_id'], timestamp=timestamp, changes=[])
            for change in changes:
                side = Side.BUY if change['side'] == 'BUY' else Side.SELL
                price_change_message.changes.append(PriceChange(side, change['price'], change['size']))
            self.price_change_messages.append(price_change_message)
    
    def replay(self, orderbook: Orderbook, market_maker: MarketMaker):
        for message in self.price_change_messages:
            self.simulation_clock._set_time(message.timestamp)
            orderbook.process_message(message)
            snapshot = orderbook.render_snapshot()
            market_maker.process_book_snapshot(snapshot)
