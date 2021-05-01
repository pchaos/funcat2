from unittest import TestCase
from funcat import *

BACKEND = TushareProDataBackend


class TestTushareDataBackend(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        set_data_backend(BACKEND())
        cls.be = BACKEND()

    def test_get_price(self):
        data = self.be.get_price("000001", 20210101, 20210201, '1d')
        self.assertTrue(len(data) > 10, f"交易日期数量：{len(data)},实际应该大于10天。")
        print(data)
        # index
        data = self.be.get_price("000001", 20210101, 20210201, '1d', is_index=True)
        self.assertTrue(len(data) > 10, f"交易日期数量：{len(data)},实际应该大于10天。")
        print(data)
