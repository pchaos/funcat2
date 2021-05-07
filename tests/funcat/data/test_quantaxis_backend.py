# -*- coding: utf-8 -*-
import unittest
from funcat import *


class TestQuantaxisDataBackend(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        set_data_backend(QuantaxisDataBackend())
        cls.qdb = QuantaxisDataBackend()

    def test_stock_basics(self):
        data = self.qdb.stock_basics
        self.assertTrue(len(data) > 3500, f"股票代码数量：{len(data)},实际数量应该大于3500只。")

    def test_get_price(self):
        data = self.qdb.get_price("000001", 20210101, 20210201, '1d')
        self.assertTrue(len(data) > 10, f"交易日期数量：{len(data)},实际应该大于10天。")
        print(data)
        # index
        data = self.qdb.get_price("000001", 20210101, 20210201, '1d', is_index=True)
        self.assertTrue(len(data) > 10, f"交易日期数量：{len(data)},实际应该大于10天。")
        print(data)

    def test_get_price2(self):
        """和tushare返回的数据做比对"""
        # index
        data = self.qdb.get_price("000001", 20210101, 20210201, '1d', is_index=True)
        self.assertTrue(len(data) > 10, f"交易日期数量：{len(data)},实际应该大于10天。")
        print(data[-9:])
        from funcat.data.tushare_backend import TushareDataBackend as backend
        # from funcat.data.quantaxis_backend import QuantaxisDataBackend as backend
        set_data_backend(backend())
        tsb = backend()
        data2 = tsb.get_price("000001.XSHG", 20210101, 20210201, '1d')
        self.assertTrue(len(data2) > 10, f"交易日期数量：{len(data2)},实际应该大于10天。")
        print(data2[-9:])
        self.assertTrue(len(data[0]) == len(data2[0]), f"{data[0]}== {data2[0]}")
        # quantaxis getprice字段：Index(['date', 'open', 'close', 'high', 'low', 'volume', 'datetime'], dtype='object')
        for i in range(len(data)):
            for j in range(len(data[0])):
                if j == 6:
                    # quantaxis、tushare vol字段单位不同，，不能直接比较
                    continue
                self.assertTrue(data[i][j] == data2[i][j], f"{data[i]}== {data2[i]}")

    def test_get_order_book_id_list(self):
        data = self.qdb.get_order_book_id_list()
        self.assertTrue(len(data) > 3500, f"股票代码数量：{len(data)},实际数量应该大于3500只。")
    def test_get_order_book_id_list2(self):
        data = self.qdb.get_order_book_id_list()
        self.assertTrue(len(data) > 3500, f"股票代码数量：{len(data)},实际数量应该大于3500只。")

    def test_get_trading_dates(self):
        data = self.qdb.get_trading_dates(20200101, 20210301)
        self.assertTrue(len(data) > 250, f"交易日期数量：{len(data)},实际应该大于250天。")
        print(f"交易日期：{data}")

        data2 = self.qdb.get_trading_dates(20200101, 20210401)
        self.assertTrue(len(data2) > len(data), f"交易日期数量：{len(data)}， {len(data2)},实际天数应该大于前一个交易天数")

    def test_freq(self):
        print(f"freq: '{get_current_freq()}' {get_current_date()}, {get_current_security()}")
        set_current_freq("1d")
        c1 = CLOSE
        lc1 = len(c1.series)
        print(f"day :{lc1}")
        set_current_freq("W")
        c2 = CLOSE
        lc2 = len(c2)
        print(f"week :{lc2}")
        self.assertTrue(lc1 > lc2, f"日线数据比周线数据多：{lc1}, {lc2};{get_start_date()} - {get_current_date()}")

    def test_freq2(self):
        """赋值的时候没有获取实际值。"""
        from copy import deepcopy
        print(f"freq: '{get_current_freq()}' {get_current_date()}, {get_current_security()}")
        set_current_freq("1d")
        c1 = deepcopy(CLOSE)
        set_current_freq("W")
        c2 = CLOSE
        lc2 = len(c2)
        print(f"week :{lc2}")
        lc1 = len(c1)
        self.assertTrue(lc1 == lc2, f"日线数据比周线数据多：{lc1}, {lc2};{get_start_date()} - {get_current_date()}")

    def test_week_trends(self):
        pass


if __name__ == '__main__':
    unittest.main()
