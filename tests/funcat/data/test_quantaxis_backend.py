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
        self.assertTrue(len(data) > 250, f"股票代码数量：{len(data)},实际数量应该大于3000只。")
        print(f"交易日期：{data}")


if __name__ == '__main__':
    unittest.main()
