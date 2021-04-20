# -*- coding: utf-8 -*-
import unittest
from unittest import TestCase
from funcat import *
from funcat.data.quantaxis_backend import QuantaxisDataBackend as QDB


class TestQuantaxisDataBackend(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        set_data_backend(QuantaxisDataBackend())
        cls.qdb = QDB()

    def test_stock_basics(self):
        T("20161216")
        S("000001.XSHG")
        sb = self.qdb.stock_basics
        self.assertTrue(len(sb) > 3000, f"股票代码数量：{len(sb)},实际数量应该大于3000只。")

    def test_get_order_book_id_list(self):
        sb = self.qdb.get_order_book_id_list()
        self.assertTrue(len(sb) > 3000, f"股票代码数量：{len(sb)},实际数量应该大于3000只。")


if __name__ == '__main__':
    unittest.main()
