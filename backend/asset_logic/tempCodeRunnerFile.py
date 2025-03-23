import future_utils as future_utils
import Order as Order
from Portfolio import Portfolio
import random

myPortfolio = Portfolio(1000000)

symbols = ["ESZ24", "NQZ24", "YMZ24", "RTYZ24", "CLZ24"]
for i in range(100):
    sym = random.choice(symbols)
    amt = random.randint(-50, 50)
    if amt == 0:
        continue
    price = round(random.uniform(50, 1000), 2)
    myPortfolio.place_order(symbol=sym, amount=amt, limit_price=price)
    myPortfolio.clear_orders()
    myPortfolio.update_all_positions()

myPortfolio.check_position_validity()
print("positions: ")
print(myPortfolio.get_positions_df())
print(f"cash balance: {myPortfolio.get_cash_balance()}")
print(f"available margin: {myPortfolio.get_available_cash()}")
