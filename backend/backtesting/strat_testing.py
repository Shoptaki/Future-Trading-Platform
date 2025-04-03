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
    ticker = "AAPL"

    # data = yf.download("AAPL", start="2022-01-01", end="2023-01-01")
    filepath = f"backtesting/{ticker.lower()}_data.csv"

    df = pd.DataFrame(
        yf.download(ticker, start="2025-03-04", end=datetime.today(), interval="15m")
    )

    df.columns = ["Close", "High", "Low", "Open", "Volume"]

    df.to_csv(filepath)

    data = bt.feeds.GenericCSVData(
        dataname=filepath,
        dtformat="%Y-%m-%d %H:%M:%S%z",
        timeframe=bt.TimeFrame.Minutes,
        compression=15,
        datetime=0,
        open=4,
        high=2,
        low=3,
        close=1,
        volume=5,
        openinterest=-1,
    )

    cerebro = bt.Cerebro()
    cerebro.addstrategy(VolumeBreakout)
    cerebro.adddata(data)

    cerebro.broker.set_cash(10000)
    cerebro.broker.setcommission(commission=0.00)  # 0.1%

    print("Starting Portfolio Value: %.2f" % cerebro.broker.getvalue())

    cerebro.run()

    print("Final Portfolio Value: %.2f" % cerebro.broker.getvalue())

    plt.rcParams.update(
        {
            "font.size": 14,  # Increase this for bigger text
            "axes.titlesize": 16,
            "axes.labelsize": 14,
            "xtick.labelsize": 12,
            "ytick.labelsize": 12,
            "legend.fontsize": 12,
        }
    )

    cerebro.plot(iplot=False, figsize=(18, 10), dpi=480)  # Width x Height in inches


def validate(
    strat_name, strategy, timeframe="1h", profits_df=None, robust_test=False, **kwargs
):
    stock_tickers = [
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

    # Dictionary for the
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

    for ticker in stock_tickers:

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

        if not robust_test:
            cerebro = bt.Cerebro()
            cerebro.addstrategy(strategy, **kwargs)
            cerebro.adddata(data)

            cerebro.broker.set_cash(10000)
            cerebro.broker.setcommission(commission=0.00)  # 0.1%

            cerebro.run()

            profit = round((cerebro.broker.getvalue() / 10000) - 1, 2)
            strat = [profit, ticker, strat_name, timeframe]

            profits_df.loc[len(profits_df)] = strat

        else:
            param_testing(data, ticker, profits_df, strat_name, strategy)

    return profits_df


def param_testing(data, ticker, profits_df, strat_name, strategy):

    for tp in range(1, 20):
        tp = tp / 200
        for sl in range(1, 20):
            sl = sl / 200

            cerebro = bt.Cerebro()
            cerebro.addstrategy(strategy, target=tp, stoploss=sl)
            cerebro.adddata(data)

            cerebro.broker.set_cash(10000)
            cerebro.broker.setcommission(commission=0.00)  # 0.1%

            cerebro.run()

            profit = round((cerebro.broker.getvalue() / 10000) - 1, 2)
            strat = [profit, 10, 30, tp, sl, ticker, strat_name]

            profits_df.loc[len(profits_df)] = strat

    for sma1 in range(5, 15):
        for sma2 in range(sma1, 30):

            cerebro = bt.Cerebro()
            cerebro.addstrategy(strategy, sma1, sma2)
            cerebro.adddata(data)

            cerebro.broker.set_cash(10000)
            cerebro.broker.setcommission(commission=0.001)  # 0.1%

            cerebro.run()

            profit = round((cerebro.broker.getvalue() / 10000) - 1, 2)
            strat = [profit, sma1, sma2, 0.05, 0.01, ticker, strat_name]

            profits_df.loc[len(profits_df)] = strat

    return profits_df


if __name__ == "__main__":
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
