import future_utils
from Order import Order
from future_utils import get_current_price
import pandas as pd
import numpy as np


class Portfolio:
    """Portfolio class for managing a client's portfolio of future contracts.
    This class controls how much money is available for trading, how much money is reserved for margin requirements,
    and how much money is tied up in open orders. It also keeps track of the portfolio's positions and their values.

    Attributes:
        cash_balance (float): Available cash in the portfolio.
        margins (dict): Dictionary containing margin requirements for different asset types.
        margin_cash (float): Cash reserved for margin requirements.
        open_orders (list): List of currently open orders.
        pending_balance (float): Total pending balance for open orders.
        portfolio_value (float): Total value of the portfolio, including cash and positions.
        available_cash (float): Cash available for trading.
        order_history (list): List of all executed orders.
        positions (pd.DataFrame): DataFrame storing current portfolio positions.


    Methods:
        place_order(symbol, amount, limit_price=None):
            Places an order for a future contract.

        get_portfolio_value():
            Returns the total portfolio value.

        withdraw_cash(amount):
            Withdraws cash from the portfolio.

        deposit_cash(amount):
            Deposits cash into the portfolio.

        update_pending_balance():
            Updates the pending balance, which accounts for margin requirements of open orders.

        update_all_positions(order):
            Updates the portfolio's open positions based on executed orders and current prices.

    """

    def __init__(self, cash_balance: float = 0):

        self.cash_balance = cash_balance
        self.margins = {"Futures": 0.15}
        self.margin_cash = cash_balance
        self.open_orders = []

        self.pending_balance = 0
        self.portfolio_value = cash_balance
        self.order_history = []
        self.available_cash = cash_balance

        self.positions = pd.DataFrame(
            {
                "Symbol": pd.Series(dtype="str"),
                "Amount": pd.Series(dtype="float"),
                "AvgCost": pd.Series(dtype="float"),
                "TotalCost": pd.Series(dtype="float"),
                "CurrentPrice": pd.Series(dtype="float"),
                "ValueOnMargin": pd.Series(dtype="float"),
                "TotalValue": pd.Series(dtype="float"),
                "P/L": pd.Series(dtype="float"),
            }
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

        if amount == 0:

            raise Exception("Invalid Order Amount")

        # Buy Orders
        elif amount > 0:

            # Checks if client has enough cash/margin to purchase

            if order_cost * self.margins["Futures"] > self.available_cash:
                raise Exception("Insuffiecient Funds")

            # Placing order and updating values
            order = Order(symbol, amount, limit_price)
            self.open_orders.append(order)
            self.update_pending_balance()

        # Sell Orders (Including Shorting)
        else:
            if symbol in self.positions:
                final_amount = self.positions[symbol] + amount
            else:
                final_amount = amount

            if (
                abs(final_amount * get_current_price(symbol) * self.margins["Futures"])
                > self.available_cash
            ):
                raise Exception("Insuffiecient Funds")

            order = Order(symbol, amount, limit_price)
            self.open_orders.append(order)
            self.update_pending_balance()

    def update_pending_balance(self):
        """Updates the pending balance of the portfolio."""

        self.pending_balance = sum(
            [
                order.get_limit_order_cost() * self.margins["Futures"]
                for order in self.open_orders
            ]
        )  # Sums the costs * margin of open orders

    def add_order_to_postions(self, order: Order):
        """Given a cleared order to update self.positions dataframe.
        It either updates an existing position or adds a new position to the portfolio.
        If a position size is reduced, the average cost is not updated and
        the cash balance is updated by the profit/loss of the position.

        This is the only time cash balance is updated besides deposits/withdrawls.

        Args:
            order (Order): Cleared order to update positions.
        """

        if (self.positions["Symbol"] == order.get_symbol()).any():
            # Checks if position is already in portfolio

            cur_position = self.positions[  # initializes current position
                self.positions["Symbol"] == order.get_symbol()
            ].copy()

            new_position = (
                cur_position.copy()
            )  # new position to be updated in self.positions dataframe

            # Checks if a position size is being increaced/reduced.
            if (
                order.get_amount() * cur_position["Amount"].iloc[0] < 0
            ):  # Position size is reduced

                # Currently when reducing position size, the average cost is not updated.
                # This is a simplification and can be updated in the future.
                newAvgCost = cur_position["AvgCost"]

                # Profit/Loss calculation
                # Changes cash balance by the profit/loss of the position
                # This is the only time cash_balance is updated besides deposits/withdrawls
                pnl = cur_position["Amount"].iloc[0] * (
                    cur_position["CurrentPrice"].iloc[0]
                    - cur_position["AvgCost"].iloc[0]
                )

                self.cash_balance += float(pnl)

            else:  # Position size is increased

                newAvgCost = (
                    cur_position["AvgCost"] * cur_position["Amount"]
                    + order.get_price_at_trade() * order.get_amount()
                ) / (cur_position["Amount"] + order.get_amount())
                # Calculates the new average cost of the position

            new_position["Amount"] = cur_position["Amount"] + order.get_amount()

            if new_position["Amount"].iloc[0] == 0:
                # If position size is reduced to 0, the position is removed from the portfolio
                self.positions = self.positions[
                    self.positions["Symbol"] != order.get_symbol()
                ]

            new_position["AvgCost"] = newAvgCost
            new_position["TotalCost"] = newAvgCost * (
                cur_position["Amount"] + order.get_amount()
            )

            new_position["CurrentPrice"] = order.get_price_at_trade()
            new_position["TotalValue"] = (
                new_position["Amount"] * new_position["CurrentPrice"]
            )

            new_position["ValueOnMargin"] = abs(
                cur_position["Amount"]
                * cur_position["CurrentPrice"]
                * self.margins["Futures"]
            )
            # Calculates value of the position on margin

            new_position["P/L"] = new_position["TotalCost"] - new_position["TotalValue"]
            self.positions[self.positions["Symbol"] == order.get_symbol()] = (
                new_position
            )

        else:

            # If position is not in portfolio, a new row is added to the positions dataframe
            new_row = pd.DataFrame(
                {
                    "Symbol": [order.get_symbol()],
                    "Amount": [float(order.get_amount())],
                    "AvgCost": [float(order.get_price_at_trade())],
                    "TotalCost": [
                        float(order.get_price_at_trade() * order.get_amount())
                    ],
                    "CurrentPrice": [float(order.get_price_at_trade())],
                    "ValueOnMargin": [
                        abs(
                            float(
                                order.get_price_at_trade()
                                * order.get_amount()
                                * self.margins["Futures"]
                            )
                        )
                    ],
                    "TotalValue": [
                        float(order.get_price_at_trade() * order.get_amount())
                    ],
                    "P/L": [float(0)],
                }
            )

            self.positions = pd.concat([self.positions, new_row], ignore_index=False)

    def update_all_positions(self):
        """Updates the current value of all positions in the portfolio. Speicifcally updates
        the current value of the position, the value of the position on margin, and the
        profit/loss of the position.
        """

        self.positions = self.positions.reset_index().drop("index", axis=1)
        for ind, position in self.positions.iterrows():
            # Iterates through all positions in the portfolio and updates the values one by one

            current_price = get_current_price(position["Symbol"])

            total_value = position["Amount"] * current_price
            value_on_margin = total_value * self.margins["Futures"]

            pnl = total_value - position["TotalCost"]

            self.positions.at[ind, "CurrentPrice"] = current_price
            self.positions.at[ind, "TotalValue"] = total_value
            self.positions.at[ind, "ValueOnMargin"] = abs(value_on_margin)
            self.positions.at[ind, "P/L"] = pnl

        self.update_pending_balance()
        self.update_avaliable_cash()
        self.update_portfolio_value()

    def clear_orders(self):
        """Checks if orders are filled and removes them.
        If an order is filled, it is added to the order history and the position is updated by self.add_order_to_positions() fcn.
        If an order is cancelled, it is removed from the open orders."""

        for order in self.open_orders:
            if order.get_status() == 0:
                # Open order
                continue
            elif order.get_status() == 1:
                # Filled order
                self.order_history.append(order)
                self.add_order_to_postions(order)
                self.open_orders.remove(order)

            elif order.get_status() == 2:
                # Cancelled order
                self.open_orders.remove(order)
            else:
                raise Exception("Invalid Order Status")

    def update_portfolio_value(self):
        """Updates value of the portfolio."""
        self.portfolio_value = (
            self.available_cash
            + sum(self.positions["ValueOnMargin"])
            + sum(self.positions["P/L"])
        )

    def update_avaliable_cash(self):
        """Updates availalbe cash which can be used for trading."""
        self.available_cash = (
            self.cash_balance
            - self.pending_balance
            - sum(self.positions["ValueOnMargin"])
            + sum(self.positions["P/L"])
        )

    def deposit_cash(self, amount):
        """Allows for depositing cash into account."""
        self.cash_balance += amount
        self.update_all_positions()

    def withdraw_cash(self, amount):
        """Checks if there is enough available cash to withdraw and then withdraws the cash."""
        if self.available_cash >= amount:
            self.cash_balance -= amount
            self.update_avaliable_cash()
        else:
            raise Exception(f"Not enough available cash to withdraw {amount}")

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
        self.update_all_positions()
        return self.positions

    def get_available_cash(self):
        return self.available_cash

    def get_portfolio_value(self):
        return self.portfolio_value

    def check_position_validity(self):
        """First updates the positions then checks if the positions in the portfolio are valid.
        Specifically TotalValue, TotalCost, and P/L are checked. If the values are not equal, an exception is raised.
        """
        self.update_all_positions()

        # Checks if the total value of the position is equal to the amount * current price
        for ind, pos in self.positions.iterrows():
            if not np.isclose(pos["Amount"] * pos["CurrentPrice"], pos["TotalValue"]):
                print(pos)
                raise Exception(
                    f"Position Total Value Mismatch. {pos["Amount"] * pos["CurrentPrice"]} != {pos['TotalValue']}"
                )
        print("All Position Total Values Match")

        # Checks if the total cost of the position is equal to the amount * avg cost
        for ind, pos in self.positions.iterrows():
            if not np.isclose(pos["Amount"] * pos["AvgCost"], pos["TotalCost"]):
                raise Exception(
                    f"Position Total Cost Mismatch. {pos['Amount'] * pos['AvgCost']} != {pos['TotalCost']}"
                )
        print("All Position Total Costs Match")

        # Checks if the P/L of the position is equal to the amount * avg cost - total value
        for ind, pos in self.positions.iterrows():
            if not np.isclose(
                pos["TotalValue"] - pos["TotalCost"],
                pos["P/L"],
            ):
                raise Exception(
                    f"Position P/L Mismatch. {pos["TotalValue"] - pos["TotalCost"]} != {pos['P/L']}"
                )
        print("All Position Values Match")

        def calculate_risk(self):
            # TODO
            pass
