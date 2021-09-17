# -*- coding: utf-8 -*-

import datetime
import os.path
import sys
import math
import pandas as pd

import backtrader as bt
from funcat.strategy import PandasDataBase, MaxShares, CSVDataBase

__updated__ = "2021-09-17"


class TestStrategy(bt.Strategy):

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

        # Keep track of pending orders
        self.order = None
        self.buyprice = None
        self.buycomm = None

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm: %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            elif order.issell():
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm: %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))

    def next(self):

        if self.order:
            return

        if not self.position:
            # Not yet in the market... we MIGHT BUY if...
            if self.dataclose[0] < self.dataclose[-1]:
                if self.dataclose[-1] < self.dataclose[-2]:
                    self.log('BUY CREATE, %.2f' % self.dataclose[0])
                    self.order = self.buy()
        else:
            # Already in the market... we might sell
            if len(self) >= (self.bar_executed + 5):
                self.log('SELL CREATE, %.2f' % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell()


class MaxShares(bt.Sizer):
    def _getsizing(self, comminfo, cash, data, isbuy):
        if isbuy:
            self.p.stake = math.floor(cash / data.close[0])
            return self.p.stake - 100

        position = self.broker.getposition(data)
        if not position.size:
            return 0  # do not sell if nothing is open

        return self.p.stake


class DegiroCommission(bt.CommInfoBase):

    params = (
        ('flat', 0.5),
        ('per_share', 0.004),
    )

    def _getcommission(self, size, price, pseudoexec):
        return self.p.flat + size * self.p.per_share


class PandasData(PandasDataBase):
    params = (
        # Possible values for datetime (must always be present)
        #  None : datetime is the "index" in the Pandas Dataframe
        #  -1 : autodetect position or case-wise equal name
        #  >= 0 : numeric index to the colum in the pandas dataframe
        #  string : column name (as index) in the pandas dataframe
        ('datetime', "datetime"),
        # Possible values below:
        #  None : column not present
        #  -1 : autodetect position or case-wise equal name
        #  >= 0 : numeric index to the colum in the pandas dataframe
        #  string : column name (as index) in the pandas dataframe
        ('open', 'open'),
        ('high', 'high'),
        ('low', 'low'),
        ('close', 'adj close'),
        ('volume', 'volume'),
        ('openinterest', None),
    )


if __name__ == '__main__':
    cerebro = bt.Cerebro()
    cerebro.addstrategy(TestStrategy)
    cerebro.broker.set_cash(10000)
    cerebro.broker.set_coc(True)

    cerebro.addsizer(MaxShares)
    comminfo = DegiroCommission()
    cerebro.broker.addcommissioninfo(comminfo)

    modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    datapath = os.path.join(modpath, '../../datas/stock_dfs/AMD.csv')
    #  data = CSVDataBase(dataname=datapath)
    df = pd.read_csv(datapath)
    df.columns = [col.lower() for col in df.columns]
    df['datetime'] = df['date'].apply(lambda x: pd.to_datetime(x))
    data = PandasData(dataname=df)
    cerebro.adddata(data, name="AMD")

    # data = bt.feeds.YahooFinanceCSVData(
    #     dataname=datapath,
    #     # Do not pass values before this date
    #     fromdate=datetime.datetime(2000, 1, 1),
    #     # Do not pass values before this date
    #     todate=datetime.datetime(2000, 12, 31),
    #     # Do not pass values after this date
    #     reverse=False)
    # cerebro.adddata(data)

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.run()
    print('Final Porfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.plot()
