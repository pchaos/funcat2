# -*- coding: utf-8 -*-
import unittest
import numpy as np
from funcat import *
from funcat.api import UPNDAY, DOWNNDAY, NDAY, KAMA
from funcat.utils import shift, rolling_sum
from .test_api import TestApi


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

    def test_kama(self):
        super().test_kama()

    def test_kama2(self):
        n = 20
        data = KAMA(CLOSE, n)
        self.assertTrue(len(data) > 1, "五日均线个数不大天1！")
        print(f"KAMA {n}:{data}, KAMA {n} 长度：{len(data)}")
        print(f"kama:", data.series[-20:])
        print(f"close:", CLOSE.series[-20:])
        print(f"kama < CLOSE", (data < CLOSE).series[-20:]) 
        print(f"kama参数：{n};前置nan数量：{len(CLOSE)-len(data.trim())}")
        
    def test_kama3(self):
        """测试KAMA参数"""
        
        def kama(price, n=10, pow1=2, pow2=30):
            '''kama indicator 
            accepts pandas dataframe of prices
            '''

            absDiffx = np.abs(price - shift(price, 1))  

            ER_change = np.abs(price - shift(price, n))
            
            ER_sum = rolling_sum(absDiffx, n)
            ER = ER_change / ER_sum

            sc = (ER * (2.0 / (pow1 + 1) - 2.0 / (pow2 + 1.0)) + 2 / (pow2 + 1.0)) ** 2.0

            answer = np.zeros(sc.size)
            N = len(answer)
            first_value = True

            for i in range(N):
                if sc[i] != sc[i]:
                    answer[i] = np.nan
                else:
                    if first_value:
                        answer[i] = price[i]
                        first_value = False
                    else:
                        answer[i] = answer[i - 1] + sc[i] * (price[i] - answer[i - 1])
            return answer

        n = 10
        data = KAMA(CLOSE, n)
        pow1, pow2=2, 30
        data2 = kama(CLOSE.series, n, pow1=pow1, pow2=pow2)
        print(f"\nkama:", np.round(data.series[-20:], 2))
        print(f"kama2:", np.round(data2[-20:], 2))
        m = 15
        print(f"KAMA-kama:", np.round(data.series[-n * m:], 2) - np.round(data2[-n * m:], 2))
        print(f"KAMA-kama full data:\n", np.round(data.series - data2, 4))
        print(f"KAMA paras: {n}, {pow1}, {pow2}")

    def test_kama_close_high(self):
        n = 20
        data = KAMA(CLOSE, n)
        data2 = KAMA(HIGH, n)
        m = 1
        print(f"kama high-kama close:", np.round(data2.series[-n * m:], 2) - np.round(data.series[-n * m:], 2))
        per = np.round((data2.series[-n * m:] - data.series[-n * m:]) / CLOSE.series[-n * m:] * 100, 3)
        print(f"kama high-kama close percent %:", per)
        per = np.round((CLOSE.series[-n * m:] - data.series[-n * m:]) / CLOSE.series[-n * m:] * 100, 3)
        print(f"Close-kama close percent %:", per)
        print(f"kama参数：{n};前置nan数量：{len(CLOSE)-len(data.trim())}")

    def test_kama_close_high2(self):
        T("20210531")
        n = 20
        data = KAMA(LOW, n)
        data2 = KAMA(HIGH, n)
        m = 1
        print(f"kama high-kama close:", np.round(data2.series[-n * m:], 2) - np.round(data.series[-n * m:], 2))
        per = np.round((data2.series[-n * m:] - data.series[-n * m:]) / CLOSE.series[-n * m:] * 100, 3)
        print(f"kama high-kama low percent %:", per)
        per = np.round((CLOSE.series[-n * m:] - data.series[-n * m:]) / CLOSE.series[-n * m:] * 100, 3)
        print(f"Close-kama low percent %:", per)
        print(f"kama参数：{n};前置nan数量：{len(CLOSE)-len(data.trim())}")
                
    def test_ref(self):
        n = 10
        c1 = REF(C, n)  # n天前的收盘价
        self.assertTrue(CLOSE.series[-(n + 1)] == c1.value, f"数据不匹配：{CLOSE.series[-(n + 1)]}, {c1}")

    def test_ref2(self):
        m = 10
        for n in range(1, m):
            c1 = REF(C, n)  # n天前的收盘价
            self.assertTrue(CLOSE.series[-(n + 1)] == c1.value, f"数据不匹配：{CLOSE.series[-(n + 1)]}, {c1}")
            print(n, c1)
        print(np.flipud(CLOSE.series[-m:]))

    def test_ref3(self):
        n = 10
        c1 = REF(C, n)  # n天前的收盘价
        print(f"CLOSE length :{len(CLOSE)};  REF(C, {n}) length:{len(c1)}")
        self.assertTrue(len(CLOSE) == len(c1) + n, "Ref的数据会缩短{n}")

    def test_ref4(self):
        n = 10
        c1 = REF(C, n)  # n天前的收盘价
        print(f"CLOSE length :{len(CLOSE)};  REF(C, {n}) length:{len(c1)}")
        j = n + 1
        c2 = REF(C, j - 1)  # j-1天前的收盘价
        self.assertTrue(len(c1) == len(c2))
        self.assertTrue(np.alltrue(c1.series == c2.series), f"c1.series == c2.series\n{c1.series == c2.series}")

    def test_ref5(self):
        n = 0
        c1 = REF(C, n)  # n天前的收盘价
        j = 1
        c2 = REF(C, j)  # j天前的收盘价
        self.assertTrue(len(c1) >= len(c2))
        self.assertTrue(len(c1) == len(CLOSE))
        self.assertTrue(np.alltrue(REF(c1, 1).series == c2.series), f"c1.series == c2.series\n{c1.series == c2.series}")
        self.assertTrue(np.alltrue(c1.series == CLOSE.series), f"c1.series == c2.series\n{c1.series == CLOSE.series}")

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
