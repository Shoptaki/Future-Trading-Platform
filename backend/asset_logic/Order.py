import future_utils
from future_utils import get_current_price


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
        self.price_at_trade = None
        self.place_order()

    def place_order(self):

        # For market orders
        if self.limit_price is None:
            self.limit_price = future_utils.get_current_price(self.symbol)

        # For buying/long orders
        else:
            if self.amount > 0:
                if get_current_price(self.symbol) <= self.limit_price:
                    self.status = "filled"
                    self.price_at_trade = get_current_price(self.symbol)
                    # TODO Place order in database and actually place order

                # For selling/short orders
                else:
                    if get_current_price(self.symbol) >= self.limit_price:
                        self.status = "filled"
                        self.price_at_trade = get_current_price(self.symbol)
                        # TODO Place order in database and actually place order

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
        return self.price_at_trade

    def get_order_amount(self):
        return self.amount

    def __repr__(self):

        output = f"Symbol: {self.symbol} | Amount: {self.amount} | Price: {self.limit_price} | Order Cost: {self.get_order_cost()} | Status: {self.status}"
        return output
