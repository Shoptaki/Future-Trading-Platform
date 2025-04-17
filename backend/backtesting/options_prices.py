import requests
import pandas as pd
from errors import check_date_format


# Using polygon api to get options contracts
def get_options_contracts(
    ticker,
    as_of_date,
    limit=1000,
    lowest_strike=None,
    highest_strike=None,
    earliest_expiration=None,
    latest_expiration=None,
    contract_type=None,
    simple_output=True,
):
    """
    Get options contracts for a given ticker and as of date from the polygon api.

    Args:
        ticker (str): Ticker of the stock
        as_of_date (str): Date to get the options contracts for the ticker. Format: YYYY-MM-DD
        limit (int): Number of options contracts to return. Default is 1000.
        lowest_strike (int):  Lowest strike price to filter the options contracts by. Default is None.
        highest_strike (int): Highest strike price to filter the options contracts by. Default is None.
        earliest_expiration (str): Earliest expiration date to filter the options contracts by. Format: YYYY-MM-DD. Default is None.
        latest_expiration (str): Latest expiration date to filter the options contracts by. Format: YYYY-MM-DD. Default is None.
        contract_type (str): Contract type to filter the options contracts by. Either "call" or "put". Default is None.
        simple_output (bool): If True, return a simple output with the contract type, strike price, expiration date, and ticker. Default is True.
    """
    if not check_date_format(as_of_date):
        raise ValueError("As of date must be in format YYYY-MM-DD")

    ticker = ticker.upper()

    API_KEY = "MHDRteHWI2drKKudOh0jDCES9SX2BkgP"

    url = "https://api.polygon.io/v3/reference/options/contracts"
    params = {
        "underlying_ticker": ticker,
        "as_of": as_of_date,
        "limit": limit,  # adjust for pagination
        "apiKey": API_KEY,
    }

    response = requests.get(url, params=params)
    response_json = response.json()

    # Convert the results to a pandas DataFrame
    df = pd.DataFrame(response_json["results"])

    # Convert the timestamp to a datetime object
    df["expiration_date"] = pd.to_datetime(df["expiration_date"])

    # Convert the as_of_date to a datetime object
    df["as_of_date"] = pd.to_datetime(as_of_date)

    # Filter by lowest strike price if specified
    if lowest_strike:
        df = df[df["strike_price"] >= lowest_strike]

    # Filter by highest strike price if specified
    if highest_strike:
        df = df[df["strike_price"] <= highest_strike]

    # Filter by earliest expiration date if specified
    if earliest_expiration:
        df = df[df["expiration_date"] >= pd.to_datetime(earliest_expiration)]

    # Filter by latest expiration date if specified
    if latest_expiration:
        df = df[df["expiration_date"] <= pd.to_datetime(latest_expiration)]

    # Simple output to get the strike price, expiration date, and contract type
    if simple_output:
        df = df[
            [
                "contract_type",
                "strike_price",
                "expiration_date",
                "as_of_date",
                "ticker",
            ]
        ]

    # Filter by contract type(call or put) if specified
    if contract_type:
        if contract_type != "call" and contract_type != "put":
            raise Warning(
                "Contract type must be either 'call' or 'put'. Returning all contracts."
            )
        else:
            df = df[df["contract_type"] == contract_type]

    return df


def get_price_data(ticker, start_date, end_date, timeframe="minute", num_timeframes=1):
    """
    Get data from the Polygon API for a given ticker, start date, end date, timeframe, and timeframes.

    Args:
        ticker (str): The ticker symbol for the futures contract (e.g. "ES1")
        start_date (str): Start date in format "YYYY-MM-DD"
        end_date (str): End date in format "YYYY-MM-DD"
        timeframe (str, optional): Time interval between data points. Defaults to "minute".
        num_timeframes (int, optional): Number of timeframe units to aggregate. Defaults to 1.

    Returns:
        pd.DataFrame: A pandas DataFrame containing the OHLCV data
    """

    # Check if the start and end date are in the correct format
    if not check_date_format(start_date):
        raise ValueError("Start date must be in format YYYY-MM-DD")
    if not check_date_format(end_date):
        raise ValueError("End date must be in format YYYY-MM-DD")

    API_KEY = "MHDRteHWI2drKKudOh0jDCES9SX2BkgP"  # Jacobs API key

    url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/{num_timeframes}/{timeframe}/{start_date}/{end_date}?adjusted=true&apiKey={API_KEY}"

    res = requests.get(url).json()

    if "results" not in res:

        raise ValueError(
            "No data found for the given request, make sure the arguments are valid.\n\n Response: "
            + str(res)
        )

    # Convert the results to a pandas DataFrame
    df = pd.DataFrame(res["results"])

    # Convert the timestamp to a datetime object
    df["t"] = pd.to_datetime(
        df["t"], unit="ms"
    )  # 't' is the timestamp column in milliseconds
    df.rename(
        columns={
            "v": "volume",
            "vw": "vwap",
            "o": "open",
            "c": "close",
            "h": "high",
            "l": "low",
            "t": "time_UTC",
            "n": "trade_count",
        },
        inplace=True,
    )

    return df


if __name__ == "__main__":
    (get_price_data("AAPL", "2025-04-01", "2025-04-01", "minute"))
