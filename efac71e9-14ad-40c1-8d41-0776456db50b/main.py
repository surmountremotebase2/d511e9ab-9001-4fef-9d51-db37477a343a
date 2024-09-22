from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA, BB
from surmount.logging import log

class TradingStrategy(Strategy):

    @property
    def assets(self):
        return ["QQQ", "TQQQ"]

    @property
    def interval(self):
        return "1day"

    def run(self, data):
        holdings = data["holdings"]
        data = data["ohlcv"]

        qqq_stake = 50
        tqqq_stake = 50

        tqqq_ma = SMA("TQQQ", data, 5)
        current_price = data[-1]["TQQQ"]['close']

        log("moving_average: " + str(tqqq_ma[len(tqqq_ma)-1]))
        log("current_price: " + str(current_price))

        return TargetAllocation({"TQQQ": tqqq_stake, "QQQ": qqq_stake})