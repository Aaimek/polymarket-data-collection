import pandas as pd
from historical_feed import HistoricalFeed
from simulation_clock import SimulationClock
from orderbook import Orderbook
from market_maker import MarketMaker
from datetime import datetime

"""
Put all of the components together and make them interact.
"""

if __name__ == "__main__":
    # Build a clock that will be shared by all components
    clock = SimulationClock(start_time=datetime.now())

    # Load the historical data
    historical_feed = HistoricalFeed(clock)
    historical_feed.load_messages()

    # Build the orderbook and the market maker
    # Make them share the clock, whose time can only be set by the HistoricalFeed
    orderbook = Orderbook(clock)
    market_maker = MarketMaker(clock)

    # Replay the historical data
    historical_feed.replay(orderbook, market_maker)