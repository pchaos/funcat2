# -*- coding: utf-8 -*-

import unittest
from datetime import datetime
import numpy as np
from matplotlib import pyplot as plt
import backtrader as bt
from backtrader import indicators as btind
from funcat.api import *
from funcat.conditional_selection import *
from funcat.utils import FuncatTestCase
from funcat.strategy import addPandasData, MaxShares

__updated__ = "2021-10-02"


def condition_kama_ema2(n: int = 10, m: float = 0.1):
    kman = KAMA(CLOSE, n)
    amastd = STD(kman, 20)
    return (CLOSE > kman) & (CLOSE > kman + m * amastd)


def up_down(n: int = 20):
    """n天相对价格

    :n: int
    :returns: TODO

    """
    pre_close = REF(CLOSE, n)
    return (CLOSE - pre_close) / pre_close


class UpdownIndicator(bt.Indicator):
    lines = ('updown', 'signal')  # output line (array)
    params = (
        ('period', 20),  # distance to previous data point
    )

    def __init__(self):
        #  for i, d in enumerate(self.datas):
        #  diff = self.data[0] - self.data(-self.p.period)
        diff = self.data - self.data(-self.p.period)
        diffdiv = diff / self.data(-self.p.period)
        self.l.updown = diffdiv


class UpDownStrategy(bt.Strategy):
    """大小盘轮动策略
    """
    params = dict(period=20, )

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def notify_order(self, order):
        # 1. If order is submitted/accepted, do nothing
        if order.status in [order.Submitted, order.Accepted]:
            return
        # 2. If order is buy/sell executed, report price executed
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: {0:8.3f}, Cost: {1:8.3f}, Comm: {2:8.4f}'
                    .format(order.executed.price, order.executed.value,
                            order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:
                self.log(
                    'SELL EXECUTED, {0:8.3f}, Cost: {1:8.3f}, Comm{2:8.4f}'.
                    format(order.executed.price, order.executed.value,
                           order.executed.comm))

            self.bar_executed = len(self)  # when was trade executed
        # 3. If order is canceled/margin/rejected, report order canceled
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

    def notify_trade(self, trade):
        if trade.isclosed:
            self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                     (trade.pnl, trade.pnlcomm))
            self.log(
                f'Current Portfolio Value: ${format(self.broker.getvalue())}')

    def __init__(self):
        """TODO: to be defined. """
        self.o = dict()  # orders per data (main, stop, limit, manual-close)
        self.inds = dict()
        self.updown = dict()
        for i, data in enumerate(self.datas):
            self.updown[i] = UpdownIndicator(self.datas[i].close,
                                             period=self.p.period)
            if i > 0:
                self.inds[i] = self.updown[i] >= self.updown[0]

        self.order = None

    def next(self):
        j = 0
        for i, d in enumerate(self.datas):
            #  if i == 0:
            #  self.signal = d
            #  else:
            # 取最大值
            #  updown0 = self.l.updown[i](0)
            #  self.signal = max(self.signal, updown0)

            #  dt, dn = self.datetime.date(), d._name
            pos = self.getposition(d)  # current size of the position
            #  pos = self.getposition().size  # current size of the position
            #  pos = self.positions
            #  print(f'{i} {d._name} {pos=}')
            #  print('{} {} Position {}'.format(dt, dn, pos))
            #  print(f"{i=} {d=}")

            if len(pos):
                self.log('{}, 持仓:{}, 成本价:{}, 当前价:{}, 盈亏:{:.2f}'.format(
                    d._name, pos.size, pos.price, pos.adjbase,
                    pos.size * (pos.adjbase - pos.price)))

            pos = self.getposition(d).size  # current size of the position
            # 最
            # j = 1
            #  signal = self.inds[1][len(self)]
            signal1 = self.inds[1]
            signal = signal1[0]
            #  if i == 0:
            #  print(f"{signal=} {self.inds[1].array=}")
            #  for k in range(20):
            #  print(f"{len(self)} {self.inds[1][-k]}", end=", ")
            #  print("")
            if not pos and self.broker.cash > 10000:
                #  if len(pos) == 0:
                #  if not self.o.get(d, None):
                j = 1 if i == 0 else i
                #  signal = self.lines.updown[1]
                if i == j and (signal):
                    #  if (self.inds[j][0] - self.inds[j][-1] >= 0):
                    self.log('BUY CREATE {0:8.3f}'.format(self.datas[i][0]))
                    self.buy(data=self.datas[i], exectype=bt.Order.Market)
                    self.o[self.datas[i]._name] = self.datas[i]._name
                elif (i != j) and (not signal):
                    self.log('BUY CREATE {0:8.3f}'.format(self.datas[i][0]))
                    self.buy(data=self.datas[0])
                    self.o[d._name] = self.datas[0]._name

            else:  # exiting can also happen after a number of days
                if (self.o.keys() == dict({
                        f"{d._name}": f"{d._name}"
                }).keys()) and ((i == 1 and not signal) or
                                ((i == 0) and signal)):
                    #  if (self.inds[j][0] - self.inds[j][-1] < 0):
                    self.log(f'SELL CREATE, {self.datas[i][0]:8.3f}')
                    self.sell(data=self.o[d._name])
                    #  self.o[d._name] = None
                    del self.o[d._name]
            #  print(f"{self.datetime.date()} order: {self.o}")


