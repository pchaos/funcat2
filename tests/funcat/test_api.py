# -*- coding: utf-8 -*-
import unittest
from funcat import *
import numpy as np


class TestApi(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.setBackend()
        set_start_date(20200101)
        T("20201216")
        S("000001.XSHG")
        print(get_start_date(), get_current_date(), get_current_security())

    @classmethod
    def setBackend(cls):
        from funcat.data.tushare_backend import TushareDataBackend as BACKEND
        # from funcat.data.quantaxis_backend import QuantaxisDataBackend as backend
        set_data_backend(BACKEND())

    def test_T(self):
        # print(f"CLOSE: {help(CLOSE)}")
        print(f"CLOSE series: {(CLOSE.series)}")
        print(f"CLOSE value: {(CLOSE.value)}")
        # print(f"CLOSE: {help(CLOSE.value)}")
        print(get_start_date(), get_current_date(), get_current_security())

    def test_000001(self):
        set_start_date(20150101)
        T("20161216")
        S("000001.XSHG")

        assert np.equal(round(CLOSE.value, 2), 3122.98), f"收盘价：{C}"
        assert np.equal(round(OPEN[2].value, 2), 3149.38)
        assert np.equal(round((CLOSE - OPEN).value, 2),
                        11.47), f"round((CLOSE - OPEN).value, 2):{round((CLOSE - OPEN).value, 2)}"
        assert np.equal(round((CLOSE - OPEN)[2].value, 2), -8.85)
        assert np.equal(round(((CLOSE / CLOSE[1] - 1) * 100).value, 2), 0.17)
        assert np.equal(round(MA(CLOSE, 60)[2].value, 2), 3131.08)
        assert np.equal(round(MACD().value, 2), -37.18)
        assert np.equal(round(HHV(HIGH, 5).value, 2), 3245.09)
        assert np.equal(round(LLV(LOW, 5).value, 2), 3100.91)
        assert COUNT(CLOSE > OPEN, 5) == 2

    def test_close(self):
        set_start_date(20150101)

        T("20161216")
        # S("000002.XSHG")
        # S("000001.XSHG")
        c = CLOSE
        if not c:
            print("没有数据返回！")
        print(f"CLOSE: {c} {CLOSE.series}")
        print(f"CLOSE长度: {c[len(c)]}")
        print(f"返回数据长度：{len(c)}, {type(c)}, type :{c.dtype}")
        assert np.equal(round(CLOSE.value, 2), 3122.98), f"收盘价：{CLOSE.value}, {type(CLOSE)}"

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
        print(f"MA5:{data.series}, MA 5 长度：{len(data)}")
        print(f"EMA5:{data2}, EMA 5 长度：{len(data2)}")
        self.assertFalse(data == data2, f"{data}, {data2}")
        print(f"data == data2,\n{data == data2,}")

    def test_wma(self):
        data = WMA(CLOSE, 5)
        self.assertTrue(len(data) > 1, "五日均线个数不大天1！")
        print(f"WMA5:{data}, WMA 5 长度：{len(data)}")

    def test_cci(self):
        data = CCI(CLOSE, HIGH, LOW)
        self.assertTrue(len(data) > 1, "cci个数不大天1！")
        print(f"CCI:{data}, CCI 5 长度：{len(data)}")

    def test_barslast(self):
        data = BARSLAST(C > 0)
        assert np.equal(REF(C, data).value, C.value)
        print(f"BARSLAST:{data}, BARSLAST长度：{len(data)}")


if __name__ == '__main__':
    unittest.main()
