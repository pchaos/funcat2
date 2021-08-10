# -*- coding: utf-8 -*-

from datetime import datetime
import os
from pathlib import Path  # Python 3.6+ only
import backtrader as bt
import pandas as pd
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt
from dotenv import load_dotenv

__updated__ = "2021-08-09"

# proxy servers for internet connection
env_path = f"{Path(__file__).parent}/.env"
load_dotenv(dotenv_path=env_path, verbose=True)

# 可能需要proxy
import requests
proxies = {
    'http': os.getenv("httpproxy", "127.0.0.1:8087"),
    'https': os.getenv("socks5", "socks5://127.0.0.1:1081"),
    'socks5': 'socks5://127.0.0.1:1081',
}
# proxies = {'http': '127.0.0.1:8087'}
headers = {"Accept": "application/json",
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           "Accept-Encoding": "none",
           "Accept-Language": "en-US,en;q = 0.8",
           "Connection": "keep-alive",
           "Referer": "https://cssspritegenerator.com",
           "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML,like Gecko) Chrome/23.0.1271.64 Safari/537.11"
           }

session = requests.session()
session.proxies = {}
session.proxies['http'] = 'socks5://localhost:1081'
session.proxies['https'] = 'socks5://localhost:1081'
session.proxies['socks5'] = 'socks5://localhost:1081'

# with requests.Session() as s:
#     s.headers = headers
#     s.proxies.update(proxies)
# data = pdr.DataReader('AAPL', 'yahoo',
#                       start=datetime(2018, 8, 13),
#                       end=datetime(2020, 8, 14), session=session)
data = pdr.get_data_yahoo('AAPL',
                          start=datetime(2018, 8, 13),
                          end=datetime(2020, 8, 14), session=session)

data.columns = ['high', 'low', 'open', 'close', 'volume', 'adj_close']
data['pct'] = data.close.pct_change(1) * 100
data['pct2'] = data.close.pct_change(2) * 100
data['pct3'] = data.close.pct_change(3) * 100

ax = plt.gca()
data.plot(kind='line', y='close', use_index=True, color='blue', ax=ax)
data.plot(kind='line', y='pct', use_index=True, color='red', ax=ax)
data.plot(kind='line', y='pct2', use_index=True, color='green', ax=ax)
data.plot(kind='line', y='pct3', use_index=True, color='orange', ax=ax)
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


def runstrat():
    cerebro = bt.Cerebro()
    cerebro.addstrategy(MyStrategy)

    #data = bt.feeds.YahooFinanceData(dataname='MSFT', fromdate=datetime(2011, 1, 1),todate=datetime(2012, 12, 31))
    df = PandasData(dataname=data)
    cerebro.adddata(df)
    startcash = 100000.0
    cerebro.broker.setcash(startcash)

    cerebro.addsizer(bt.sizers.FixedSize, stake=1)

    cerebro.broker.setcommission(commission=0.05)

    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='mysharpe')
    cerebro.addanalyzer(bt.analyzers.DrawDown, _namge='DrawDown')

    print('Starting Balance: %.2f' % cerebro.broker.getvalue())

    strats = cerebro.run(stdstats=False)
    strat = strats[0]
    cerebro.addobserver(bt.observers.Value)

    print('Sharpe Ratio:', strat.analyzers.mysharpe.get_analysis())
    print('DrawDown:', strat.analyzers.DrawDown.get_analysis())
    print('Final Balance: %.2f' % cerebro.broker.getvalue())
    cerebro.run()
    print(f"Done.")
    # Get final portfolio Value
    portvalue = cerebro.broker.getvalue()
    pnl = portvalue - startcash

    # Print out the final result
    print('Final Portfolio Value: ${}'.format(portvalue))
    print('P/L: ${}'.format(pnl))

    # Finally plot the end results
    # plt.rcParams['font.sans-serif']=['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams['figure.figsize'] = [18, 16]
    plt.rcParams['figure.dpi'] = 300
    plt.rcParams['figure.facecolor'] = 'w'
    plt.rcParams['figure.edgecolor'] = 'k'
    cerebro.plot(style='candlestick')


if __name__ == '__main__':
    runstrat()
