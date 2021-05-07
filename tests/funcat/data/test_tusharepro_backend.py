import unittest
from unittest import TestCase
from funcat import *

BACKEND = TushareProDataBackend


class TestTushareDataBackend(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        set_data_backend(BACKEND())
        cls.be = BACKEND()

    def test_stock_basics(self):
        data = self.be.stock_basics
        self.assertTrue(len(data) > 3500, f"股票代码数量：{len(data)},实际数量应该大于3500只。")
        print(data)

    def test_get_price(self):
        data = self.be.get_price("000001.sz", 20210101, 20210201, '1d')
        self.assertTrue(len(data) > 10, f"交易日期数量：{len(data)},实际应该大于10天。")
        print(data)
        # index
        data = self.be.get_price("000001.SH", 20210101, 20210201, '1d')
        self.assertTrue(len(data) > 10, f"交易日期数量：{len(data)},实际应该大于10天。")
        print(data)

if __name__ == '__main__':
    unittest.main()
