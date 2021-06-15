# -*- coding: utf-8 -*-
import unittest
from matplotlib import rcParams
import matplotlib.pyplot as plt
import numpy as np
from funcat import *
from funcat.api import *
from funcat.helper import selectV
from funcat.utils import FuncatTestCase

__updated__ = "2021-06-15"


def condition_ema(n: int=13):
    return CLOSE >= EMA(CLOSE, n)


def condition_ema_ema(n: int=13, m: int=55):
    return (CLOSE > EMA(CLOSE, n)) & (CLOSE > EMA(CLOSE, m))


class Test_ema_trend(FuncatTestCase):
    @classmethod
    def setUpClass(cls)->None:
        super(Test_ema_trend, cls).setUpClass()
        cls.codes = ['510500', '159915', '510300']
        for i, item in enumerate(cls.codes):
            cls.codes[i] = f"{item}.etf"

    def test_condition_ema(self):
        data = selectV(condition_ema,
                       start_date=20181228,
                       end_date=20190104,
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


if __name__ == '__main__':
    FuncatTestCase.main()
