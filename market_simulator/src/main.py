import pandas as pd
from historical_feed import HistoricalFeed
from simulation_clock import SimulationClock
from orderbook import Orderbook
from market_maker import MarketMaker
from datetime import datetime


if __name__ == "__main__":
    clock = SimulationClock(start_time=datetime.now())
    historical_feed = HistoricalFeed(clock)
    historical_feed.load_messages()

    orderbook = Orderbook(clock)
    market_maker = MarketMaker(clock)

    print("Replaying historical feed...")

    historical_feed.replay(orderbook, market_maker)