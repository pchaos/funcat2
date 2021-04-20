# -*- coding: utf-8 -*-
import unittest
from unittest import TestCase
from funcat import *


class TestQuantaxisDataBackend(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        set_data_backend(QuantaxisDataBackend())
        cls.qdb = QuantaxisDataBackend()

    def test_stock_basics(self):
        T("20161216")
        S("000001.XSHG")
        data = self.qdb.stock_basics
        self.assertTrue(len(data) > 3000, f"股票代码数量：{len(data)},实际数量应该大于3000只。")

    def test_get_order_book_id_list(self):
        data = self.qdb.get_order_book_id_list()
        self.assertTrue(len(data) > 3000, f"股票代码数量：{len(data)},实际数量应该大于3000只。")

    def test_get_trading_dates(self):
        data = self.qdb.get_trading_dates(20200101, 20210301)
        self.assertTrue(len(data) > 250, f"交易日期数量：{len(data)},实际应该大于250天。")
        print(f"交易日期：{data}")

        data2 = self.qdb.get_trading_dates(20200101, 20210401)
        self.assertTrue(len(data2) > len(data), f"交易日期数量：{len(data)}， {len(data2)},实际天数应该大于前一个交易天数")



if __name__ == '__main__':
    unittest.main()
