import backtrader as bt


class RSIVolume(bt.Strategy):
    params = (
        ("rsi_period", 14),
        ("vol_period", 20),
        ("rsi_low", 20),
        ("rsi_high", 80),
    )

    def __init__(self):
        self.rsi = bt.ind.RSI(self.data.close, period=self.p.rsi_period)
        self.avg_volume = bt.ind.SMA(self.data.volume, period=self.p.vol_period)

    def next(self):
        if not self.position:
            # Entry Condition
            if self.rsi < self.p.rsi_low and self.data.volume[0] > self.avg_volume[0]:

                self.buy(size=10)
        else:
            # Exit Condition
            if self.rsi > self.p.rsi_high and self.data.volume[0] < self.avg_volume[0]:
                self.sell(size=10)
