import future_utils as future_utils
import Order as Order
from Portfolio import Portfolio

myPortfolio = Portfolio(10000)

myPortfolio.get_cash_balance()

myPortfolio.place_order(symbol="ESZ24", amount=10, limit_price=200)

print("open orders: ", myPortfolio.get_open_orders())

print(myPortfolio.get_cash_balance())

myPortfolio.clear_filled_orders()
print(myPortfolio.get_positions_df())
print(len(myPortfolio.get_open_orders()))

print(myPortfolio.get_order_history())
