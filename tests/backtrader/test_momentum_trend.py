# -*- coding: utf-8 -*-

"""“动量+趋势跟踪”策略作为示例。策略思路为：计算N只股票过去30日的收益率并进行排序，选择前10只股票加入选股池（动量），逐日滚动计算和判断：如果选股池中某只个股满足股价位于20均线以上且没有持仓时买入（以20日均线为生命线跟踪趋势）；如果某只个股已持仓但判断不在选股池中或股价位于20均线以下则卖出。每次交易根据十只个股平均持仓（注意：最多交易10只个股）。
https://zhuanlan.zhihu.com/p/144390882
"""
import unittest
import os
import numpy as np
import pandas as pd
import backtrader as bt
from funcat.api import *
from funcat.conditional_selection import *
from funcat.utils import FuncatTestCase
from funcat.context import ExecutionContext
from funcat.time_series import get_bars

__updated__ = "2021-07-21"


def get_data(code):
    S(code)
    freq = ExecutionContext.get_current_freq()
    bars = get_bars(freq)
    data = pd.DataFrame(bars)
    if len(bars) > 0:
        # data = data[['datetime', 'open', 'high', 'low', 'close', 'volume']]
        data = data[['date', 'open', 'high', 'low', 'close', 'volume']]
        # data['datetime'] = pd.to_datetime(
        #     data['datetime'] // 1000000,
        #     format='%Y%m%d').astype('str')[
        #     :6]
        # data.set_index('datetime', inplace=True)
        data['date'] = pd.to_datetime(data['date'], format="%Y-%m-%d")
        data.set_index('date', inplace=True)
    return data


def get_code_list(date='20150202'):
    # T(date)
    filename = "../datas/etf.txt"
    currDir = os.path.join(os.path.abspath(os.path.dirname(__file__)), ".")
    fullname = os.path.join(f"{currDir}", filename)
    print(fullname)
    if os.path.exists(fullname):
        with open(fullname, "r") as f:
            codes = f.readlines()  # print(codes[:10])
    for i, item in enumerate(codes):
        codes[i] = f"{ item[:6] }.etf"
        if codes[i].startswith("000"):
            # 指数替换
            codes[i] = "588000.etf"
    if codes[0].startswith("代码"):
        print(f"del 代码")
        del codes[0]
    for i in reversed(range(len(codes))):
        # 删除空行
        if (len(codes[i].strip()) != 10):
            del codes[i]
    return codes


class MyStrategy(bt.Strategy):
    # 策略参数
    params = dict(
        period=20,  # 均线周期
        look_back_days=30,
        printlog=False
    )

    def __init__(self):
        self.mas = dict()
        # 遍历所有股票,计算20日均线
        for data in self.datas:
            self.mas[data._name] = bt.ind.SMA(data.close, period=self.p.period)
            print(f"{data._name}:{data.close.array[-10:]}")

    def next(self):
        # 计算截面收益率
        rate_list = []
        for data in self.datas:
            if len(data) > self.p.look_back_days:
                p0 = data.close[0]
                pn = data.close[-self.p.look_back_days]
                rate = (p0 - pn) / pn
                rate_list.append([data._name, rate])

        # 股票池
        long_list = []
        sorted_rate = sorted(rate_list, key=lambda x: x[1], reverse=True)
        long_list = [i[0] for i in sorted_rate[:10]]

        # 得到当前的账户价值
        total_value = self.broker.getvalue()
        p_value = total_value * 0.9 / 10
        for data in self.datas:
            # 获取仓位
            pos = self.getposition(data).size
            if not pos and data._name in long_list and \
                    self.mas[data._name][0] > data.close[0]:
                size = int(p_value / 100 / data.close[0]) * 100
                self.buy(data=data, size=size)

            if pos != 0 and data._name not in long_list or \
                    self.mas[data._name][0] < data.close[0]:
                self.close(data=data)

    def log(self, txt, dt=None, doprint=False):
        if self.params.printlog or doprint:
            dt = dt or self.datas[0].datetime.date(0)
            print(f'{dt.isoformat()},{txt}')

    # 记录交易执行情况（可省略，默认不输出结果）
    def notify_order(self, order):
        # 如果order为submitted/accepted,返回空
        if order.status in [order.Submitted, order.Accepted]:
            return
        # 如果order为buy/sell executed,报告价格结果
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f'买入:\n价格:{order.executed.price:.2f},\
                成本:{order.executed.value:.2f},\
                手续费:{order.executed.comm:.2f}')

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:
                self.log(f'卖出:\n价格：{order.executed.price:.2f},\
                成本: {order.executed.value:.2f},\
                手续费{order.executed.comm:.2f}')

            self.bar_executed = len(self)

        # 如果指令取消/交易失败, 报告结果
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('交易失败')
        self.order = None

    # 记录交易收益情况（可省略，默认不输出结果）
    def notify_trade(self, trade):
        if not trade.isclosed:
            return
        self.log(f'策略收益：\n毛收益 {trade.pnl:.2f}, 净收益 {trade.pnlcomm:.2f}')


class TestMovemtum(FuncatTestCase):
    @classmethod
    def setUp(cls) -> None:
        T("20310906")
        S("000001.XSHG")

    def test_movementum(self):
        cerebro = bt.Cerebro()
        for s in get_code_list()[:]:
            data = get_data(s)
            if len(data) > 30:
                feed = bt.feeds.PandasData(dataname=data)
                cerebro.adddata(feed, name=s)
            else:
                # 太短的数据，会报错
                print(f"{s} data is too short")

        # 回测设置
        startcash = 100000.0
        cerebro.broker.setcash(startcash)
        # 设置佣金为千分之一
        cerebro.broker.setcommission(commission=0.001)
        # 添加策略
        cerebro.addstrategy(MyStrategy, printlog=True)
        cerebro.run()
        # 获取回测结束后的总资金
        portvalue = cerebro.broker.getvalue()
        pnl = portvalue - startcash
        # 打印结果
        print(f'总资金: {round(portvalue,2)}')
        print(f'净收益: {round(pnl,2)}')


if __name__ == '__main__':
    unittest.main()
