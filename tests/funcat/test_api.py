# -*- coding: utf-8 -*-
import unittest
from funcat import *
import numpy as np


class TestApi(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        from funcat.data.tushare_backend import TushareDataBackend as backend
        # from funcat.data.quantaxis_backend import QuantaxisDataBackend as backend
        set_data_backend(backend())
        T("20201216")
        S("000001.XSHG")

    def test_000001(self):
        T("20161216")
        S("000001.XSHG")

        assert np.equal(round(CLOSE.value, 2), 3122.98), f"收盘价：{C}"
        assert np.equal(round(OPEN[2].value, 2), 3149.38)
        assert np.equal(round((CLOSE - OPEN).value, 2), 11.47)
        assert np.equal(round((CLOSE - OPEN)[2].value, 2), -8.85)
        assert np.equal(round(((CLOSE / CLOSE[1] - 1) * 100).value, 2), 0.17)
        assert np.equal(round(MA(CLOSE, 60)[2].value, 2), 3131.08)
        assert np.equal(round(MACD().value, 2), -37.18)
        assert np.equal(round(HHV(HIGH, 5).value, 2), 3245.09)
        assert np.equal(round(LLV(LOW, 5).value, 2), 3100.91)
        assert COUNT(CLOSE > OPEN, 5) == 2

    def test_close(self):
        T("20161216")
        S("000001.XSHG")
        self.assertTrue(np.equal(round(CLOSE.value, 2), 3122.98), f"收盘价：{CLOSE}")

    def test_ma(self):
        c = C
        print(c, C, f"CLOSE type:{type(CLOSE)}, length: {len(CLOSE)}")
        self.assertTrue(len(c) > 1, f"len(C) {len(c)}")
        ma5 = MA(CLOSE, 5)
        self.assertTrue(len(ma5) > 1, "五日均线个数不大天1！")
        print(f"MA5:{ma5}, MA 5 长度：{len(ma5)}")

    def test_ema(self):
        data = EMA(CLOSE, 5)
        self.assertTrue(len(data) > 1, "五日均线个数不大天1！")
        print(f"EMA5:{data}, EMA 5 长度：{len(data)}")

    def test_ma_ema(self):
        data = MA(CLOSE, 5)
        data2 = EMA(CLOSE, 5)
        self.assertTrue(len(data) == len(data2), "ma ema长度不同")
        print(f"EMA5:{data}, EMA 5 长度：{len(data)}")

    def test_wma(self):
        data = WMA(CLOSE, 5)
        self.assertTrue(len(data) > 1, "五日均线个数不大天1！")
        print(f"WMA5:{data}, WMA 5 长度：{len(data)}")


if __name__ == '__main__':
    unittest.main()
