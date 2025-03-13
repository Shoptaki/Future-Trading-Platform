import future_utils as future_utils
import Order as Order
from Portfolio import Portfolio

myPortfolio = Portfolio(1000)

myPortfolio.get_cash_balance()

myPortfolio.place_order(symbol="ESZ24", amount=10, limit_price=50)

print(myPortfolio.get_open_orders())
