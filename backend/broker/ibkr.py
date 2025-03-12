import asyncio
from ib_insync import IB, Stock

# Dummy market data for testing
DUMMY_MARKET_DATA = {
    "symbol": "AAPL",
    "price": 150.75,
    "bid": 150.50,
    "ask": 151.00,
    "volume": 1000000,
    "timestamp": "2024-02-26T12:00:00Z"
}

# Fetch Market Data (Returns Dummy Data)
async def fetch_market_data(symbol: str):
    print(f"Returning dummy market data for {symbol}")
    await asyncio.sleep(1)  # Simulate delay
    return DUMMY_MARKET_DATA
