# -*- coding: utf-8 -*-

import unittest
from datetime import datetime
import numpy as np
from matplotlib import pyplot as plt
import backtrader as bt
from funcat.api import *
from funcat.conditional_selection import *
from funcat.utils import FuncatTestCase
from funcat.strategy import addPandasData

__updated__ = "2021-09-03"


class MyStrategy(bt.Strategy):
    def __init__(self):
        self.sma = bt.ind.SMA(period=10)

    def next(self):
        if self.sma > self.data.close and self.data.pct > 0 or self.data.pct2 > 0:
            print('BUY CREATE, %.2f' % self.data.close[0])
        elif self.sma < self.data.close and self.data.pct < 0 or self.data.pct2 < 0:
            print('SELL CREATE, %.2f' % self.data.close[0])
            self.order = self.sell()


class TestFcdata(FuncatTestCase):
    @classmethod
    def setUp(cls) -> None:
        T("20210101")
        #  S("000001.XSHG")

    def test_addPandasData(self):
        # 回测期间
        start = datetime(2010, 1, 31)
        end = datetime(2020, 8, 31)
        # 初始化cerebro回测系统设置
        cerebro = bt.Cerebro()
        #  codes= ['000001', '000001.XSHG']
        codes = '000001'
        # 加载数据
        addPandasData(codes, cerebro=cerebro)
        startcash = 100000.0
        cerebro.broker.setcash(startcash)

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
        # Get final portfolio Value
        portvalue = cerebro.broker.getvalue()
        pnl = portvalue - startcash

        # Print out the final result
        print('Final Portfolio Value: ${}'.format(portvalue))
        print('P/L: ${}'.format(pnl))

        # Finally plot the end results
        # plt.rcParams['font.sans-serif']=['SimHei']
        plt.rcParams['axes.unicode_minus'] = True
        plt.rcParams['figure.figsize'] = [18, 16]
        plt.rcParams['figure.dpi'] = 300
        plt.rcParams['figure.facecolor'] = 'w'
        plt.rcParams['figure.edgecolor'] = 'k'
        cerebro.plot(style='candlestick')


if __name__ == '__main__':
    unittest.main()
