import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import backtrader as bt

stocks = ["AAPL", "MSFT", "GOOG", "NVDA", "META", "AMZN", "TSLA"]
df = df = pd.read_csv("data.csv", index_col = 0, header = [0, 1])
df.index = pd.to_datetime(df.index)

weights = pd.DataFrame({
            "date": df.index,
            "AAPL": [.1] * len(df.index), 
            "MSFT": [.1] * len(df.index), 
            "GOOG": [.1] * len(df.index), 
            "NVDA": [.1] * len(df.index), 
            "META": [.1] * len(df.index), 
            "AMZN": [.1] * len(df.index), 
            "TSLA": [.1] * len(df.index)
        }).set_index('date')

class Trader(bt.Strategy):
    def __init__(self):
        self.weights = weights

    def next(self):
        dt = self.datas[0].datetime.date(0)
        dt = pd.to_datetime(dt)

        if dt in self.weights.index:
            weight_AAPL = self.weights.loc[dt, "AAPL"]
            weight_MSFT = self.weights.loc[dt, "MSFT"]
            weight_GOOG = self.weights.loc[dt, "GOOG"]
            weight_NVDA = self.weights.loc[dt, "NVDA"]
            weight_META = self.weights.loc[dt, "META"]
            weight_AMZN = self.weights.loc[dt, "AMZN"]
            weight_TSLA = self.weights.loc[dt, "TSLA"]
            
            self.order_target_percent(data = self.datas[0], target = weight_AAPL)
            self.order_target_percent(data = self.datas[1], target = weight_MSFT)
            self.order_target_percent(data = self.datas[2], target = weight_GOOG)
            self.order_target_percent(data = self.datas[3], target = weight_NVDA)
            self.order_target_percent(data = self.datas[4], target = weight_META)
            self.order_target_percent(data = self.datas[5], target = weight_AMZN)
            self.order_target_percent(data = self.datas[6], target = weight_TSLA)


data_feeds = []

for stock in stocks:
    feed = bt.feeds.PandasData(dataname = df[stock])
    data_feeds.append(feed)

cerebro = bt.Cerebro()
cerebro.addstrategy(Trader)

cerebro.addanalyzer(bt.analyzers.PyFolio, _name='pyfolio')
cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe')
cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')

for data in data_feeds:
    cerebro.adddata(data)

cerebro.broker.set_cash(10_000)

results = cerebro.run()
strategy = results[0]

print(f"Sharpe Ratio: {strategy.analyzers.sharpe.get_analysis()}")
print(f"Max Drawdown: {strategy.analyzers.drawdown.get_analysis()}")

final_value = cerebro.broker.get_value()
print(final_value)

cerebro.plot()