import yfinance as yf
import backtrader as bt
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from Strategies import SmaCross


def main():
    ticker = "AAPL"

    # data = yf.download("AAPL", start="2022-01-01", end="2023-01-01")
    filepath = f"backend/backtesting/{ticker.lower()}_data.csv"

    df = pd.DataFrame(
        yf.download(ticker, start="2025-02-27", end=datetime.today(), interval="15m")
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
    cerebro.addstrategy(SmaCross)
    cerebro.adddata(data)

    cerebro.broker.set_cash(10000)
    cerebro.broker.setcommission(commission=0.001)  # 0.1%

    print("Starting Portfolio Value: %.2f" % cerebro.broker.getvalue())

    cerebro.run(runonce=True)

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


if __name__ == "__main__":
    main()
