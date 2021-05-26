# -*- coding: utf-8 -*-

import datetime
import numpy as np
import asyncio
from tqdm.asyncio import tqdm

from .context import ExecutionContext, set_current_security, set_current_date, symbol, set_start_date, \
    get_current_security
from .utils import getsourcelines, FormulaException, get_int_date

__all__ = ["select",
           "select2",
           "selectAsync",
           "suppress_numpy_warn",
           "backtest",
           "zig_helper",
           ]


def suppress_numpy_warn(func):

    def wrapper(*args, **kwargs):
        try:
            old_settings = np.seterr(all='ignore')
            return func(*args, **kwargs)
        finally:
            np.seterr(**old_settings)  # reset to default

    return wrapper


def choose(order_book_id, func, callback):
    set_current_security(order_book_id)
    try:
        if func():
            date = ExecutionContext.get_current_date()
            callback(date, order_book_id, symbol(order_book_id))
            return {"date": get_int_date(date), "code": order_book_id, "cname": symbol(order_book_id)}
    except FormulaException as e:
        pass
    return {}


def _list2Array(alist: list):
    arr = np.asarray(alist)
    return arr[arr != {}]


@suppress_numpy_warn
def selectAsync(func, start_date="2016-10-01", end_date=None, callback=print, order_book_id_list=[]) -> np.array:
    """异步select"""

    async def achoose(order_book_id_list, func, callback):
        with tqdm(range(len(order_book_id_list))) as pbar:
            async for i in pbar:
                order_book_id = order_book_id_list[i]
                results.append(choose(order_book_id, func, callback))
                if not (i % 10 == 0):
                    # pbar.update(5)
                    pbar.set_description(f"{i}, {order_book_id}")

    print(getsourcelines(func))
    results = []
    start_date = get_int_date(start_date)
    if end_date is None:
        end_date = datetime.date.today()
    end_date = get_int_date(end_date)
    data_backend = ExecutionContext.get_data_backend()
    if len(order_book_id_list) == 0:
        order_book_id_list = data_backend.get_order_book_id_list()
    trading_dates = data_backend.get_trading_dates(start=start_date, end=end_date)
    set_start_date(trading_dates[0] - 10000)  # 提前一年的数据
    loop = asyncio.get_event_loop()
    for idx, date in enumerate(reversed(trading_dates)):
        if end_date and date > get_int_date(end_date):
            continue
        if date < get_int_date(start_date):
            break
        set_current_date(str(date))
        print(f"Dealing [{date}]")

        loop.run_until_complete(achoose(order_book_id_list, func, callback))
    loop.close()
    print("")
    return _list2Array(results)


@suppress_numpy_warn
def select2(func, start_date="2016-10-01", end_date=None, callback=print, order_book_id_list=[]) -> np.array:
    """not done"""
    from numba.typed import List

    # @njit()
    def achoose(order_book_id_list, func, callback):
        for i in range(len(order_book_id_list)):
            order_book_id = order_book_id_list[i]
            set_current_security(order_book_id)
            results.append(choose(order_book_id, func, callback))

            if not (i % 5):
                # pbar.update(5)
                # print(f"{i}", end=" ")
                pass

    print(getsourcelines(func))
    results = []
    start_date = get_int_date(start_date)
    if end_date is None:
        end_date = datetime.date.today()
    end_date = get_int_date(end_date)
    data_backend = ExecutionContext.get_data_backend()
    if len(order_book_id_list) == 0:
        order_book_id_list = data_backend.get_order_book_id_list()
    trading_dates = data_backend.get_trading_dates(start=start_date, end=end_date)
    set_start_date(trading_dates[0] - 10000)
    for idx, date in enumerate(reversed(trading_dates)):
        if end_date and date > get_int_date(end_date):
            continue
        if date < get_int_date(start_date):
            break
        set_current_date(str(date))
        print(f"Dealing [{date}]")
        iddic = {i: order_book_id_list[i] for i in range(0, len(order_book_id_list))}
        achoose(iddic, func, callback)
    print("")
    return _list2Array(results)


@suppress_numpy_warn
def select(func, start_date="2016-10-01", end_date=None, callback=print, order_book_id_list=[]) -> np.array:
    result = []
    print(getsourcelines(func))
    start_date = get_int_date(start_date)
    if end_date is None:
        end_date = datetime.date.today()
    end_date = get_int_date(end_date)
    data_backend = ExecutionContext.get_data_backend()
    if len(order_book_id_list) == 0:
        order_book_id_list = data_backend.get_order_book_id_list()
    trading_dates = data_backend.get_trading_dates(start=start_date, end=end_date)
    set_start_date(trading_dates[0] - 10000)
    for idx, date in enumerate(reversed(trading_dates)):
        if end_date and date > get_int_date(end_date):
            continue
        if date < get_int_date(start_date):
            # 日期小于开始日期则计算完成
            break
        set_current_date(str(date))
        print(f"[{date}]")

        order_book_id_list = tqdm(order_book_id_list)
        for order_book_id in order_book_id_list:
            result.append(choose(order_book_id, func, callback))
            order_book_id_list.set_description("Processing {}".format(order_book_id))
    print("")
    return _list2Array(result)


