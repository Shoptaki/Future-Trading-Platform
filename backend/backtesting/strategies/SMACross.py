import backtrader as bt
import pandas as pd


class SmaCross(bt.Strategy):

    def log(self, txt, trade=False, dt=None):
        """Logging function for this strategy"""
        dt = dt or self.datas[0].datetime.date(0)
        timestamp = "%s, %s" % (dt.isoformat(), txt)
        print(timestamp)

    def __init__(self, sma1=10, sma2=30, target=0.05, stoploss=0.01):

        self.sma1 = bt.ind.SMA(period=sma1)
        self.sma2 = bt.ind.SMA(period=sma2)

        self.target = target
        self.stoploss = stoploss

        self.trades_df = pd.DataFrame()  # will be populated at the end

        self.order_brackets = []

        self.current_trade = {}

        self.dataclose = self.datas[0]

    def next(self):

        if not self.position:  # not in the market

            # Positive sma cross from time before

            if self.sma1[0] > self.sma2[0] and self.sma1[-1] < self.sma2[-1]:

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

                # self.log("LONG ORDER CREATE, %.2f" % self.dataclose[0], trade=True)

            # Negabive sma cross from time before
            elif self.sma1[0] < self.sma2[0] and self.sma1[-1] > self.sma2[-1]:
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

    """def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
        if order.status == order.Completed:
            print(f"Order completed: {order.executed.price}")
        elif order.status == order.Canceled:
            print("Order canceled")
        elif order.status == order.Rejected:
            print("Order rejected")"""
