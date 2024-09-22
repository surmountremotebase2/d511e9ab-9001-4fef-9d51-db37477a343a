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

        try:
            test = self.strategy
        except:
            self.strategy = "balanced"
            log("Setting initial strategy")

        qqq_stake = 50
        tqqq_stake = 50

        tqqq_ma = SMA("TQQQ", data, 150)
        current_price = data[-1]["TQQQ"]['close']
        moving_average_30 = tqqq_ma[len(tqqq_ma)-1]

        sma_10 = SMA("TQQQ", data, 30)
        moving_average_10 = sma_10[len(sma_10)-1]

        if moving_average_10 > moving_average_30:
            if self.strategy != "balanced":
                log("Switching to balanced")
                qqq_stake = 60
                tqqq_stake = 40
                self.strategy = "balanced"
                return TargetAllocation({"TQQQ": tqqq_stake, "QQQ": qqq_stake})
        else:
            if self.strategy != "aggressive":
                log("Switching to agressive")
                qqq_stake = 80
                tqqq_stake = 20
                self.strategy = "aggressive"
                return TargetAllocation({"TQQQ": tqqq_stake, "QQQ": qqq_stake})