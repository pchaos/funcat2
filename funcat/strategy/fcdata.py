# -*- coding: utf-8 -*-
"""PandasData基类
"""

import backtrader as bt

class PandasDataBase(bt.feeds.PandasData):
    #  lines = ('adj_close', 'pct', 'pct2', 'pct3')
    params = (
        ('datetime', 'datatime'),
        ('open', 'open'),
        ('high', 'high'),
        ('low', 'low'),
        ('close', 'close'),
        ('volume', 'volume'),
        ('openinterest', None),
    )
