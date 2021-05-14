# -*- coding: utf-8 -*-

import inspect
import datetime
import functools

import numpy as np
from .singletion import FuncCounter


class FormulaException(Exception):
    pass


def wrap_formula_exc(func):

    def wrapper(*args, **kwargs):
        try:
            # print(func, args, kwargs)
            return func(*args, **kwargs)
        except (ValueError, IndexError) as e:
            raise FormulaException(e)

    return wrapper


def getsourcelines(func):
    try:
        source_code = "".join(inspect.getsourcelines(func)[0]).strip()
        return source_code
    except:
        return ""


def get_int_date(date):
    if isinstance(date, int) or isinstance(date, np.int64):
        if date < 15000000 or date > 99990000:
            # 日期格式错误 公园1500～9999年
            raise Exception(f"date format error:{date}")
        return date

    try:
        if len(date) == 19:
            return int(datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S").strftime("%Y%m%d%H%M%S"))
        elif len(date) == 10:
            return int(datetime.datetime.strptime(date, "%Y-%m-%d").strftime("%Y%m%d"))
        elif len(date) == 14:
            return int(datetime.datetime.strptime(date, "%Y%m%d%H%M%S").strftime("%Y%m%d%H%M%S"))
    except:
        pass

    try:
        if len(date) != 8:
            return int(datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S").strftime("%Y%m%d%H%M%S"))
        else:
            return int(datetime.datetime.strptime(date, "%Y%m%d").strftime("%Y%m%d"))
    except:
        pass

    if isinstance(date, (datetime.date)):
        return int(date.strftime("%Y%m%d"))

    raise ValueError(f"unknown date {date}, type {type(date)}")


def get_str_date_from_int(date_int):
    try:
        date_int = int(date_int)
    except ValueError:
        date_int = int(date_int.replace("-", ""))
    year = date_int // 10000
    month = (date_int % 10000) // 100
    day = date_int % 100
    return f"{year:d}-{month:02d}-{day:02d}"


def get_date_from_int(date_int):
    date_str = get_str_date_from_int(date_int)

    return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()


def rolling_window(a, window):
    '''
    copy from http://stackoverflow.com/questions/6811183/rolling-window-for-1d-arrays-in-numpy
    '''
    shape = a.shape[:-1] + (a.shape[-1] - window + 1, window)
    strides = a.strides + (a.strides[-1],)
    return np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)


def handle_numpy_warning(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        with np.errstate(invalid='ignore'):
            return func(*args, **kwargs)

    return wrapper


from functools import wraps


def func_counter(func):
    """function执行次数记数
    """

    @wraps(func)
    def wrapped_f(*args, **kwargs):
        FuncCounter.instance().update(func.__name__)
        return func(*args, **kwargs)

    return wrapped_f
