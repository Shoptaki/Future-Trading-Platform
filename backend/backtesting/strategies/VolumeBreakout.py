import backtrader as bt


class VolumeBreakout(bt.Strategy):
    def __init__(self):
        self.high_close = bt.ind.Highest(self.data.close, period=20)
        self.avg_volume = bt.indicators.SimpleMovingAverage(self.data.volume, period=20)

        self.low_close = bt.ind.Highest(self.data.close, period=20)

        self.target = 0.05
        self.stoploss = 0.03

        self.order_brackets = []

    def next(self):
        if not self.position:
            # Entry: breakout + volume surge
            if (
                self.data.close[0] > self.high_close[-1]
                and self.data.volume[0] > 1.5 * self.avg_volume[0]
            ):
                entry_price = self.data.close[0]

                size = 10  # or however much you want

                limit_price = entry_price * (1 + self.target)
                stop_price = entry_price * (1 - self.stoploss)

                # Buys orders and appends them to self.orders list
                self.order_brackets.append(
                    self.buy_bracket(
                        size=size,
                        stopprice=stop_price,
                        limitprice=limit_price,
                    )
                )
            # Entry: breakout + volume surge
            if (
                self.data.close[0] < self.low_close[-1]
                and self.data.volume[0] > 1.5 * self.avg_volume[0]
            ):
                entry_price = self.data.close[0]

                size = 10  # or however much you want

                limit_price = entry_price * (1 + self.target)
                stop_price = entry_price * (1 - self.stoploss)

                # Buys orders and appends them to self.orders list
                self.order_brackets.append(
                    self.buy_bracket(
                        size=size,
                        stopprice=stop_price,
                        limitprice=limit_price,
                    )
                )
