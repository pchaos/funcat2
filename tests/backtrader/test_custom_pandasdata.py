# -*- coding: utf-8 -*-

from datetime import datetime
import backtrader as bt
import pandas as pd
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt

__updated__ = "2021-08-08"

data = pdr.get_data_yahoo('AAPL',
                          start=datetime(2017, 8, 13),
                          end=datetime(2018, 8, 14))

data.columns = ['high', 'low', 'open', 'close', 'volume', 'adj_close']
data['pct'] = data.close.pct_change(1) * 100
data['pct2'] = data.close.pct_change(2) * 100
data['pct3'] = data.close.pct_change(3) * 100

ax = plt.gca()
data.plot(kind='line', y='close', use_index=True, color='blue', ax=ax)
data.plot(kind='line', y='pct', use_index=True, color='red', ax=ax)
#  plt.show()


class PandasData(bt.feeds.PandasData):
    lines = ('adj_close', 'pct', 'pct2', 'pct3')
    params = (
        ('datetime', None),
        ('open', 'open'),
        ('high', 'high'),
        ('low', 'low'),
        ('close', 'close'),
        ('volume', 'volume'),
        ('openinterest', None),
        ('adj_close', 'adj_close'),
        ('pct', 'pct'),
        ('pct2', 'pct2'),
        ('pct3', 'pct3'),
    )


class MyStrategy(bt.Strategy):
    def __init__(self):
        self.sma = bt.ind.SMA(period=10)

    def next(self):
        if self.sma > self.data.close and self.data.pct > 0 or self.data.pct2 > 0:
            print('BUY CREATE, %.2f' % self.data.close[0])
        elif self.sma < self.data.close and self.data.pct < 0 or self.data.pct2 < 0:
            print('SELL CREATE, %.2f' % self.data.close[0])
            self.order = self.sell()


cerebro = bt.Cerebro()
cerebro.addstrategy(MyStrategy)

#data = bt.feeds.YahooFinanceData(dataname='MSFT', fromdate=datetime(2011, 1, 1),todate=datetime(2012, 12, 31))
df = PandasData(dataname=data)
cerebro.adddata(df)
cerebro.broker.setcash(100000.0)

cerebro.addsizer(bt.sizers.FixedSize, stake=1)

cerebro.broker.setcommission(commission=0.05)

cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='mysharpe')
cerebro.addanalyzer(bt.analyzers.DrawDown, _name='DrawDown')

print('Starting Balance: %.2f' % cerebro.broker.getvalue())

strats = cerebro.run(stdstats=False)
strat = strats[0]
cerebro.addobserver(bt.observers.Value)

print('Sharpe Ratio:', strat.analyzers.mysharpe.get_analysis())
print('DrawDown:', strat.analyzers.DrawDown.get_analysis())
print('Final Balance: %.2f' % cerebro.broker.getvalue())
cerebro.run()
print(f"Done.")
