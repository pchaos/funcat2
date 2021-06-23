# -*- coding: utf-8 -*-

import inspect
import datetime
import functools

import numpy as np
from .singletion import FuncCounter

__updated__ = "2021-06-23"


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


import numba


@numba.njit
def shift(arr: np.array, num: int=1, fill_value=np.nan):
    """Shift elements in a numpy array
    https://stackoverflow.com/questions/30399534/shift-elements-in-a-numpy-array
    """
    result = np.empty_like(arr)
    if num > 0:
        result[:num] = fill_value
        result[num:] = arr[:-num]
    elif num < 0:
        result[num:] = fill_value
        result[:num] = arr[-num:]
    else:
        result[:] = arr
    return result


def rolling_apply(fun, a, w):
    r = np.empty(a.shape)
    r.fill(np.nan)
    for i in range(w - 1, a.shape[0]):
        r[i] = fun(a[(i - w + 1):i + 1])
    return r


# @numba.njit
def rolling_sum(arr: np.array, n=4) -> np.array:
    pre_sum = np.convolve(arr, np.ones(n, dtype=int), 'valid')
    return np.append(np.array([np.nan] * (n - 1)), pre_sum)


def fft_denoiser(x, n_components, to_real=True):
    """Fast fourier transform denoiser.

    Denoises data using the fast fourier transform.

    Parameters
    ----------
    x : numpy.array
        The data to denoise.
    n_components : int
        The value above which the coefficients will be kept.
    to_real : bool, optional, default: True
        Whether to remove the complex part (True) or not (False)

    Returns
    -------
    clean_data : numpy.array
        The denoised data.

    References
    ----------
    .. [1] Steve Brunton - Denoising Data with FFT[Python]
       https://www.youtube.com/watch?v=s2K1JfNR7Sc&ab_channel=SteveBrunton
        https://medium.com/swlh/5-tips-for-working-with-time-series-in-python-d889109e676d
    """
    n = len(x)

    # compute the fft
    fft = np.fft.fft(x, n)

    # compute power spectrum density
    # squared magnitud of each fft coefficient
    PSD = fft * np.conj(fft) / n

    # keep high frequencies
    _mask = PSD > n_components
    fft = _mask * fft

    # inverse fourier transform
    clean_data = np.fft.ifft(fft)

    if to_real:
        clean_data = clean_data.real

    return clean_data


def getStringWithDecodedUnicode(value):
    """convert a dict to a unicode JSON string
    import re
    import json
    getStringWithDecodedUnicode = lambda str : re.sub( '\\\\u([\da-f]{4})', (lambda x : chr( int( x.group(1), 16 ) )), str )

    data = {"Japan":"日本"}
    jsonString = json.dumps( data )
    print( "json.dumps({0}) = {1}".format( data, jsonString ) )
    jsonString = getStringWithDecodedUnicode( jsonString )
    print( "Decoded Unicode: %s" % jsonString )

    Output
    json.dumps({'Japan': '日本'}) = {"Japan": "\u65e5\u672c"}
    Decoded Unicode: {"Japan": "日本"}
    """
    findUnicodeRE = re.compile('\\\\u([\da-f]{4})')

    def getParsedUnicode(x):
        return chr(int(x.group(1), 16))

    return findUnicodeRE.sub(getParsedUnicode, str(value))