class MyStrategy(bt.Strategy):
    def __init__(self):
        self.sma = bt.ind.SMA(period=10)

    def next(self):
        if self.sma > self.data.close:
            print('BUY CREATE, %.2f' % self.data.close[0])
            self.order = self.buy()
        elif self.sma < self.data.close:
            print('SELL CREATE, %.2f' % self.data.close[0])
            self.order = self.sell()


class TestFcdata(FuncatTestCase):
    @classmethod
    def setUp(cls) -> None:
        T("20210901")
        #  S("000001.XSHG")

    def test_addPandasData(self):
        # 回测期间
        start = datetime(2010, 1, 31)
        end = datetime(2020, 8, 31)
        # 初始化cerebro回测系统设置
        cerebro = bt.Cerebro()
        cerebro.addstrategy(MyStrategy)
        codes = ['510300.etf', '159949.etf']
        #  codes = '000001'
        # 加载数据
        addPandasData(codes, cerebro=cerebro)
        startcash = 100000.0
        cerebro.broker.setcash(startcash)

        cerebro.addsizer(bt.sizers.FixedSize, stake=1)

        cerebro.broker.setcommission(commission=0.005)

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

    def test_addPandasData_kama(self):
        # 回测期间
        start = datetime(2013, 1, 31)
        end = datetime(2020, 8, 31)
        set_start_date(start)
        # 初始化cerebro回测系统设置
        cerebro = bt.Cerebro()
        cerebro.addstrategy(UpDownStrategy)
        #  codes= ['000001', '000001.XSHG']
        #  codes = ['510300.etf', '159949.etf']
        codes = ['510300.etf', '159915.etf']
        #  codes = '000001'
        # 加载数据
        addPandasData(codes, cerebro=cerebro)
        startcash = 100000.0
        cerebro.broker.setcash(startcash)

        cerebro.addsizer(MaxShares)

        cerebro.broker.setcommission(commission=0.002)

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
        plt.rcParams["font.family"] = "FangSong"
        plt.rcParams['font.sans-serif'] = ['SimHei']
        #  plt.rcParams['axes.unicode_minus'] = True
        plt.rcParams['axes.unicode_minus'] = False
        plt.rcParams['figure.figsize'] = [18, 16]
        plt.rcParams['figure.dpi'] = 300
        plt.rcParams['figure.facecolor'] = 'w'
        plt.rcParams['figure.edgecolor'] = 'k'
        cerebro.plot(title="up down ", style='candlestick')


if __name__ == '__main__':
    unittest.main()
