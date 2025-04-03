import backtrader as bt


class SmaCross(bt.Strategy):
    def log(self, txt, dt=None):
        """Logging function fot this strategy"""
        dt = dt or self.datas[0].datetime.date(0)
        print("%s, %s" % (dt.isoformat(), txt))

    def __init__(self):

        print(len(self))
        print(len(self.datas))

        self.dataclose = self.datas[0]
        self.sma1 = bt.ind.SMA(period=10)
        self.sma2 = bt.ind.SMA(period=30)

        self.long_tp = 0.05
        self.long_drawdown = 0.01

        self.short_tp = 0.05
        self.short_drawdown = 0.01

        self.long_tp_price = float("inf")
        self.long_drawdown_price = 0

        self.short_tp_price = 0
        self.short_drawdown_price = float("inf")

        self.short_max = float("inf")
        self.long_max = 0

    def next(self):
        # self.log("Close, %.2f" % self.dataclose[0])

        if len(self) == len(self.data) - 1 and self.position:
            print("Closing on the last bar")
            self.close()

        if not self.position:  # not in the market
            if self.sma1[0] > self.sma2[0] and self.sma1[-1] < self.sma2[-1]:
                self.log("LONG ORDER CREATE, %.2f" % self.dataclose[0])

                self.order = self.buy(size=10)
                self.long_tp_price = self.dataclose[0] * (1 + self.long_tp)

                self.long_max = self.dataclose[0]

                self.notify_order(self.order)

            elif self.sma1[0] < self.sma2[0] and self.sma1[-1] > self.sma2[-1]:
                self.log("SHORT ORDER CREATE, %.2f" % self.dataclose[0])

                self.order = self.sell(size=10)
                self.short_tp_price = self.dataclose[0] * (1 - self.short_tp)
                self.short_max = self.dataclose[0]

                self.notify_order(self.order)
        else:
            self.short_max = min(self.dataclose[0], self.short_max)
            self.long_max = max(self.dataclose[0], self.long_max)

            self.short_drawdown_price = self.short_max * (1 - self.short_drawdown)

            self.long_drawdown_price = self.long_max * (1 - self.long_drawdown)

            # Short Stop loss
            if self.dataclose[0] >= self.short_drawdown_price:
                self.log("STOP LOSS HIT - CLOSING POSITION, %.2f" % self.dataclose[0])
                self.close()

            # Short Take profit
            elif self.dataclose[0] <= self.short_tp_price:
                self.log("TAKE PROFIT HIT - CLOSING POSITION, %.2f" % self.dataclose[0])
                self.close()

            # Long Stop loss
            elif self.dataclose[0] <= self.long_drawdown_price:
                self.log("STOP LOSS HIT - CLOSING POSITION, %.2f" % self.dataclose[0])
                self.close()

            # Long Take profit
            elif self.dataclose[0] >= self.long_tp_price:
                self.log("TAKE PROFIT HIT - CLOSING POSITION, %.2f" % self.dataclose[0])
                self.close()

        """# Opposite Sign
        elif self.sma1[0] < self.sma2[0]:
            self.log("OPPOSITE SIGN HIT - CLOSING POSITION, %.2f" % self.dataclose[0])
            self.close()"""

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
        if order.status == order.Completed:
            print(f"Order completed: {order.executed.price}")
        elif order.status == order.Canceled:
            print("Order canceled")
        elif order.status == order.Rejected:
            print("Order rejected")

    def stop(self):
        if self.position:
            print("Closing position at end of backtest")
            self.close()
