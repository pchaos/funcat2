# -*- coding: utf-8 -*-
import unittest
from matplotlib import rcParams
import matplotlib.pyplot as plt
import numpy as np
import os
from functools import lru_cache
from funcat import *
from funcat.api import *
from funcat.helper import selectV
from funcat.utils import FuncatTestCase

__updated__ = "2021-06-17"


def condition_ema(n: int=13):
    return CLOSE >= EMA(CLOSE, n)


def condition_ema_ema(n: int=13, m: int=55):
    return (CLOSE > EMA(CLOSE, n)) & (CLOSE > EMA(CLOSE, m))


def condition_ema_ema2(n: int=13, m: int=55):
    return (CLOSE > EMA(CLOSE, n)) & (EMA(CLOSE, m) > REF(EMA(CLOSE, m), n))


def condition_kama_ema(n: int=10, m: int=21):
    return (CLOSE > KAMA(CLOSE, n)) & (EMA(CLOSE, m) > REF(EMA(CLOSE, m), n))


def condition_kama_ema2(n: int=10, m: float =0.1):
    kman = KAMA(CLOSE, n)
    amastd = STD(kman, 20)
    return (CLOSE > kman) & (CLOSE > kman + m * amastd)


class Test_ema_trend(FuncatTestCase):
    @classmethod
    def loadFromFile(cls):
        filename = "etf.txt"
        currDir = os.path.join(os.path.abspath(os.path.dirname(__file__)), ".")
        fullname = os.path.join(f"{currDir}", filename)
        print(fullname)
        if os.path.exists(fullname):
            with open(fullname, "r") as f:
                cls.codes = f.readlines()  # print(cls.codes[:10])
        for i, item in enumerate(cls.codes):
            cls.codes[i] = f"{ item[:6] }.etf"
        return cls.codes

    @classmethod
    def setUpClass(cls)->None:
        super(Test_ema_trend, cls).setUpClass()
        cls.codes = ['510500', '159915', '510300',
                     "512400", "512800", "512760", "515050"]
        for i, item in enumerate(cls.codes):
            cls.codes[i] = f"{ item[:6] }.etf"

    def show_last(self, arr: np.array, last_n=-1):
        from funcat import get_start_date, get_current_date, get_current_security
        from funcat.context import ExecutionContext
        current_date = get_current_date()
        start_date = current_date - 10000
        trading_dates = ExecutionContext.get_data_backend(
        ).get_trading_dates(start=start_date, end=current_date)
        lastday = trading_dates[last_n]
        result = []
        for i, item in enumerate(arr):
            if item['date'] == lastday:
                result.append(i)
        if arr.shape[0] > 0:
            return arr[result]
        else:
            return np.array([])

    def test_condition_ema(self):
        data = selectV(condition_ema,
                       start_date=20181228,
                       end_date=20190104,
                       order_book_id_list=self.codes)
        print(f"condition_ema results:{data}")

    def test_condition_ema_2(self):
        data = selectV(condition_ema,
                       start_date=20210101,
                       end_date=20210704,
                       order_book_id_list=self.codes)
        print(f"condition_ema results:{data}")

    def test_condition_ema_ema(self):
        data = selectV(condition_ema_ema,
                       start_date=20181001,
                       end_date=20190104,
                       order_book_id_list=self.codes)
        print(f"condition_ema_ema results:{data}")

    def test_condition_ema_ema2(self):
        data = selectV(condition_ema_ema,
                       start_date=20210101,
                       end_date=20210704,
                       order_book_id_list=self.codes)
        print(f"condition_ema_ema results:{data}")
        print(f"last day status:{self.show_last(data)}")

    def select_conditions(self, codes, last_n=-1, func=condition_ema_ema2):
        data = selectV(func, start_date=20210101,
                       end_date=20210704,
                       order_book_id_list=codes)
        print(f"condition_ema_ema results {len(data)}:{data}")
        print(f"total:{len(codes)} codes")
        if last_n != 0:
            print(
                f"last day status {self.show_last(data, last_n).shape[0]} :{self.show_last(data, last_n)}")
        return data

    def test_condition_ema_ema3(self):
        # 从本地文件读取etf代码列表
        codes = self.loadFromFile()
        self.select_conditions(codes)

    def test_condition_ema_ema3_2(self):
        # 从本地文件读取etf代码列表
        codes = self.loadFromFile()
        self.select_conditions(codes)
        self.select_conditions(codes, last_n=-2)

    def test_condition_ema_ema3_3(self):
        # 从本地文件读取etf代码列表
        codes = self.loadFromFile()
        self.select_conditions(codes)
        data = self.select_conditions(codes)
        n = 10
        for i in range(n):
            x = self.show_last(data, -i - 1)
            print(x)
            filename = f"/tmp/outfile{i}.txt"
            np.savetxt(filename, x, fmt=['%s'])
            print(f"save to {filename}")

    def test_condition_ema_ema4(self):
        codes = ["501078.etf"]
        # codes = ["588000.etf"]
        self.select_conditions(codes)

    def test_condition_ema_ema5(self):
        # 从本地文件读取etf代码列表
        codes = self.loadFromFile()
        data = self.select_conditions(codes)
        lastdata = self.show_last(data)
        lastcodes = []
        for i, item in enumerate(lastdata):
            lastcodes.append(item['code'])
        n = 13
        result = []
        if len(lastcodes) > 0:
            for i, item in enumerate(lastcodes):
                S(item)
                try:
                    c = CLOSE / REF(CLOSE, n)
                    result.append([item, np.round(c.value, 3)])
                except Exception as e:
                    print(f"{item}计算错误！")
        print(f"percent:{result}")
        result = np.array(result)
        print(f"percent {result.shape}:{np.array(result)}")

    def test_condition_kama_ema(self):
        # 从本地文件读取etf代码列表
        codes = self.loadFromFile()
        data = self.select_conditions(codes, func=condition_kama_ema)
        lastdata = self.show_last(data)
        lastcodes = []
        for i, item in enumerate(lastdata):
            lastcodes.append(item['code'])
        n = 13
        result = []
        if len(lastcodes) > 0:
            for i, item in enumerate(lastcodes):
                S(item)
                try:
                    c = CLOSE / REF(CLOSE, n)
                    result.append([item, np.round(c.value, 3)])
                except Exception as e:
                    print(f"{item}计算错误！")
        print(f"percent:{result}")
        result = np.array(result)
        print(f"percent {result.shape}:{np.array(result)}")

    def show_result(self, codes, n):
        result = []
        if len(codes) > 0:
            for i, item in enumerate(codes):
                S(item)
                try:
                    c = CLOSE / REF(CLOSE, n)
                    result.append((item, np.round(c.value, 3)))
                except Exception as e:
                    print(f"{item}计算错误！")

        print(f"percent:{result}")
        dtype = [('code', 'S10'), ('percent', float)]
        result_np = np.array(result, dtype=dtype)
        # print(f"percent numpy: {result_np.shape}:{result_np}")
        sorted_result = np.sort(result_np, order='percent')
        print(
            f"percent ordered: {sorted_result.shape}:{sorted_result}")

    def test_condition_kama_ema2(self):
        # 从本地文件读取etf代码列表
        codes = self.loadFromFile()
        data = self.select_conditions(codes, func=condition_kama_ema2)
        lastdata = self.show_last(data)
        lastcodes = []
        for i, item in enumerate(lastdata):
            lastcodes.append(item['code'])
        n = 10
        self.show_result(lastcodes, n)
        n = 5
        self.show_result(lastcodes, n)


if __name__ == '__main__':
    FuncatTestCase.main()
