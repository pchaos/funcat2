# -*- coding: utf-8 -*-
import unittest
from funcat.utils import *
from funcat.api import *

class TestUtils(unittest.TestCase):
    def test_get_str_date_from_int(self):
        data = get_str_date_from_int(20210101)
        self.assertTrue(data == '2021-01-01')
        data = get_str_date_from_int(20211011)
        self.assertTrue(data == '2021-10-11')

    def test_get_str_date_from_int(self):
        data = MA(CLOSE, 5)
        data2 = EMA(CLOSE, 5)
        print(FuncCounter.instance().get("get_bars"))

if __name__ == '__main__':
    unittest.main()
