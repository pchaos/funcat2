# -*- coding: utf-8 -*-

# from functools import reduce
import numpy as np
import talib

from .context import ExecutionContext
from .utils import FormulaException, rolling_window, handle_numpy_warning
from .time_series import (
    MarketDataSeries,
    NumericSeries,
    BoolSeries,
    fit_series,
    get_series,
    get_bars,
    ensure_timeseries,
)
from .helper import zig_helper

#  ignore pandas warning
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)


# delete nan of series for error made by some operator
def filter_begin_nan(series):
    i = 0
    for x in series:
        if np.isnan(x):
            i += 1
        else:
            break
    return series[i:]


class ArgumentSeriesBase(NumericSeries):
    def getFunc(self):
        """EXAMPLE:
        def getFunc(self):
          return talib.MA
        """
        raise NotImplementedError


class OneArgumentSeries(ArgumentSeriesBase):
    def __init__(self, series, arg):
        if isinstance(series, NumericSeries):
            series = series.series

            try:
                series[np.isinf(series)] = np.nan
                # print(f"series type:{type(series)}; self.func: {help(self.func)}")
                # func = self.getFunc()
                # series = func(series, arg)
                series = self.getFunc()(series, arg)
                series = filter_begin_nan(series)
            except Exception as e:
                raise FormulaException(e)
        super(ArgumentSeriesBase, self).__init__(series)
        self.extra_create_kwargs["arg"] = arg

    # def __init__(self, series, arg):
    #     if isinstance(series, NumericSeries):
    #         series = series.series
    #
    #         try:
    #             series[np.isinf(series)] = np.nan
    #             print(f"series type:{type(series)}; self.func: {help(self.func)}")
    #             series = self.func(series, arg)
    #         except Exception as e:
    #             raise FormulaException(e)
    #     super(OneArgumentSeries, self).__init__(series)
    #     self.extra_create_kwargs["arg"] = arg


class MovingAverageSeries(OneArgumentSeries):
    """http://www.tadoc.org/indicator/MA.htm"""

    def getFunc(self):
        return talib.MA


class WeightedMovingAverageSeries(OneArgumentSeries):
    """http://www.tadoc.org/indicator/WMA.htm"""

    # func = talib.WMA
    def getFunc(self):
        return talib.WMA


class ExponentialMovingAverageSeries(OneArgumentSeries):
    """http://www.fmlabs.com/reference/default.htm?url=ExpMA.htm"""

    # func = talib.EMA
    def getFunc(self):
        return talib.EMA


class StdSeries(OneArgumentSeries):
    # func = talib.STDDEV
    def getFunc(self):
        return talib.STDDEV


class TwoArgumentSeries(ArgumentSeriesBase):
    # class TwoArgumentSeries(NumericSeries):

    def __init__(self, series, arg1, arg2):
        if isinstance(series, NumericSeries):
            series = series.series
            try:
                series[np.isinf(series)] = np.nan
                series = self.getFunc()(series, arg1, arg2)
                series = filter_begin_nan(series)
            except Exception as e:
                raise FormulaException(e)
        super(TwoArgumentSeries, self).__init__(series)
        self.extra_create_kwargs["arg1"] = arg1
        self.extra_create_kwargs["arg2"] = arg2


class SMASeries(TwoArgumentSeries):
    """同花顺专用SMA"""

    def getFunc(self):
        return self.func

    def func(self, series, n, _=None):
        results = np.nan_to_num(series).copy()
        # FIXME this is very slow
        for i in range(1, len(series)):
            results[i] = ((n - 1) * results[i - 1] + results[i]) / n
        return results


class CCISeries(TwoArgumentSeries):
    def getFunc(self):
        return talib.CCI

    def __init__(self, high, low, close):
        if isinstance(high, NumericSeries) and isinstance(low, NumericSeries) and isinstance(close, NumericSeries):
            series1 = low.series
            series2 = close.series

            try:
                series1[series1 == np.inf] = np.nan
                series2[series2 == np.inf] = np.nan
            except Exception as e:
                raise FormulaException(e)
        super(CCISeries, self).__init__(high, series1, series2)

    # def __init__(self, high, low, close):
    #     if isinstance(high, NumericSeries) and isinstance(low, NumericSeries) and isinstance(close, NumericSeries):
    #         series0 = high.series
    #         series1 = low.series
    #         series2 = close.series
    #
    #         try:
    #             series0[series0 == np.inf] = np.nan
    #             series1[series1 == np.inf] = np.nan
    #             series2[series2 == np.inf] = np.nan
    #             func = self.getFunc()
    #             # print(func, help(func))
    #             series = func(series0, series1, series2)
    #             # series = (self.getFunc())(series0, series1, series2)
    #         except Exception as e:
    #             raise FormulaException(e)
    #         super(CCISeries, self).__init__(series)


