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

        tqqq_ma = SMA("TQQQ", data, 200)
        current_price = data[-1]["TQQQ"]['close']
        moving_average_30 = tqqq_ma[len(tqqq_ma)-1]

        sma_10 = SMA("TQQQ", data, 50)
        moving_average_10 = sma_10[len(sma_10)-1]

        if moving_average_10 > moving_average_30:
            log("ten day greater")
            qqq_stake = 50
            tqqq_stake = 50
        else:
            log("ten day lower")
            qqq_stake = 70
            tqqq_stake = 30

        return TargetAllocation({"TQQQ": tqqq_stake, "QQQ": qqq_stake})