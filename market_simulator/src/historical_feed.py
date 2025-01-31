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
    """
    This class is in charge of loading historical data, and replaying it for the MarketMaker and the OrderBook.
    """
    def __init__(self, clock: SimulationClock):
        self.price_change_messages = []
        self.simulation_clock = clock 

    def load_messages(self) -> None:
        """
        Loads the price change messages from a csv file.
        TODO: Make it load direcly from the database
        """
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
        """
        Replays the histirical data it has loaded.
            1. Make the clock move to the time of the next message
            2. Send the message to the OrderBook
            3. TODO: Make the MarketMaket get both
                - OrderBook snapshot
                - Status of its orders
        """
        for message in self.price_change_messages:
            self.simulation_clock._set_time(message.timestamp)
            orderbook.process_message(message)
            snapshot = orderbook.render_snapshot()
            market_maker.process_book_snapshot(snapshot)
