from surmount.base_class import Strategy, TargetAllocation
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Initialize memory to keep track of the previous state
        self.previous_spy_above_qqq = None

    @property
    def assets(self):
        return ["SPY", "QQQ"]

    @property
    def interval(self):
        # We use daily data to check for the crossover once a day
        return "1day"

    def run(self, data):
        # Extract closing prices for SPY and QQQ
        spy_close = data["ohlcv"][-1]["SPY"]["close"]
        qqq_close = data["ohlcv"][-1]["QQQ"]["close"]

        # Determine current state: is SPY closing price above QQQ?
        spy_above_qqq = spy_close > qqq_close

        # Initialize default allocation
        allocation = {"SPY": 0.5, "QQQ": 0.5}

        # Check if there was a crossover event since the last run
        if self.previous_spy_above_qqq is not None:  # Ensure this is not the first run
            if spy_above_qqq != self.previous_spy_above_qqq:
                # A crossover event happened
                if spy_above_qqq:
                    # SPY has crossed above QQQ, allocate 40% to SPY and 60% to QQQ
                    allocation = {"SPY": 0.4, "QQQ": 0.6}
                else:
                    # SPY has crossed below QQQ, allocate 60% to SPY and 40% to QQQ
                    allocation = {"SPY": 0.6, "QQQ": 0.4}

        # Update the previous state for the next run
        self.previous_spy_above_qqq = spy_above_qqq

        # Log the current allocation for debugging purposes
        log(f"Allocation: SPY {allocation['SPY']*100}%, QQQ {allocation['QQQ']*100}%")

        return TargetAllocation(allocation)