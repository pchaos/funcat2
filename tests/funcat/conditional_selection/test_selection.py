# -*- coding: utf-8 -*-
import unittest

import numpy as np

from funcat.api import *
from funcat.utils import MyTestCase


# from funcat.context import ExecutionContext


class TestSelection(MyTestCase):
    @classmethod
    def setUp(cls) -> None:
        T("20201216")
        S("000001.XSHG")

    def test_bit_and(self):
        S("601636")
        T("20210506")
        start_date = 20210414
        set_start_date(start_date)
        DAYS = 3
        COND1 = (REF(C, DAYS - 1) / REF(C, DAYS) - 1)
        COND2 = (REF(C, DAYS - 2) / REF(C, DAYS - 1) - 1)
        COND3 = (REF(C, DAYS - 3) / REF(C, DAYS - 2) - 1)
        print(CLOSE.series)
        for i in range(1, DAYS + 1):
            print(DAYS - i, REF(CLOSE, DAYS - i).series[-10:])
        print((COND2 > COND1).series)
        print((COND3 > COND2).series)
        a = COND3 > COND2 & COND2 > COND1
        print("A, COND3 > COND2 & COND2 > COND1\n", a.series)
        b = COND3 > COND2 and COND2 > COND1
        print("B, COND3 > COND2 and COND2 > COND1\n", b.series)
        c = (COND3 > COND2) & (COND2 > COND1)
        print(f"只有这个是正确的\n", c.series)
        for i in range(1, len(b)):
            if b[i] != c[i]:
                print(f"数据不同步:-{i}, {b[i]} != {c[i]}")

    def test_hong_san_bing(self):
        # fakeData = self.fakeMarketData()
        data = HSB()
        # print(hsb.series)
        self.assertTrue(len(data) > 0)

    def test_hong_san_bing2(self):
        # 旗滨集团 四月底～五月初有三红兵
        S("601636")
        T("20210506")
        start_date = 20210401
        set_start_date(start_date)
        data = HSB()
        print(data.series)
        print(CLOSE.series)
        print((CLOSE / REF(CLOSE, 1)).series)
        print((VOL / REF(VOL, 1)).series)
        self.assertTrue(len(data) > 0)
        print(data.series)

    def test_hong_san_bing_select(self):
        # order_book_id_list = self.BE.get_order_book_id_list()[300:1500]
        order_book_id_list = self.BE.get_order_book_id_list()[3000:4000]
        # order_book_id_list = self.BE.get_order_book_id_list()
        # 选出涨停股
        data = select(HSB,
                      start_date=20210426,
                      end_date=20210506,
                      order_book_id_list=order_book_id_list)
        self.assertTrue(len(data) > 0, f"交易数据:{data}")
        print(data)


if __name__ == '__main__':
    unittest.main()
