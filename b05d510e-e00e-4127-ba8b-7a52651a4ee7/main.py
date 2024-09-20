from surmount.base_class import Strategy, TargetAllocation, backtest
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["SPY", "QQQ", "XLK", "TECL", "TQQQ", "UPRO", "XSD"]
        self.weights = [20, 20, 20, 10, 10, 10, 10]
        self.count = 0

    @property
    def interval(self):
        return "1day"

    @property
    def assets(self):
        return self.tickers

    def run(self, data):
        self.count += 1
        if (self.count % 90 == 1):
            allocation_dict = {self.tickers[i]: self.weights[i]/sum(self.weights) for i in range(len(self.tickers))}
            return TargetAllocation(allocation_dict)
        return None