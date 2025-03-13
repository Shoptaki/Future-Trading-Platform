"""future_utils.py

A collection of utility functions for working with futures contracts.
Each of the functions solely take *symbol* as an argument.

symbol (str): Symbol for specific future contract.

"""


# TODO
def get_current_price(symbol):
    pass


def get_expiration_year(symbol):
    return int(f"20{symbol[-2:]}")


def get_expiration_month(symbol):
    return convert_code(symbol[-3])


def get_asset_name(symbol):
    return convert_code(symbol[:-3])


def get_contract_name(symbol):
    asset_name = get_asset_name(symbol)
    month = get_expiration_month(symbol)
    year = get_expiration_year(symbol)

    return f"{asset_name} {month} {year}"


def convert_code(code):
    codes = {
        # Monthly Futures Symbol List
        "F": "January",
        "G": "February",
        "H": "March",
        "J": "April",
        "K": "May",
        "M": "June",
        "N": "July",
        "Q": "August",
        "U": "September",
        "V": "October",
        "X": "November",
        "Z": "December",
        # Indices
        "EMD": "E-mini Mid-Cap 400",
        "ER": "DJ Bloomberg Commodity Index",
        "ES": "E-mini S&P 500",
        "GI": "GSCI Index",
        "NK": "Nikkei 225 (CME)",
        "NQ": "E-Mini NASDAQ 100",
        "RTY": "E-mini Russell 2000",
        "VX": "Volatility Index",
        "YM": "Dow Jones (Mini)",
        # Energy Futures
        "AC": "Ethanol",
        "BZ1": "Brent Crude Oil (NYMEX)",
        "CL": "Crude Oil (NYMEX)",
        "HO": "Heating Oil",
        "NG": "Natural Gas",
        "QG": "Natural Gas (E-mini)",
        "QM": "Crude Oil (E-mini)",
        "QU": "Gasoline (RBOB-E-mini)",
        "RB": "Gasoline (RBOB)",
        # Interest Rate Futures
        "ED": "Eurodollars",
        "EM": "1-Month Libor",
        "FF": "Fed Funds (30-Day)",
        "FV": "U.S. 5-Yr Notes",
        "TU": "U.S. 2-Yr. Notes",
        "TY": "U.S. 10-Yr. Notes",
        "UL": "Ultra Bond",
        "US": "U.S. Treasury Bond",
        # Currency Futures
        "AD": "Australian Dollar",
        "BP": "British Pound",
        "BR": "Brazilian Real",
        "CD": "Canadian Dollar",
        "E7": "Euro FX (E-mini)",
        "EC": "Euro FX",
        "J7": "Japanese Yen (E-mini)",
        "JY": "Japanese Yen",
        "KRW": "Korean Won",
        "M6A": "Australian Dlr. (E-micro)",
        "M6B": "British Pound (E-micro)",
        "M6E": "Euro FX (E-micro)",
        "MCD1": "Canadian Dollar (E-micro)",
        "MIR": "E-micro INR/USD",
        "MP": "Mexican Peso",
        "MSF": "Swiss Franc (E-Micro)",
        "NE": "New Zealand Dollar",
        "RA": "South African Rand",
        "RF": "Euro FX/Swiss",
        "SEK": "Swedish Krona",
        "SF": "Swiss Franc",
        # Metal Futures
        "GC": "Gold (Comex)",
        "HG": "Copper (Comex)",
        "HRC": "HRC Steel Index",
        "MGC": "Gold (E-Micro)",
        "PA": "Palladium",
        "PL": "Platinum",
        "QC": "Copper (E-mini)",
        "QI": "Silver-Mini (Comex)",
        "QO": "Gold (mini-Comex)",
        "SI": "Silver (Comex)",
        # Housing Futures
        "BOS": "Boston Housing Idx",
        "CHI": "Chicago Housing Idx",
        "CUS": "Composite Housing Idx",
        "DEN": "Denver Housing Idx",
        "LAV": "Las Vegas Housing Idx",
        "LAX": "Los Angeles Housing Idx",
        "MIA": "Miami Housing Idx",
        "NYM": "NY Commuter Housing Idx",
        "SDG": "San Diego Housing Idx",
        "SFR": "San Francisco Housing Idx",
        "WDC": "Washington DC Housing Idx",
        # Livestock Futures
        "FC": "Feeder Cattle",
        "LC": "Live Cattle",
        "LH": "Lean Hog",
        # Grain Futures
        "BO": "Soybean Oil",
        "C": "Corn",
        "KW": "Wheat (K.C.)",
        "MW": "Wheat (Minneapolis)",
        "O": "Oats",
        "RR": "Rough Rice",
        "S": "Soybeans",
        "SM": "Soybean Meal",
        "W": "Wheat (Chicago)",
        # Mini Grain Futures
        "YC": "Corn (Mini)",
        "YK": "Soybeans (Mini)",
        "YW": "Wheat (Mini)",
        # Food & Fiber Futures
        "CB": "Butter",
        "CSC1": "Cheese",
        "DA": "Milk",
        "LB": "Lumber",
    }

    return codes.get(code, None)