class SumSeries(NumericSeries):
    """求和"""

    def __init__(self, series, period):
        if isinstance(series, NumericSeries):
            series = series.series
            try:
                series[series == np.inf] = 0
                series[series == -np.inf] = 0
                series = talib.SUM(series, period)
            except Exception as e:
                raise FormulaException(e)
        super(SumSeries, self).__init__(series)
        self.extra_create_kwargs["period"] = period


class AbsSeries(NumericSeries):
    def __init__(self, series):
        if isinstance(series, NumericSeries):
            series = series.series
            try:
                series[series == np.inf] = 0
                series[series == -np.inf] = 0
                series = np.abs(series)
            except Exception as e:
                raise FormulaException(e)
        super(AbsSeries, self).__init__(series)


@handle_numpy_warning
def CrossOver(s1, s2):
    """s1金叉s2
    :param s1:
    :param s2:
    :returns: bool序列
    :rtype: BoolSeries
    """
    s1, s2 = ensure_timeseries(s1), ensure_timeseries(s2)
    series1, series2 = fit_series(s1.series, s2.series)
    cond1 = series1 > series2
    series1, series2 = fit_series(s1[1].series, s2[1].series)
    cond2 = series1 <= series2  # s1[1].series <= s2[1].series
    cond1, cond2 = fit_series(cond1, cond2)
    s = cond1 & cond2
    return BoolSeries(s)


def Ref(s1, n):
    if isinstance(n, NumericSeries):
        return s1[int(n.value)]
    return s1[n]


@handle_numpy_warning
def minimum(s1, s2):
    s1, s2 = ensure_timeseries(s1), ensure_timeseries(s2)
    if len(s1) == 0 or len(s2) == 0:
        raise FormulaException("minimum size == 0")
    series1, series2 = fit_series(s1.series, s2.series)
    s = np.minimum(series1, series2)
    return NumericSeries(s)


@handle_numpy_warning
def maximum(s1, s2):
    s1, s2 = ensure_timeseries(s1), ensure_timeseries(s2)
    if len(s1) == 0 or len(s2) == 0:
        raise FormulaException("maximum size == 0")
    series1, series2 = fit_series(s1.series, s2.series)
    s = np.maximum(series1, series2)
    return NumericSeries(s)


@handle_numpy_warning
def count(cond, n):
    # TODO lazy compute
    series = cond.series
    size = len(cond.series) - n
    try:
        # result = np.full(size, 0, dtype=np.int)
        result = np.full(size, 0, dtype=int)
    except ValueError as e:
        raise FormulaException(e)
    for i in range(size - 1, 0, -1):
        s = series[-n:]
        result[i] = len(s[s == True])
        series = series[:-1]
    return NumericSeries(result)


@handle_numpy_warning
def every(cond, n):
    return count(cond, n) == n


@handle_numpy_warning
def hhv(s, n):
    # TODO lazy compute
    series = s.series
    size = len(s.series) - n
    try:
        # result = np.full(size, 0, dtype=np.float64)
        result = np.full(size, 0, dtype=float)
    except ValueError as e:
        raise FormulaException(e)

    result = np.max(rolling_window(series, n), 1)

    return NumericSeries(result)


@handle_numpy_warning
def llv(s, n):
    # TODO lazy compute
    series = s.series
    size = len(s.series) - n
    try:
        # result = np.full(size, 0, dtype=np.float64)
        result = np.full(size, 0, dtype=float)
    except ValueError as e:
        raise FormulaException(e)

    result = np.min(rolling_window(series, n), 1)

    return NumericSeries(result)


@handle_numpy_warning
def hhvbars(s, n):
    """HHVBARS 上一高点位置 求上一高点到当前的周期数.
    用法: HHVBARS(X,N):求N周期内X最高值到当前周期数,N=0表示从第一个有效值开始统计
    例如:HHVBARS(HIGH,0)求得历史新高到到当前的周期数
    """
    # TODO lazy compute
    series = s.series
    size = len(s.series) - n
    try:
        # result = np.full(size, 0, dtype=np.float64)
        result = np.full(size, 0, dtype=float)
    except ValueError as e:
        raise FormulaException(e)

    result = np.argmax(rolling_window(series, n), 1)

    return NumericSeries(result)


