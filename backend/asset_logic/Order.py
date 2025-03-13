import backend.asset_logic.Future as Future
import Portfolio


class Order:
    def __init__(self, future: Future, amount: int, limitOrderPrice=None):
        self.amount = amount
        self.future = Future

        future = Future(symbol=self.symbol)
