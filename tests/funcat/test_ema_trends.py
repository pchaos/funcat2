# -*- coding: utf-8 -*-
import unittest
from matplotlib import rcParams
import matplotlib.pyplot as plt
import numpy as np
import os
from functools import lru_cache
import json
from funcat import *
from funcat.api import *
from funcat.helper import selectV
from funcat.utils import FuncatTestCase

__updated__ = "2021-06-24"


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
        filename = "../datas/etf.txt"
        currDir = os.path.join(os.path.abspath(os.path.dirname(__file__)), ".")
        fullname = os.path.join(f"{currDir}", filename)
        print(fullname)
        if os.path.exists(fullname):
            with open(fullname, "r") as f:
                cls.codes = f.readlines()  # print(cls.codes[:10])
        for i, item in enumerate(cls.codes):
            cls.codes[i] = f"{ item[:6] }.etf"
            if cls.codes[i].startswith("000"):
                # 指数替换
                cls.codes[i] = "588000.etf"
        if cls.codes[0].startswith("代码"):
            print(f"del 代码")
            del cls.codes[0]
        for i in reversed(range(len(cls.codes))):
            # 删除空行
            if (len(cls.codes[i].strip()) != 10):
                del cls.codes[i]
        return cls.codes

    @classmethod
    def setUpClass(cls)->None:
        super(Test_ema_trend, cls).setUpClass()
        cls.codes = ['510500', '159915', '510300',
                     "512400", "512800", "512760", "515050"]
        for i, item in enumerate(cls.codes):
            cls.codes[i] = f"{ item[:6] }.etf"

    def sort_arr(self, arr: np.array, sort=''):
        result = []
        for i, item in enumerate(arr):
            try:
                result.append(
                    (item['date'], item['code'], item['cname']))
            except Exception as e:
                print(f"{item}计算错误！")

        # print(f"percent:{result}")
        # dtype = [(('date', int), ('code', 'U'), ('cname', 'U'))]
        dtype = [('date', int), ('code', (np.str_, 10)),
                 ('cname', (np.str_, 10))]
        arr_sorted = np.array(result, dtype=dtype)
        return np.sort(arr_sorted, order='code')

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
            return self.sort_arr(arr[result])
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
        """站上13日ema 并且ema55向上"""
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
            l
            astcodes.append(item['code'])
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

    def show_result(self, codes, n, topn=5):
        result = []
        if len(codes) > 0:
            for i, item in enumerate(codes):
                S(item)
                try:
                    c = CLOSE / REF(CLOSE, n)
                    result.append((item, np.round(100 * c.value, 2)))
                except Exception as e:
                    print(f"{item}计算错误！")

        # print(f"percent:{result}")
        dtype = [('code', 'S10'), ('percent', float)]
        result_np = np.array(result, dtype=dtype)
        # print(f"percent numpy: {result_np.shape}:{result_np}")
        sorted_result = np.sort(result_np, order='percent')
        print(
            f"{n} day percent ordered %: {sorted_result.shape}:{sorted_result}")
        # sorted_result.tofile('/tmp/kama.csv', sep=',')
        jsfile = f"/tmp/kama{n}.json"
        # calculate row and column numbers
        row_count = sorted_result.shape[0]
        # neglect first row and get new row numbers
        row_count = row_count - 1
        npMatrix = sorted_result.transpose()
        # transfer numpy array to list
        matrix = npMatrix.tolist()
        # transfer list to that JSON file
        result = {}

        for index, item in enumerate(matrix):
            if index + topn > row_count:
                result[item[0].decode()] = item[1]
        return {f"{n} day (CLOSE/REF(CLOSE, {n}) percent %)": result}

    def dict_to_json(self, value):
        # When parsing JSON anything can go wrong
        # So we need to handle exceptions. For example
        # If the JSON fails validation, the exception
        # is triggered
        try:
            # Load JSON data from a string to Python object
            if isinstance(value, str):
                o_json = json.loads(value)
            elif isinstance(value, dict):
                o_json = value
            elif isinstance(value, list):
                o_json = value
            # Convert the JSON Python object back to string
            # Also format it in a nice way. That is what
            # this article is all about. The indent parameter
            # specifies the width of the indentation which is
            # self explanatory. The sorted_keys parameter
            # specifies if we want to keep the input JSON
            # as is or sort the key. In this case we are not
            f_json = json.dumps(
                o_json, indent=2, sort_keys=False, ensure_ascii=False)

            # Print the beautified JSON
            # print(f_json)
            return f_json
        # Catch any exceptions
        except Exception as ex:
            # repr is used to print more information about
            # the object which is handy when debugging
            print(repr(ex))
        return json.dumps({})

    def test_condition_kama_ema2(self):
        """kman=10日卡夫曼自适应均线，
        close > kamn 并且 close > kamn+0.1×STD(kman, 20)
        """
        # 从本地文件读取etf代码列表
        codes = self.loadFromFile()
        data = self.select_conditions(codes, func=condition_kama_ema2)
        lastdata = self.show_last(data)
        lastcodes = []
        for i, item in enumerate(lastdata):
            lastcodes.append(item['code'])
        # 与n天前的比值
        n = 10
        j1 = self.show_result(lastcodes, n)
        n = 5
        j2 = self.show_result(lastcodes, n)
        # print(j1, j2)
        print(self.dict_to_json([j1, j2]))
        print(f"{len(lastdata)}/{len(codes)},{lastdata}")
        if len(lastdata) > 0:
            with open(f"/tmp/kama_ema_{lastdata[0]['date']}.txt", 'w') as f:
                f.write(f"{lastdata[0]['date']}\n" + f"""kman=10日卡夫曼自适应均线，\n close > kamn 并且 close > kamn+0.1×STD(kman, 20)\n""" + f"备选etf：\n{codes}\n" +
                        f"{str(self.dict_to_json([j1, j2]))}\n{len(lastdata)}/{len(codes)},{lastdata}\n")
        # print(self.dict_to_json(list(enumerate(lastdata))))

    def test_condition_kama_ema3(self):
        """kman=10日卡夫曼自适应均线，
        close > kamn 并且 close > kamn+0.1×STD(kman, 20)
        """
        # 从本地文件读取etf代码列表
        codes = self.loadFromFile()
        data = self.select_conditions(codes, func=condition_kama_ema2)
        lastdata = self.show_last(data)
        lastcodes = []
        for i, item in enumerate(lastdata):
            lastcodes.append(item['code'])
        # 与n天前的比值
        nlist = [5, 10, 20]
        jlist = []
        for n in nlist:
            j1 = self.show_result(lastcodes, n)
            jlist.append(j1)
        # print(j1, j2)
        print(self.dict_to_json(jlist))
        print(f"{len(lastdata)}/{len(codes)},{lastdata}")
        # code出现的次数
        codes_count = {}
        for item_dict in jlist:
            print(item_dict)
            for item in item_dict.values():
                for key in item.keys():
                    codes_count[key] = codes_count.get(key, 0) + 1
        codes_count = {"排名靠前出现的次数": codes_count}
        if len(lastdata) > 0:
            with open(f"/tmp/kama_ema_{lastdata[0]['date']}.txt", 'w') as f:
                f.write(f"{lastdata[0]['date']}\n" +
                        f"""kman=10日卡夫曼自适应均线，\n close > kamn 并且 close > kamn+0.1×STD(kman, 20)\n""" +
                        f"标的etf：\n{codes}\n" +
                        f"{str(self.dict_to_json(jlist))}\n" +
                        f"{self.dict_to_json(codes_count)}\n" +
                        f"{len(lastdata)}/{len(codes)},{lastdata}\n")


if __name__ == '__main__':
    FuncatTestCase.main()
