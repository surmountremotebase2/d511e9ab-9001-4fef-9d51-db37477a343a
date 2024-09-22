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

        tqqq_ma = SMA("TQQQ", data, 30)
        current_price = data[-1]["TQQQ"]['close']
        moving_average_30 = tqqq_ma[len(tqqq_ma)-1])

        sma_10 = SMA("TQQQ", data, 10)
        moving_average_10 = sma_10[len(sma_10)-1]


        log("moving_average: " + str(tqqq_ma[len(tqqq_ma)-1]))
        log("current_price: " + str(current_price))

        if moving_average_10 > moving_average_30:
            qqq_stake = 50
            tqqq_stake = 50
        else:
            qqq_stake = 70
            tqqq_stake = 30

        return TargetAllocation({"TQQQ": tqqq_stake, "QQQ": qqq_stake})