import yfinance as yf
import backtrader as bt
import pandas as pd
from datetime import datetime
import os
import matplotlib.pyplot as plt
from strategies.SMACross import SmaCross
from strategies.EmaCross import EmaCross
from strategies.VolumeBreakout import VolumeBreakout
from strategies.RSIVolume import RSIVolume
from strategies.BollingerRSI import BollingerRSI


def main():
    strategies = {
        "SMACross": SmaCross,
        "EMACross": EmaCross,
        "VolumeBreakout": VolumeBreakout,
        "RSIVolume": RSIVolume,
        "BollingerRSI": BollingerRSI,
    }

    timeframes_2y = ["1d", "1h"]
    timeframes_1mo = ["5m", "15m"]

    # 2Y backtest
    profits_df = None

    for name, strategy in strategies.items():
        for tf in timeframes_2y:
            profits_df = validate(name, strategy, timeframe=tf, profits_df=profits_df)

    profits = profits_df.sort_values(by="profit", ascending=False)
    print(profits)
    profits.to_csv("backtesting/profit_2yo.csv")

    # 1Mo backtest
    profits_df = None

    for name, strategy in strategies.items():
        for tf in timeframes_1mo:
            profits_df = validate(name, strategy, timeframe=tf, profits_df=profits_df)

    profits = profits_df.sort_values(by="profit", ascending=False)
    print(profits)
    profits.to_csv("backtesting/profit_1mo.csv")
    pass


def validate(
    strat_name, strategy, timeframe="1h", profits_df=None, tickers=None, **kwargs
):
    """
    Validate a strategy over a given timeframe and tickers.

    Args:
        strat_name (str): Name of the strategy to validate.
        strategy (bt.Strategy): The strategy to validate.
        timeframe (str): The timeframe to validate the strategy over.
        profits_df (pd.DataFrame): A DataFrame to store the profits of the strategy.
        tickers (list): A list of stock tickers to validate the strategy over.
        **kwargs: Additional keyword arguments for the strategy.

    """
    if tickers is None:
        tickers = [
            "MSFT",  # Microsoft Corporation
            "NVDA",  # NVIDIA Corporation
            "AMZN",  # Amazon.com, Inc.
            "GOOG",  # Alphabet Inc. (Class C)
            "META",  # Meta Platforms, Inc.
            "TSLA",  # Tesla, Inc.
            "AVGO",  # Broadcom Inc.
            "LLY",  # Eli Lilly and Company
            "AAPL",  # Apple Inc.
        ]

    cols = ["profit", "ticker", "strategy", "timeframe"]
    if profits_df is None:
        profits_df = pd.DataFrame(columns=cols)

    # Dictionary for the timeframes
    timeframes = {"5m": 5, "15m": 15, "1h": 60, "1d": 1}

    # Determines timeframe type for bt
    timeframe_str = {
        "5m": bt.TimeFrame.Minutes,
        "15m": bt.TimeFrame.Minutes,
        "1h": bt.TimeFrame.Minutes,
        "1d": bt.TimeFrame.Days,
    }

    # Determines date formate
    if timeframe_str[timeframe] == bt.TimeFrame.Minutes:
        dtformat = "%Y-%m-%d %H:%M:%S%z"
    else:
        dtformat = "%Y-%m-%d"

    # Determines start date
    if timeframe in ["15m", "5m"]:
        start_date = "2025-03-04"
    else:
        start_date = "2023-04-10"

    # iterates through the stock tickers, downloads the data/reads it from csv file
    # Then runs the strategy
    for ticker in tickers:

        filepath = f"backtesting/data/{ticker.lower()}_data_{timeframe}.csv"

        if not os.path.exists(filepath):
            df = pd.DataFrame(
                yf.download(
                    ticker, start=start_date, end=datetime.today(), interval=timeframe
                )
            )
            df.columns = ["Close", "High", "Low", "Open", "Volume"]

            df.to_csv(filepath)

        else:
            df = pd.read_csv(filepath)

        data = bt.feeds.GenericCSVData(
            dataname=filepath,
            dtformat=dtformat,
            timeframe=timeframe_str[timeframe],
            compression=timeframes[timeframe],
            datetime=0,
            open=4,
            high=2,
            low=3,
            close=1,
            volume=5,
            openinterest=-1,
        )

        cerebro = bt.Cerebro()
        cerebro.addstrategy(strategy, **kwargs)
        cerebro.adddata(data)

        cerebro.broker.set_cash(10000)
        cerebro.broker.setcommission(commission=0.00)  # 0.1%

        cerebro.run()

        profit = round((cerebro.broker.getvalue() / 10000) - 1, 2)
        strat = [profit, ticker, strat_name, timeframe]

        profits_df.loc[len(profits_df)] = strat

    return profits_df


if __name__ == "__main__":

    main()
