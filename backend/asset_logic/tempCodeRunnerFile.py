import future_utils as future_utils
import Order as Order
from Portfolio import Portfolio
import random

myPortfolio = Portfolio(1000000)

myPortfolio.place_order(symbol="ESZ24", amount=10, limit_price=200)
# print("open orders: ", myPortfolio.get_open_orders())


symbols = ["ESZ24", "NQZ24", "YMZ24", "RTYZ24", "CLZ24"]
for i in range(50):
    sym = random.choice(symbols)
    amt = random.randint(1, 50)
    price = round(random.uniform(150, 250), 2)
    myPortfolio.place_order(symbol=sym, amount=amt, limit_price=price)

myPortfolio.clear_orders()
myPortfolio.check_position_validity()

# myPortfolio.print_positions()

print(myPortfolio.get_positions_df())
# myPortfolio.check_position_validity()

myPortfolio.place_order(symbol="NQZ24", amount=-10, limit_price=150)