@suppress_numpy_warn
def selectV(func, start_date="2016-10-01", end_date=None, callback=print, order_book_id_list=[]) -> np.array:
    """条件选股
    Args:
        func (function): 选股条件
        start_date: 选股开始时间
        end_date: 选股截止时间（默认为当天）
        callback：回调函数（默认为print）
        order_book_id_list: 选股范围（默认为所有股票，不包含指数、基金）
    Returns:
        返回符合条件的数组（时间，代码，中文名 --- np.array[date, code, symbol]）
        """

    def choose(order_book_id, func, callback):
        """返回func返回True的数据"""
        set_current_security(order_book_id)
        try:
            flag = func()
            data_backend = ExecutionContext.get_data_backend()
            dates = data_backend.get_trading_dates(start_date, end_date, order_book_id)
            real_length = min(len(flag), len(dates))
            flag_true = flag.series[-real_length:][flag.series[-real_length:]]
            # if real_length > 0 and len(flag_true) > 0:
            if len(flag_true) > 0:
                return zip(flag_true, np.array(dates, dtype=int)[-real_length:][flag.series[-real_length:]])
            else:
                return zip()
            # callback(date, order_book_id, symbol(order_book_id))
            # return {"date": get_int_date(date), "code": order_book_id, "cname": symbol(order_book_id)}
        except FormulaException as e:
            pass
        return zip()

    result = []
    print(getsourcelines(func))
    start_date = get_int_date(start_date)
    if end_date is None:
        end_date = datetime.date.today()
    end_date = get_int_date(end_date)
    data_backend = ExecutionContext.get_data_backend()
    if len(order_book_id_list) == 0:
        order_book_id_list = data_backend.get_order_book_id_list()
    trading_dates = data_backend.get_trading_dates(start=start_date, end=end_date)
    set_start_date(trading_dates[0] - 10000)
    set_current_date(str(trading_dates[-1]))
    for code in tqdm(order_book_id_list):
        # print(f"[{code}];", end="")
        for flag, date in tuple(choose(code, func, callback)):
            callback(code, flag, date)
            result.append({"date": get_int_date(date), "code": code, "cname": symbol(code)})
    print("")
    return _list2Array(result)


@suppress_numpy_warn
def backtest(func_buy, func_sell, func_update, account, start_date="2016-10-01", end_date=None, callback=print):
    start_date = get_int_date(start_date)
    if end_date is None:
        end_date = datetime.date.today()
    end_date = get_int_date(end_date)
    date_backend = ExecutionContext.get_data_backend()
    trading_dates = date_backend.get_trading_dates(start=start_date, end=end_date)
    for idx, date in enumerate(trading_dates):
        if get_int_date(date) < start_date:
            continue
        if get_int_date(date) > end_date:
            break
        set_current_date(date)
        if account.position_num == 0:
            func_buy(account)
            if account.position_num != 0:
                continue

        if account.position_num != 0:
            func_sell(account)

        func_update(account)

    print('[{}]'.format(account.value))


def zig_helper(series, n):
    i = 0
    start = 0
    rise = 1
    fall = 2
    candidate_i = None
    peers = [0]
    peer_i = 0
    curr_state = start
    z = np.zeros(len(series))
    if len(series) <= n:
        return z, peers
    while True:
        i += 1
        if i == series.size - 1:
            if candidate_i is None:
                peer_i = i
                peers.append(peer_i)
            else:
                if curr_state == rise:
                    if series[n] >= series[candidate_i]:
                        peer_i = i
                        peers.append(peer_i)
                    else:
                        peer_i = candidate_i
                        peers.append(peer_i)
                        peer_i = i
                        peers.append(peer_i)
                elif curr_state == fall:
                    if series[i] <= series[candidate_i]:
                        peer_i = i
                        peers.append(peer_i)
                    else:
                        peer_i = candidate_i
                        peers.append(peer_i)
                        peer_i = i
                        peers.append(peer_i)
            break

        if curr_state == start:
            if series[i] >= series[peer_i] * (1.0 + n / 100.0):
                candidate_i = i
                curr_state = rise
            elif series[i] <= series[peer_i] * (1.0 - n / 100.0):
                candidate_i = i
                curr_state = fall
        elif curr_state == rise:
            if series[i] >= series[candidate_i]:
                candidate_i = i
            elif series[i] <= series[candidate_i] * (1.0 - n / 100.0):
                peer_i = candidate_i
                peers.append(peer_i)
                curr_state = fall
                candidate_i = i
        elif curr_state == fall:
            if series[i] <= series[candidate_i]:
                candidate_i = i
            elif series[i] >= series[candidate_i] * (1.0 + n / 100.0):
                peer_i = candidate_i
                peers.append(peer_i)
                curr_state = rise
                candidate_i = i
    for i in range(len(peers) - 1):
        peer_start_i = peers[i]
        peer_end_i = peers[i + 1]
        start_value = series[peer_start_i]
        end_value = series[peer_end_i]
        a = (end_value - start_value) / (peer_end_i - peer_start_i)
        for j in range(peer_end_i - peer_start_i + 1):
            z[j + peer_start_i] = start_value + a * j

    return z, peers
