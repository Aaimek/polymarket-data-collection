# The market simulation part

## Idea
The idea behind this part is to *simulate*:
- A market
- A market maker

And make then interact, and go *though time*, by replaying historical data.

Here, going through time is done *jump by jump, from one message received to the next*. This is not realistic but it's for simplicity's sake.

## How it's done

(To get a good gasp of how it works once this is read, go see `main.py`)

### SimulationClock
A simple class that has a proprety `current_time`. It serves to tell the time to the different components.

### OrderBook
A class that has methods for:
- Receiving messages from the historical feed
- Receiving messages from the MarketMaker (tbd)
- Do all the magic to process all of those and update it's state (tbd)

### MarketMaker
A class that serves to implement a simple market maker.

What it receives is:
- An orderbook snapshot
- Status of the orders he placed (tbd)

What it outputs is:
- What to do with the order he places (tbd)
- New orders to palce (tbd)

### Historical feed
- Loads historical data, in the form of a bunch of messages as they would have came from the API
- Via the `replay` method:
    - move the clock to the time of the next message
    - send the message to the OrderBook
    - make the OrderBook and MarketMaker interract turn-by tuen

## In practice

## Notes on how it's primitive now
- Historical feeds loads data from one example csv I put in the repo