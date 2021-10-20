# -*- coding: utf-8 -*-
"""

"""
import numpy as np
import backtrader as bt

__updated__ = "2021-10-03"
 
class MQNIndicator(bt.Indicator):
    """
    1.  calculate the change each day
    2.  compute an average of this change over 'x' periods
    3.  compute a standard deviation of this change of 'x' periods
    4.  compute the square root of 'x' periods
    5.  calculate (#4\*(#2/#3))  
        Optional: 6) calculate SMA of #5
    6.  Plot #5 (and #6) (I know that I don't have a plotlines() just yet, trying to get it at least working before dealing with that)
    """
    lines = ('mqn', 'ma',)

    params = (
        ('len', 35),
        ('ma_len', 20),
    )

    def __init__(self):
        self.addminperiod(self.p.len+1)

    def next(self):
        for i, d in enumerate(self.datas):

            data = d.get(size=self.p.len+1)
            changes = []

            for i in range(1, len(data)):
                changes.append(data[-i] - data[-i-1])

            if len(changes) == self.p.len:
                avg_chng = np.average(changes)
                stdev = np.std(changes)
                sqroot = np.sqrt(self.p.len)

                mqn = sqroot * (avg_chng/stdev)

                self.l.mqn[0] = mqn

                ma = self.l.mqn.get(size=self.p.ma_len)
                self.l.ma[0] = np.average(ma)

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



