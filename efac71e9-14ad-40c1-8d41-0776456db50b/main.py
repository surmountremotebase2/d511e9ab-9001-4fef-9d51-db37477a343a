from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA, BB
from surmount.logging import log

class TradingStrategy(Strategy):

    @property
    def etf(self):
        return "QQQ"

    @property
    def letf(self):
        return "TQQQ"

    @property
    def assets(self):
        return [self.etf, self.letf]

    @property
    def interval(self):
        return "1day"
    
    @property
    def conservative(self):
        return "conservative"
    
    @property
    def aggressive(self):
        return "aggressive"

    def run(self, data):
        holdings = data["holdings"]
        data = data["ohlcv"]

        try:
            test = self.strategy
        except:
            self.strategy = self.conservative
            log("Setting initial strategy")

        standard_stake = 50
        leveraged_stake = 50

        tqqq_ma = SMA("TQQQ", data, 150)
        current_price = data[-1]["TQQQ"]['close']
        moving_average_30 = tqqq_ma[len(tqqq_ma)-1]

        sma_10 = SMA("TQQQ", data, 30)
        moving_average_10 = sma_10[len(sma_10)-1]

        if moving_average_10 > moving_average_30:
            if self.strategy != self.conservative:
                log("Switching to balanced")
                standard_stake = 60
                leveraged_stake = 40
                self.strategy = self.conservative
                return TargetAllocation({self.letf : leveraged_stake, self.etf : standard_stake})
        else:
            if self.strategy != self.aggressive:
                log("Switching to agressive")
                standard_stake = 80
                leveraged_stake = 20
                self.strategy = self.aggressive
                return TargetAllocation({self.letf: leveraged_stake, self.etf : standard_stake})