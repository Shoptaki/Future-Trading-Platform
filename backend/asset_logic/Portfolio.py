import future_utils
from Order import Order
from future_utils import get_current_price
import pandas as pd


class Portfolio:
    """class representing a trading portfolio that manages cash, margins, and open orders.

    Attributes:
        cash_balance (float): Available cash in the portfolio.
        margins (dict): Dictionary containing margin requirements for different asset types.
        margin_cash (float): Cash reserved for margin requirements.
        open_orders (list): List of currently open orders.
        pending_balance (float): Total pending balance for open orders.
        portfolio_value (float): Total value of the portfolio, including cash and positions.
        futures (dict): Dictionary tracking open futures positions {symbol: amount}.
        positions (pd.DataFrame): DataFrame storing current portfolio positions.

    Methods:
        place_order(symbol, amount, limit_price=None):
            Places an order for a future contract.

        get_portfolio_value():
            Returns the total portfolio value.

        update_portfolio_value():
            Updates the portfolio's total value based on current prices.

        withdraw_cash(amount):
            Withdraws cash from the portfolio.

        deposit_cash(amount):
            Deposits cash into the portfolio.

        settle_order(order):
            Settles an executed order by updating positions and cash balance.

        update_pending_balance():
            Updates the pending balance, which accounts for margin requirements of open orders.

        update_positions(order):
            Updates the portfolio's open positions based on executed orders.

    """

    def __init__(self, cash_balance: float = 0):

        self.cash_balance = cash_balance
        self.margins = {"Futures": 0.15}
        self.margin_cash = cash_balance
        self.open_orders = []

        self.pending_balance = 0
        self.portfolio_value = cash_balance
        self.order_history = []

        self.positions = pd.DataFrame(
            columns=[
                "Symbol",
                "Amount",
                "AvgCost",
                "CurrentValue",
                "ValueOnMargin",
                "P/L",
            ]
        )

    def place_order(self, symbol: str, amount: int, limit_price=None):
        """Begins order placement future contract(s).

        Args:
            symbol (str): symbol for the specific order to be placed
            amount (int): Amount of asset to be purchased. Can be negative to sell/short asset.
            limit_price (float, optional): Price for limit order.
            If None then market order is placed instead. Defaults to None.

        Raises:
            Exception: Not enough funds for order
        """
        if limit_price is None:
            order_cost = get_current_price(symbol) * amount
        else:
            order_cost = limit_price * amount

        # Buy Orders
        if amount > 0:

            # Checks if client has enough cash/margin to purchase
            if order_cost * self.margins["Futures"] > self.cash_balance:
                raise Exception("Insuffiecient Funds")

            # Placing order and updating values
            order = Order(symbol, amount, limit_price)
            self.open_orders.append(order)
            self.update_pending_balance()

        # Sell Orders (Including Shorting)
        else:
            if symbol in self.futures:
                final_amount = self.future[symbol] + amount
            else:
                final_amount = amount

            if (
                abs(final_amount * get_current_price(symbol) * self.margins["Futures"])
                > self.cash_balance
            ):
                raise Exception("Insuffiecient Funds")

            order = Order(symbol, amount, limit_price)
            self.open_orders.append(order)
            self.update_pending_balance()

    def get_portfolio_value(self):
        pass

    def update_portfolio_value(self):
        pass

    def withdraw_cash(self, amount):
        if self.cash_balance >= amount:
            self.cash_balance -= amount
        else:
            raise Exception(f"Not enough cash to withdraw {amount}")

        self.update_portfolio_value()

    def settle_order(self, order: Order):
        self.order_history.append(order)
        self.add_order_to_postions(order)

    def update_pending_balance(self):
        self.pending_balance = sum(
            [
                order.get_order_cost() * self.margins["Futures"]
                for order in self.open_orders
            ]
        )  # Sums the costs * margin of open orders

    #
    def add_order_to_postions(self, order: Order):
        """Given a cleared order to update self.positions dataframe.

        Args:
            order (Order): Cleared order to update positions.
        """
        if order.get_symbol() in self.positions["Symbol"]:
            trade = self.positions[self.positions["Symbol"] == order.get_symbol()]
            newAvgCost = (
                trade["AvgCost"] * trade["Amount"] + order.get_order_cost()
            ) / (trade["Amount"] + order.get_amount())
            trade["AvgCost"] = newAvgCost
            trade["Amount"] += order.get_amount()
            trade["CurrentValue"] = get_current_price(order.get_symbol())
            trade["ValueOnMargin"] = (
                trade["Amount"] * trade["CurrentValue"] * self.margins["Futures"]
            )
            trade["P/L"] = (
                trade["Amount"] * trade["CurrentValue"] - trade["Amount"] * newAvgCost
            )
        else:
            self.positions = self.positions.append(
                {
                    "Symbol": order.get_symbol(),
                    "Amount": order.get_amount(),
                    "AvgCost": order.get_order_cost(),
                    "CurrentValue": get_current_price(order.get_symbol()),
                    "ValueOnMargin": order.get_order_cost() * self.margins["Futures"],
                    "P/L": 0,
                },
                ignore_index=True,
            )

    def update_all_positions(self):
        """Updates the current value of all positions in the portfolio. Speicifcally updates
        the current value of the position, the value of the position on margin, and the
        profit/loss of the position.
        """
        for position in self.positions.iterrows():
            position["CurrentValue"] = get_current_price(position["Symbol"])
            position["ValueOnMargin"] = (
                position["Amount"] * position["CurrentValue"] * self.margins["Futures"]
            )
            position["P/L"] = (
                position["Amount"] * position["CurrentValue"]
                - position["Amount"] * position["AvgCost"]
            )

    def clear_filled_orders(self):
        for order in self.open_orders:
            if order.get_status() == "filled":
                self.open_orders.remove(order)
                self.settle_order(order)

    def deposit_cash(self, amount):
        self.cash_balance += amount
        self.update_portfolio_value()

    def set_margins(self, asset, margin):
        self.margins[asset] = margin

    def get_margins(self, asset):
        return self.margins[asset]

    def get_cash_balance(self):
        return self.cash_balance

    def get_open_orders(self):
        return self.open_orders

    def get_pending_balance(self):
        return self.pending_balance

    def get_order_history(self):
        return self.order_history

    def get_positions_df(self):
        return self.positions
