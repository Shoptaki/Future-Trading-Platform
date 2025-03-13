import Future
import Order


class Portfolio:

    def __init__(self, cashBalance=0):
        self.assets = {"Futures": []}
        self.margins = {"Future": 0.15}
        self.cashBalance = cashBalance

    def placeBuyOrder(self, symbol, amount, limitOrderPrice=None):

        future = Future(symbol)

        if limitOrderPrice is None:
            orderCost = future.getCurrentPrice() * self.amount
        else:
            orderCost = limitOrderPrice * self.amount

        if orderCost * self.margins["Future"] > self.cashBalance:
            raise Exception("Not enough funds for order")

        else:
            self.assets["Futures"].append(future)

        newOrder = Order(future, amount)

    def placeSellOrder(self):
        pass

    def getPortfolioValue(self):
        pass

    def withdrawCash(self, amount):
        if self.cashBalance >= amount:
            self.cashBalance -= amount
        else:
            raise Exception(f"Not enough cash to withdraw {amount}")

    def depositCash(self, amount):
        self.cashBalance += amount
