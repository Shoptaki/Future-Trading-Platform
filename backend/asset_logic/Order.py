import backend.asset_logic.future_utils as future_utils


class Order:
    """Order class which places order made from Portfolio.

    Args:
        symbol (str): Symbol for future contract
        amount (int): amount of contracts for order. Can be negative for selling/shorting.
        limit_price (float, optional): Price for limit order. Leave as None for market order. Defaults to None.
    """

    def __init__(self, symbol: str, amount: int, limit_price=None):
        self.amount = amount
        self.future = future_utils
        self.symbol = self.symbol
        self.limit_price = limit_price
        self.place_order()

    def place_order(self):
        pass

    def get_status(self):
        pass

    def get_order_cost(self):
        if self.limit_price is not None:
            return self.amount * self.limit_price
        else:
            # Value for market order. Fix Later
            return None
