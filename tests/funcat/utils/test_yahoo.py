# -*- coding: utf-8 -*-

import unittest
import warnings
from funcat.utils import save_sp500_tickers, get_data_from_yahoo

__updated__ = "2021-08-10"


class TestYahoo(unittest.TestCase):

    """Test case docstring."""

    @classmethod
    def setUpClass(cls):
        super(TestYahoo, cls).setUpClass()
        # 隐藏warning： ResourceWarning: Enable tracemalloc to get the object
        # allocation traceback
        warnings.simplefilter('ignore', ResourceWarning)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_save_sp500_tickers(self):
        sp500 = save_sp500_tickers()
        self.assertTrue(len(sp500) >= 500,
                        f"返回长度不够{len(sp500)=}\n： {sp500=}")
        print(f"{len(sp500)=}, {sp500=}")

    def test_get_data_from_yahoo(self):
        get_data_from_yahoo()


if __name__ == "__main__":
    unittest.main()
