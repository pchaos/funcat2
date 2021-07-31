# -*- coding: utf-8 -*-
'''
Author: www.backtest-rookies.com

MIT License

Copyright (c) 2017 backtest-rookies.com

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

https://backtest-rookies.com/2017/08/22/backtrader-multiple-data-feeds-indicators/
'''

from datetime import datetime
import unittest
import numpy as np
from matplotlib import pyplot as plt
import backtrader as bt
from funcat.api import *
from funcat.conditional_selection import *
from funcat.utils import FuncatTestCase

__updated__ = "2021-07-22"


class maCross(bt.Strategy):
    '''
    For an official backtrader blog on this topic please take a look at:

    https://www.backtrader.com/blog/posts/2017-04-09-multi-example/multi-example.html

    oneplot = Force all datas to plot on the same master.
    '''
    params = (('sma1', 40), ('sma2', 200), ('oneplot', True))

    def __init__(self):
        '''
        Create an dictionary of indicators so that we can dynamically add the
        indicators to the strategy using a loop. This mean the strategy will
        work with any numner of data feeds. 
        '''
        self.inds = dict()
        for i, d in enumerate(self.datas):
            self.inds[d] = dict()
            self.inds[d]['sma1'] = bt.indicators.SimpleMovingAverage(
                d.close, period=self.params.sma1)
            self.inds[d]['sma2'] = bt.indicators.SimpleMovingAverage(
                d.close, period=self.params.sma2)
            self.inds[d]['cross'] = bt.indicators.CrossOver(
                self.inds[d]['sma1'], self.inds[d]['sma2'])

            if i > 0:  #Check we are not on the first loop of data feed:
                if self.p.oneplot == True:
                    d.plotinfo.plotmaster = self.datas[0]

    def next(self):
        for i, d in enumerate(self.datas):
            dt, dn = self.datetime.date(), d._name
            pos = self.getposition(d).size
            if not pos:  # no market / no orders
                if self.inds[d]['cross'][0] == 1:
                    self.buy(data=d, size=1000)
                elif self.inds[d]['cross'][0] == -1:
                    self.sell(data=d, size=1000)
            else:
                if self.inds[d]['cross'][0] == 1:
                    self.close(data=d)
                    self.buy(data=d, size=1000)
                elif self.inds[d]['cross'][0] == -1:
                    self.close(data=d)
                    self.sell(data=d, size=1000)

    def notify_trade(self, trade):
        dt = self.data.datetime.date()
        if trade.isclosed:
            print('{} {} Closed: PnL Gross {}, Net {}'.format(
                dt, trade.data._name, round(trade.pnl, 2),
                round(trade.pnlcomm, 2)))


class OandaCSVData(bt.feeds.GenericCSVData):
    params = (
        ('nullvalue', float('NaN')),
        ('dtformat', '%Y-%m-%dT%H:%M:%S.%fZ'),
        ('datetime', 6),
        ('time', -1),
        ('open', 5),
        ('high', 3),
        ('low', 4),
        ('close', 1),
        ('volume', 7),
        ('openinterest', -1),
    )


class Test_multi_feeds_indicator(FuncatTestCase):
    @classmethod
    def setUp(cls) -> None:
        T("20210506")
        S("000001.XSHG")

    def test_multi_feeds_indicator(self):

        #Variable for our starting cash
        startcash = 10000

        #Create an instance of cerebro
        cerebro = bt.Cerebro()

        #Add our strategy
        cerebro.addstrategy(maCross, oneplot=False)

        #create our data list
        datalist = [
            ('../datas/CAD_CHF-2005-2017-D1.csv',
             'CADCHF'),  #[0] = Data file, [1] = Data name
            ('../datas/EUR_USD-2005-2017-D1.csv', 'EURUSD'),
            ('../datas/GBP_AUD-2005-2017-D1.csv', 'GBPAUD'),
        ]

        #Loop through the list adding to cerebro.
        for i in range(len(datalist)):
            data = OandaCSVData(dataname=datalist[i][0])
            cerebro.adddata(data, name=datalist[i][1])

        # Set our desired cash start
        cerebro.broker.setcash(startcash)

        # Run over everything
        cerebro.run()

        #Get final portfolio Value
        portvalue = cerebro.broker.getvalue()
        pnl = portvalue - startcash

        #Print out the final result
        print('Final Portfolio Value: ${}'.format(portvalue))
        print('P/L: ${}'.format(pnl))

        #Finally plot the end results
        # plt.rcParams['font.sans-serif']=['SimHei']
        plt.rcParams['axes.unicode_minus']=False
        plt.rcParams['figure.figsize']=[18, 16]
        plt.rcParams['figure.dpi']=300
        plt.rcParams['figure.facecolor']='w'
        plt.rcParams['figure.edgecolor']='k'
        cerebro.plot(style='candlestick')

        # Store the figures returned by cerebro.plot() and plot them w/plotly
        # result = cerebro.plot()
        # plotly.offline.plot_mpl(result[0][0], filename='simple_candlestick.html')
if __name__ == '__main__':
    unittest.main()
