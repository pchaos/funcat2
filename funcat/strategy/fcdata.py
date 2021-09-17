# -*- coding: utf-8 -*-
"""PandasData基类
"""

import math
import backtrader as bt
import backtrader.feeds as btfeeds
from .. import get_data_backend, get_current_freq, get_start_date, get_current_date
#  from ..context import ExecutionContext as fec

__updated__ = "2021-09-16"


class PandasDataBase(btfeeds.PandasData):
    """The ``dataname`` parameter inherited from ``feed.DataBase`` is the pandas
    DataFrame
    """
    #  lines = ('adj_close', 'pct', 'pct2', 'pct3')
    params = (
        # Possible values for datetime (must always be present)
        #  None : datetime is the "index" in the Pandas Dataframe
        #  -1 : autodetect position or case-wise equal name
        #  >= 0 : numeric index to the colum in the pandas dataframe
        #  string : column name (as index) in the pandas dataframe
        ('datetime', None),
        # Possible values below:
        #  None : column not present
        #  -1 : autodetect position or case-wise equal name
        #  >= 0 : numeric index to the colum in the pandas dataframe
        #  string : column name (as index) in the pandas dataframe
        ('open', 'open'),
        ('high', 'high'),
        ('low', 'low'),
        ('close', 'close'),
        ('volume', 'volume'),
        ('openinterest', None),
    )


class CSVDataBase(bt.feeds.GenericCSVData):
    params = (
        ('nullvalue', float('NaN')),
        #  ('dtformat', '%Y-%m-%dT%H:%M:%S.%fZ'),
        ('dtformat', '%Y-%m-%d'),
        #  ('datetime', -1),
        ('datetime', "Date"),
        #  ('time', -1),
        ('time', None),
        ('open', -1),
        ('high', -1),
        ('low', -1),
        ('close', -1),
        ('volume', -1),
        #  ('openinterest', -1),
        ('openinterest', None),
    )


class MaxShares(bt.Sizer):
    """计算最大可买、卖数量
    用法： cerebro.addsizer(MaxShares)
    """

    def _getsizing(self, comminfo, cash, data, isbuy):
        if isbuy:
            self.p.stake = math.floor(cash / data.close[0] / 100) * 100
            return self.p.stake

        position = self.broker.getposition(data)
        if not position.size:
            return 0  # do not sell if nothing is open

        return self.p.stake


def addPandasData(codes, cerebro: bt.Cerebro, pandas_data_type=PandasDataBase):
    """将证券代码转换为对应的PandasData，并添加pandasData数据到cerebro
    """
    be = get_data_backend()
    start = get_start_date()
    end = get_current_date()
    freq = get_current_freq()
    if isinstance(codes, str):
        # 统一转换成list类型
        codes = [codes]
    dflist = []
    if hasattr(be, 'get_dataFrames'):
        dflist = be.get_dataFrames(codes, start, end, freq)

    for i, data in enumerate(dflist):
        pdf = pandas_data_type(dataname=data)
        cerebro.adddata(pdf, name=codes[i])
