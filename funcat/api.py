# -*- coding: utf-8 -*-
"""1，HIGH 最高价 返回该周期最高价。 用法：HIGH
2，H 最高价 返回该周期最高价。 用法： H
3， LOW 最低价 返回该周期最低价。 用法： LOW
4， L 最低价 返回该周期最低价。 用法： L
5、CLOSE 收盘价 返回该周期收盘价。 用法： CLOSE
6， C 收盘价 返回该周期收盘价。 用法： C
7， VOL 成交量 返回该周期成交量。 用法： VOL
8， V 成交量 返回该周期成交量。 用法： V
9， OPEN 开盘价 返回该周期开盘价。 用法： OPEN
10，O：开盘价 返回该周期开盘价。 用法： O
"""
import numpy as np

__updated__ = "2021-06-16"

from .time_series import MarketDataSeries, NumericSeries

from .func import (
    SumSeries,
    AbsSeries,
    StdSeries,
    SMASeries,
    CCISeries,
    MovingAverageSeries,
    WeightedMovingAverageSeries,
    ExponentialMovingAverageSeries,
    KAMASeries,
    CrossOver,
    minimum,
    maximum,
    every,
    count,
    hhv,
    llv,
    hhvbars,
    llvbars,
    Ref,
    iif,
    ceiling,
    const,
    drawnull,
    zig,
    troughbars,
    barslast,
    mular,
    upnday,
    downnday,
    nday
)
from .context import (
    symbol,
    set_current_security,
    get_current_security,
    set_current_date,
    get_current_date,
    set_start_date,
    get_start_date,
    set_data_backend,
    set_current_freq,
    get_current_freq,
)
from .helper import select, select2, selectAsync, backtest, zig_helper
# from .conditional_selection import hong_san_bing, FOURWEEK, FOURWEEKQTY

# create open high low close volume datetime
for name in ["open", "high", "low", "close", "volume", "datetime"]:
    # dtype = np.float64 if name != "datetime" else np.uint64
    dtype = float if name != "datetime" else int
    cls = type("{}Series".format(name.capitalize()),
               (MarketDataSeries,), {"name": name, "dtype": dtype})
    obj = cls(dynamic_update=True)
    for var in [name[0], name[0].upper(), name.upper()]:
        globals()[var] = obj

VOL = VOLUME

MA = MovingAverageSeries
WMA = WeightedMovingAverageSeries
EMA = ExponentialMovingAverageSeries
SMA = SMASeries
KAMA = KAMASeries
CCI = CCISeries

SUM = SumSeries
ABS = AbsSeries
STD = StdSeries

CROSS = CrossOver
REF = Ref
MIN = minimum
MAX = maximum
EVERY = every
UPNDAY = upnday
DOWNNDAY = downnday
NDAY = nday
COUNT = count
HHV = hhv
LLV = llv
HHVBARS = hhvbars
LLVBARS = llvbars
IF = IIF = iif
BARSLAST = barslast
MULAR = mular
CEILING = ceiling
CONST = const
DRAWNULL = drawnull
ZIG = zig  # zig当前以收盘价为准
TROUGHBARS = troughbars

S = set_current_security
T = set_current_date

__all__ = [
    "OPEN", "O",
    "HIGH", "H",
    "LOW", "L",
    "CLOSE", "C",
    "VOLUME", "V", "VOL",
    "DATETIME",

    "SMA",
    "CCI",
    "MA",
    "EMA",
    "WMA",
    "KAMA",

    "SUM",
    "ABS",
    "STD",

    "CROSS",
    "REF",
    "MAX",
    "MIN",
    "EVERY",
    "COUNT",
    "HHV",
    "LLV",
    "HHVBARS",
    "LLVBARS",
    "IF", "IIF",
    "BARSLAST",
    "CEILING",
    "CONST",
    "DRAWNULL",
    "ZIG",
    "TROUGHBARS",
    "MULAR",
    "UPNDAY",
    "DOWNNDAY",
    "NDAY",

    "S",
    "T",

    "select",
    "select2",
    "selectAsync",
    "backtest",
    "zig_helper",
    "symbol",
    "set_current_security",
    "get_current_security",
    "set_current_date",
    "get_current_date",
    "set_start_date",
    "get_start_date",
    "set_data_backend",
    "set_current_freq",
    "get_current_freq",
    "NumericSeries",

    # "HSB",
    # "FOURWEEK",
    # "FOURWEEKQTY",
]