@handle_numpy_warning
def llvbars(s, n):
    """LLVBARS 上一低点位置 求上一低点到当前的周期数.
    用法: LLVBARS(X,N):求N周期内X最低值到当前周期数,N=0表示从第一个有效值开始统计
    例如:LLVBARS(LOW,20)求得20日最低点到当前的周期数
    """
    # TODO lazy compute
    series = s.series
    size = len(s.series) - n
    try:
        # result = np.full(size, 0, dtype=np.float64)
        result = np.full(size, 0, dtype=float)
    except ValueError as e:
        raise FormulaException(e)

    result = np.argmin(rolling_window(series, n), 1)

    return NumericSeries(result)


@handle_numpy_warning
def iif(condition, true_statement, false_statement):
    """IF 逻辑判断 根据条件求不同的值。
用法： IF(X，A，B) 若X不为0则返回A，否则返回B。
例如： IF(CLOSE>OPEN，HIGH，LOW)表示该周期收阳则返回最高值，否则返回最低值。
IFF 逻辑判断 根据条件求不同的值。
用法： IFF(X，A，B) 若X不为0则返回A，否则返回B。
例如： IFF(CLOSE>OPEN，HIGH，LOW) 表示该周期收阳则返回最高值，否则返回最低值。
"""
    series1 = get_series(true_statement)
    series2 = get_series(false_statement)
    cond_series, series1, series2 = fit_series(condition.series, series1, series2)

    series = series2.copy()
    series[cond_series] = series1[cond_series]

    return NumericSeries(series)


@handle_numpy_warning
def ceiling(s):
    """CEILING 向上舍入 向上舍入。 用法： CEILING(A) 返回沿A数值增大方向最接近的整数。
例如： CEILING(12.3) 求得13，CEILING(-3.5)求得-3。 FLOOR 向下舍入 向下舍入。 用法： FLOOR(A) 返回沿A数值减小方向最接近的整数。
"""
    series = s.series
    return NumericSeries(np.ceil(series))


@handle_numpy_warning
def const(s):
    if isinstance(s, NumericSeries):
        return NumericSeries(s.series)
    elif isinstance(s, np.ndarray):
        return NumericSeries(s)
    else:
        return NumericSeries(np.array([s]))


@handle_numpy_warning
def drawnull(s):
    """DRAWNULL 无效数 返回无效数。
用法： DRAWNULL
例如： IF(CLOSE>REF(CLOSE，1)，CLOSE，DRAWNULL) 表示下跌时分析图上不画线。 BACKSET 向前赋值
"""
    pass


@handle_numpy_warning
def zig(s, n):
    """ZIG 之字转向 之字转向。 用法： ZIG(K，N) 当价格变化量超过N%时转向，K表示0:开盘价，1:最高价， 2:最低价，3:收盘价，其余:数组信息
例如： ZIG(3，5) 表示收盘价的5%的ZIG转向。
"""
    series = s.series
    assert isinstance(series, np.ndarray)
    z, _ = zig_helper(series, n)
    return NumericSeries(z)


@handle_numpy_warning
def troughbars(s, n, m):
    """TROUGHBARS 波谷位置 前M个ZIG转向波谷到当前距离。
    用法： TROUGHBARS(K，N，M) 表 示之字转向ZIG(K，N)的前M个波谷到当前的周期数，M必须大于等于1。
    例如： TROUGH(2，5，2) 表示%5最低价ZIG转向的前2个波谷到当前的周期数。
    """
    series = s.series
    assert isinstance(series, np.ndarray)
    z, peers = zig_helper(series, n)
    z_in_p = [z[i] for i in peers]
    count = 0
    for i in range(len(z_in_p) - 1, 1, -1):
        if count == m:
            return i

        if z_in_p[i] < z_in_p[i - 1]:
            count += 1

    return 0


@handle_numpy_warning
def barslast(statement):
    """BARSLAST 上一条件成立位置 上一次条件成立到当前的周期数.
    用法: BARSLAST(X):上一次X不为0到现在的天数，
    例如:BARSLAST(CLOSE/REF(CLOSE,1)>=1.
    """
    series = get_series(statement)
    size = len(series)
    end = size
    begin = size - 1
    try:
        result = np.full(size, 1e16, dtype=int)
    except ValueError as e:
        raise FormulaException(e)

    for s in series[::-1]:
        if s:
            result[begin:end] = range(0, end - begin)
            end = begin
        begin -= 1

    return NumericSeries(result)
