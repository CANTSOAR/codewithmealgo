import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import backtrader as bt

stocks = ["NVDA", "PLTR", "TTWO", "AMD", "META", "CCL", "AAPL", "COST"]

stock_data = pd.read_csv("new_data.csv", header = [0, 1], index_col = 0)
stock_data.index = pd.to_datetime(stock_data.index)
for stock in stocks:
    data = stock_data[(stock, "Close")]
    data50SMA = data.rolling(50).mean()
    data200SMA = data.rolling(200).mean()

    stock_data[(stock, "SMA50")] = data50SMA
    stock_data[(stock, "SMA200")] = data200SMA
signals = pd.DataFrame({"date": stock_data.index}).set_index("date")

for stock in stocks:
    data50SMA = stock_data[(stock, "SMA50")]
    data200SMA = stock_data[(stock, "SMA200")]

    signal = 2 * (data50SMA > data200SMA) - 1

    signals[stock] = signal

class Golden_Cross_Trader(bt.Strategy):

    def __init__(self):
        self.trading_logic = signals


    def next(self):
        dt = self.datas[0].datetime.date(0)
        dt = pd.to_datetime(dt)

        if dt in self.trading_logic.index:
            for i, stock in enumerate(stocks):
                signal = self.trading_logic.loc[dt, stock]

                self.order_target_percent(data = self.datas[i], target = .125 * signal)

cerebro = bt.Cerebro()

for stock in stocks:
    feed = bt.feeds.PandasData(dataname = stock_data[stock])
    cerebro.adddata(data = feed)

cerebro.broker.set_cash(10_000)
cerebro.addstrategy(Golden_Cross_Trader)

cerebro.addanalyzer(bt.analyzers.PyFolio, _name='pyfolio')
cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe')
cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')

results = cerebro.run()[0]

print(f"Sharpe Ratio: {results.analyzers.sharpe.get_analysis()}")
print(f"Max Drawdown: {results.analyzers.drawdown.get_analysis()}")

cerebro.plot()[0][0].savefig("test.png")