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

        sma_long = SMA(self.letf, data, 150)
        current_price = data[-1][self.letf]['close']
        moving_average_long = sma_long[len(sma_long)-1]

        sma_short = SMA(self.letf, data, 30)
        moving_average_short = sma_short[len(sma_short)-1]

        if moving_average_short > moving_average_long:
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