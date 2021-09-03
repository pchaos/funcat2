# -*- coding: utf-8 -*-
"""PandasData基类
"""

import backtrader as bt
import backtrader.feeds as btfeeds
from .. import get_data_backend, get_current_freq, get_start_date, get_current_date

from ..context import ExecutionContext as fec

__updated__ = "2021-09-03"


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


def addPandasData(codes, cerebro: bt.Cerebro, pandas_data_type=PandasDataBase):
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
    #  else:
        #  todo 调用be.get_price
        #  for code in codes:
        #  data=be.get_price(codes, start, end, freq)
        #  df= pd.Dataframe(data)
        #  dflist.append(df)

    for i, data in enumerate(dflist):
        pdf = pandas_data_type(dataname=data)
        cerebro.adddata(pdf)
