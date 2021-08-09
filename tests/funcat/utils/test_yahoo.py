# -*- coding: utf-8 -*-

import unittest
from funcat.utils import save_sp500_tickers

class TestYahoo(unittest.TestCase):

    """Test case docstring."""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_name(self):
        pass

    def test_save_sp500_tickers(self):
        sp500 = save_sp500_tickers()
        print(sp500)

if __name__ == "__main__":
    unittest.main()
