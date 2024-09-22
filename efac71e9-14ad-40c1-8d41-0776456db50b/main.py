from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA, BB
from surmount.logging import log

class TradingStrategy(Strategy):

    @property
    def etf(self):
        # Set the symbol for underlying ETF
        return "QQQ"

    @property
    def letf(self):
        # Set the symbol for the leveraged ETF
        return "TQQQ"

    @property
    def assets(self):
        return [self.etf, self.letf]

    @property
    def interval(self):
        return "1day"
    
    @property
    def conservative(self):
        # String ID for conservative mix
        return "conservative"
    
    @property
    def aggressive(self):
        # String ID for aggressive mix
        return "aggressive"

    @property
    def long_duration(self):
        # Duration in Days for Golden Cross long duration
        return 150

    @property
    def short_duration(self):
        # Duration in Days for Golden Cross short duration
        return 40

    @property
    def aggressive_mix(self):
        # Aggressive portfolio weights
        return {
            "etf": 60,
            "letf": 40
        }
    
    @property
    def conservative_mix(self):
        # Conservative portolio weights
        return {
            "etf": 100,
            "letf": 0
        }

    def run(self, data):
        holdings = data["holdings"]
        data = data["ohlcv"]

        try:
            test = self.strategy
        except:
            self.strategy = "initial"
            log("Setting initial strategy")

        # Get short duration moving average
        sma_long = SMA(self.letf, data, self.long_duration)
        current_price = data[-1][self.letf]['close']
        moving_average_long = sma_long[len(sma_long)-1]

        # Get long duration moving average
        sma_short = SMA(self.letf, data, self.short_duration)
        moving_average_short = sma_short[len(sma_short)-1]

        if moving_average_short < moving_average_long:
            # if the short term moving average falls below the long term, set strategy to conservative
            if self.strategy != self.conservative:
                log("Switching to conservative")
                standard_stake = self.conservative_mix["etf"]
                leveraged_stake = self.conservative_mix["letf"]
                self.strategy = self.conservative
                return TargetAllocation({self.letf: leveraged_stake, self.etf : standard_stake})
                
        else:
            # if the short term moving average climbs above the long term, set strategy to aggressive
            if self.strategy != self.aggressive:
                log("Switching to aggressive")
                standard_stake = self.aggressive_mix["etf"]
                leveraged_stake = self.aggressive_mix["letf"]
                self.strategy = self.aggressive
                return TargetAllocation({self.letf : leveraged_stake, self.etf : standard_stake})