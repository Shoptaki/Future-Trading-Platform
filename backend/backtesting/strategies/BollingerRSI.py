import backtrader as bt


class BollingerRSI(bt.Strategy):
    params = (
        ("rsi_period", 14),
        ("bb_period", 20),
        ("rsi_low", 20),
        ("rsi_high", 80),
    )

    def __init__(self):
        self.rsi = bt.ind.RSI(self.data.close, period=self.p.rsi_period)
        self.bb = bt.ind.BollingerBands(self.data.close, period=self.p.bb_period)

    def next(self):
        if not self.position:
            if (
                self.data.close[0] < self.bb.lines.bot[0]
                and self.rsi[0] < self.p.rsi_low
            ):
                self.buy(size=10)
            if (
                self.data.close[0] > self.bb.lines.top[0]
                and self.rsi[0] > self.p.rsi_high
            ):
                self.sell(size=10)

        else:
            # Close Long
            if self.rsi[0] > 50 and self.position.size > 0:
                self.close()

            # Close short
            if self.rsi[0] < 50 and self.position.size < 0:
                self.close()
