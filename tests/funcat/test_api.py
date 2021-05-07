# -*- coding: utf-8 -*-
import unittest
import numpy as np
from funcat import *
from funcat.api import UPNDAY, DOWNNDAY, NDAY
from funcat.utils import MyTestCase

class TestApi(MyTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.setBackend()
        set_start_date(20200101)
        T("20201216")
        S("000001.XSHG")
        print(get_start_date(), get_current_date(), get_current_security())

    @classmethod
    def setBackend(cls):
        # from funcat.data.tushare_backend import TushareDataBackend as BACKEND
        from funcat.data.quantaxis_backend import QuantaxisDataBackend as BACKEND
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

    def test_sma(self):
        data = SMA(CLOSE, 5)
        self.assertTrue(len(data) > 1, "五日均线个数不大天1！")
        print(f"SMA 5:{data}, SMA 5 长度：{len(data)}")

    def test_llv(self):
        n = 3
        data = LLV(CLOSE, n)
        self.assertTrue(len(data) > 1, "LLV个数不大天1！")
        print(f"LLV: {data.series}, LLV {n} 长度：{len(data)}, {data}")

    def test_llv_2(self):
        fakeData = self.fakeMarketData()
        n = 5
        data = LLV(fakeData, n)
        self.assertTrue(len(data) > 1, "LLV个数不大天1！")
        print(f"LLV:{data.series}, LLV {n} 长度：{len(data)}, {data}")
        self.assertTrue(len(fakeData) == (len(data) + n - 1), f"返回数量不匹配！{len(fakeData)}， {len(data)}")

    def test_llv_3(self):
        fakeData = self.fakeMarketData(np.array([i for i in range(100, 0, -1)]))
        n = 5
        data = LLV(fakeData, n)
        print(f"LLV:{data.series}, LLV {n} 长度：{len(data)}, {data}")
        self.assertTrue(len(fakeData) == (len(data) + n - 1), f"返回数量不匹配！{len(fakeData)}， {len(data)}")
        self.assertIn(data.series, fakeData.series[(n - 1):], f"{fakeData.series[(n - 1):]}")
        self.assertTrue(np.alltrue(data.series == fakeData.series[(n - 1):]), f"{fakeData.series[(n - 1):]}")

    def test_llv_4(self):
        fakeData = self.fakeMarketData(np.array([i for i in range(100, 1, -1)]))
        n = 0
        data = LLV(fakeData, n)
        print(f"LLV:{data.series}, LLV {n} 长度：{len(data)}, {data}")
        self.assertTrue(len(data) == 1, f"返回数量不匹配！{len(fakeData)}， {len(data)}")
        self.assertTrue(np.alltrue(data.series == fakeData.series[(n - 1):]), f"历史最低价 {fakeData.series[(n - 1):]}")

    def test_hhv(self):
        n = 3
        data = HHV(CLOSE, n)
        self.assertTrue(len(data) > 1, "HHV个数不大天1！")
        print(f"HHV: {data.series}, HHV {n} 长度：{len(data)}, {data}")

    def test_hhv_2(self):
        fakeData = self.fakeMarketData()
        n = 5
        data = HHV(fakeData, n)
        self.assertTrue(len(data) > 1, "LLV个数不大天1！")
        print(f"HHV:{data.series}, HHV {n} 长度：{len(data)}, {data}")
        self.assertTrue(len(fakeData) == (len(data) + n - 1), f"返回数量不匹配！{len(fakeData)}， {len(data)}")
        self.assertTrue(np.alltrue(data.series == fakeData.series[(n - 1):]), f"{fakeData.series[(n - 1):]}")

    def test_hhv_3(self):
        fakeData = self.fakeMarketData(np.array([i for i in range(100, 0, -1)]))
        n = 5
        data = HHV(fakeData, n)
        self.assertTrue(len(data) > 1, "LLV个数不大天1！")
        print(f"HHV:{data.series}, HHV {n} 长度：{len(data)}, {data}")
        self.assertTrue(len(fakeData) == (len(data) + n - 1), f"返回数量不匹配！{len(fakeData)}， {len(data)}")
        self.assertTrue(np.alltrue(data.series == fakeData.series[:-(n - 1)]), f"{fakeData.series[(n - 1):]}")

    def test_hhv_4(self):
        fakeData = self.fakeMarketData(np.array([i for i in range(100, 0, -1)]))
        n = 0
        data = HHV(fakeData, n)
        self.assertTrue(len(data) == 1, "HHV个数不等于1！")
        print(f"HHV:{data.series}, HHV {n} 长度：{len(data)}, {data}")
        self.assertTrue(len(fakeData) >= len(data), f"返回数量不匹配！{len(fakeData)}， {len(data)}")
        self.assertTrue(np.alltrue(data.series == fakeData.series[:-(n - 1)]), f"{fakeData.series[(n - 1):]}")

    def test_cci(self):
        data = CCI(CLOSE, HIGH, LOW)
        self.assertTrue(len(data) > 1, "cci个数不大天1！")
        print(f"CCI:{data}, CCI 5 长度：{len(data)}")

    def test_barslast(self):
        data = BARSLAST(C > 0)
        assert np.equal(REF(C, data).value, C.value)
        print(f"BARSLAST:{data}, BARSLAST长度：{len(data)}")
        data2 = BARSLAST(C > LOW)
        print(f"BARSLAST(C > LOW):{data2}")


class TestApiQuantaxis(TestApi):
    @classmethod
    def setBackend(cls):
        from funcat.data.quantaxis_backend import QuantaxisDataBackend as BACKEND
        set_data_backend(BACKEND())
        print(BACKEND.__name__)

    def test_close(self):
        set_start_date(20160101)

        T("20161216")
        # S("000002.XSHG")
        # S("000001.XSHG")
        c = CLOSE
        if not c:
            print("没有数据返回！")
        print(f"CLOSE: {c} {CLOSE.series}")
        print(f"CLOSE长度: {c[len(c)]}")
        print(f"返回数据长度：{len(c)}, {type(c)}, type :{c.dtype}, name: {c.name}")
        # print(dir(c))
        assert np.equal(round(CLOSE.value, 2), 3122.98), f"收盘价：{CLOSE.value}, {type(CLOSE)}"

        # stock
        S("000001")
        assert np.equal(round(CLOSE.value, 2), 9.25), f"收盘价：{CLOSE.value}, {type(CLOSE)}"

    def test_ref(self):
        n = 10
        c1 = REF(C, n)  # n天前的收盘价
        self.assertTrue(CLOSE.series[-(n + 1)] == c1.value, f"数据不匹配：{CLOSE.series[-(n + 1)]}, {c1}")

    def test_ref3(self):
        n = 10
        c1 = REF(C, n)  # n天前的收盘价
        print(f"CLOSE length :{len(CLOSE)};  REF(C, {n}) length:{len(c1)}")
        self.assertTrue(len(CLOSE) == len(c1) + n, "Ref的数据会缩短{n}")

    def test_ref2(self):
        m = 10
        for n in range(1, m):
            c1 = REF(C, n)  # n天前的收盘价
            self.assertTrue(CLOSE.series[-(n + 1)] == c1.value, f"数据不匹配：{CLOSE.series[-(n + 1)]}, {c1}")
            print(n, c1)
        print(np.flipud(CLOSE.series[-m:]))

    def test_upnday(self):
        n = 5
        und = UPNDAY(CLOSE, n)
        print(f"CLOSE length :{len(CLOSE)}; UPNDAY length:{len(und)}")
        self.assertTrue(len(CLOSE) == len(und) + n + 1, "返回的结果会变短{n+1}")

    def test_upnday2(self):
        n = 5
        fakeData = self.fakeMarketData()
        und = UPNDAY(fakeData, n)
        for i in range(1, len(fakeData) - n - 1):
            # 返回结果每个都为True
            self.assertTrue(und.series[i], f"第{i}个数据返回不正确")

    def test_upnday3(self):
        n = 5
        fakeData = self.fakeMarketData(np.array([i for i in range(100, 0, -1)]))
        und = UPNDAY(fakeData, n)
        for i in range(1, len(fakeData) - n - 1):
            # 返回结果每个都为False
            self.assertTrue(und.series[i] == False, f"第{i}个数据返回不正确")

    def test_upnday4(self):
        n = 5
        m = 100
        data = np.array(range(int(m / 2), 0, -1))
        data2 = np.array(range(int(m / 2)))
        fakeData = self.fakeMarketData(np.append(data, data2))
        result = {"0": 0, "1": 0}
        und = UPNDAY(fakeData, n)
        for i in range(1, len(und)):
            if und.series[i]:
                result["1"] += 1
            else:
                result["0"] += 1
        print(f"原始数据长度：{len(fakeData)}, 返回数据长度：{len(und)}\n", result)
        self.assertTrue(result["1"] < result["0"], f"连续上涨的个数应该小于非连续上涨的个数")
        self.assertTrue(result["1"] + result["0"] + n + 2 == int(m / 2) * 2, f"连续上涨的个数应该小于非连续上涨的个数")

    def test_upnday5(self):
        n = 5
        data = np.array(range(10, 0, -1))
        data2 = np.array(range(10))
        fd = np.append(data, data2)
        for i in range(3):
            fd = np.append(fd, fd)
        fakeData = self.fakeMarketData(fd)
        result = {"0": 0, "1": 0}
        und = UPNDAY(fakeData, n)
        for i in range(1, len(und)):
            if und.series[i]:
                result["1"] += 1
            else:
                result["0"] += 1
        print(f"原始数据长度：{len(fakeData)}, 返回数据长度：{len(und)}\n", result)
        print(und.series)

    # def test_upnday6(self):
    #     # todo
    #     n = 5
    #     und = UPNDAY(CLOSE, n)
    #     print(f"CLOSE length :{len(CLOSE)}; UPNDAY length:{len(und)}")
    #     # print(und.series)
    #     for i in range(n + 1, len(und)):
    #         if und[i]:
    #             j = len(und) - (i + n + 1)
    #             # j = len(und) - (i + n )
    #             a, b, c = CLOSE[j], CLOSE[j + 1], CLOSE[j + 2]
    #             print(i, a, b, c, end=";")
    #             if a > b > c:
    #                 print(True)
    #             else:
    #                 print(False)
    #                 try:
    #                     print(CLOSE[j - 1], CLOSE[j + 3])
    #                 except Exception as e:
    #                     pass

    def test_downnday(self):
        n = 5
        und = DOWNNDAY(CLOSE, n)
        print(f"CLOSE length :{len(CLOSE)}; DOWNNDAY length:{len(und)}")
        self.assertTrue(len(CLOSE) == len(und) + n + 1, "返回的结果会变短{n+1}")

    def test_downnday2(self):
        n = 5
        fakeData = self.fakeMarketData(np.array([i for i in range(100, 0, -1)]))
        und = DOWNNDAY(fakeData, n)
        for i in range(1, len(fakeData) - n - 1):
            # 返回结果每个都为False
            self.assertTrue(und.series[i], f"第{i}个数据返回不正确")

    def test_nday(self):
        n = 5
        und = NDAY(HIGH, LOW, n)
        print(f"CLOSE length :{len(CLOSE)}; NDAY length:{len(und)}")
        self.assertTrue(len(CLOSE) == len(und) + n, f"返回的结果会变短{len(CLOSE) - len(und)}")
        for i in range(1, len(und)):
            # 返回结果每个都为False
            self.assertTrue(und.series[i], f"第{i}个数据返回不正确")

    def test_nday2(self):
        n = 5
        und = NDAY(LOW, HIGH, n)
        print(f"CLOSE length :{len(CLOSE)}; NDAY length:{len(und)}")
        self.assertTrue(len(CLOSE) == len(und) + n, f"返回的结果会变短{len(CLOSE) - len(und)}")
        for i in range(1, len(und)):
            # 返回结果每个都为False
            self.assertTrue(und.series[i] == False, f"第{i}个数据返回不正确")


if __name__ == '__main__':
    unittest.main()
