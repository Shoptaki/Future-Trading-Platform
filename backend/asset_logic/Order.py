import future_utils


class Order:
    """Order class which places order made from Portfolio.

    Args:
        symbol (str): Symbol for future contract
        amount (int): amount of contracts for order. Can be negative for selling/shorting.
        limit_price (float, optional): Price for limit order. Leave as None for market order. Defaults to None.
    """

    def __init__(self, symbol: str, amount: int, limit_price=None):
        self.amount = amount
        self.symbol = symbol
        self.limit_price = limit_price
        self.place_order()
        self.status = "open"

    def place_order(self):
        pass

    def get_status(self):
        pass

    def get_order_cost(self):
        """Cost of order (amount * price).

        Returns:
            cost (float)
        """
        if self.limit_price is not None:
            return self.amount * self.limit_price
        else:
            # Value for market order. Fix Later
            return None

    def get_symbol(self):
        return self.symbol

    def get_price_at_trade(self):
        return self.limit_price

    def get_order_amount(self):
        return self.amount

    def __repr__(self):

        output = f"Symbol: {self.symbol} | Amount: {self.amount} | Price: {self.limit_price} | Order Cost: {self.get_order_cost()} | Status: {self.status}"
        return output
