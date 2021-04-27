# -*- coding: utf-8 -*-
import unittest
from funcat import *
from funcat.api import *
from funcat.context import ExecutionContext


class TestFuncat2TestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        set_data_backend(QuantaxisDataBackend())
        cls.qdb = QuantaxisDataBackend()

    def test_select(self):
        # 选出涨停股
        data = select(
            lambda: C / C[1] - 1 >= 0.0995,
            start_date=20181231,
            end_date=20190104,
        )
        self.assertTrue(len(data) > 10, f"涨停股:{data}")

    def test_CLOSE(self):
        data_backend = ExecutionContext.get_data_backend()
        order_book_id_list = data_backend.get_order_book_id_list()[:300]
        # 选出涨停股
        data = select(
            lambda: C > 50,
            start_date=20181221,
            end_date=20190104,
            order_book_id_list=order_book_id_list
        )
        self.assertTrue(len(data) > 10, f"交易数据:{data}")

    def test_CLOSE_asyn(self):
        data_backend = ExecutionContext.get_data_backend()
        order_book_id_list = data_backend.get_order_book_id_list()[:150]
        # 选出涨停股
        data = selectAsync(
            lambda: C > 50,
            start_date=20181221,
            end_date=20190104,
            order_book_id_list=order_book_id_list
        )
        self.assertTrue(len(data) > 10, f"交易数据:{data}")

if __name__ == '__main__':
    unittest.main()
