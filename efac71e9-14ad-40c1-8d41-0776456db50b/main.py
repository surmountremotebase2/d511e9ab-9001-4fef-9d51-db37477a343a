from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA, BB
from surmount.logging import log

class TradingStrategy(Strategy):

    @property
    def assets(self):
        return ["QQQ", "SQQQ"]

    @property
    def interval(self):
        return "1hour"

    def run(self, data):
        holdings = data["holdings"]
        data = data["ohlcv"]

        sqqq_stake = 0
        tqqq_stake = 0

        tqqq_bbands = BB("TQQQ", data, 20, 1.4)
        tqqq_ma = SMA("TQQQ", data, 5)

        if len(data)<20:
            return TargetAllocation({})

        current_price = data[-1]["TQQQ"]['close']

        if tqqq_bbands is not None and current_price < tqqq_bbands['lower'][-1] and tqqq_ma[-1]>tqqq_ma[-2]:
            log("going long")
            if holdings["TQQQ"] >= 0:
                tqqq_stake = min(1, holdings["TQQQ"]+0.1)
            else:
                tqq_stake = 0.4
        elif tqqq_bbands is not None and current_price > tqqq_bbands['upper'][-1]:
            log("going short")
            if holdings["QQQ"] >= 0:
                qqq_stake = min(1, holdings["QQQ"]+0.075)
            else:
                qqq_stake = 0.2
        else:
            log("meh")
            tqqq_stake = 0
            qqq_stake = 0

        return TargetAllocation({"SQQQ": sqqq_stake, "QQQ": qqq_stake})