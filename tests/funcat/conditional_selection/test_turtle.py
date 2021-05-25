# -*- coding: utf-8 -*-
import unittest
import numpy as np
from datetime import date
from funcat import FOURWEEK, FOURWEEKQTY
from funcat.api import T, S, set_current_freq, symbol, \
  CLOSE
from funcat.utils import FuncatTestCase


class TestTurtle(FuncatTestCase):

    @classmethod
    def setUp(cls) -> None:
        T("20210506")
        S("000001.XSHG")
        set_current_freq("1d")
        
    def test_four_week_qty(self):
        n = 20
        last_high, last_low = FOURWEEKQTY()
        print(last_high, last_low.series[-10:])
        print(last_high.series[n - 1:n + 20], last_low.series[:10])
        print(last_high, last_low.series[-10:])
        print(tuple(zip(last_high.series, last_low.series)))
        for h, l in tuple(zip(last_high.series, last_low.series)):
            self.assertTrue((h > l) or not(h > 0), f"四周规则上轨应该比下轨大：{h},{l} ; {type(h)}")
        self.assertTrue(len(CLOSE) == len(last_high), f"{len(CLOSE)} == {len(last_high)}")

    def test_four_week_qty_weeks(self):
        """周为单位计算四周规则"""
        set_current_freq("W")
        n = 4
        last_high, last_low = FOURWEEKQTY(CLOSE, CLOSE, n, n)
        print(last_high, last_low.series[-10:])
        print(last_high.series[n - 1:n + 20], last_low.series[:10])
        print(last_high, last_low.series[-10:])
        print(tuple(zip(last_high.series, last_low.series)))
        for h, l in tuple(zip(last_high.series, last_low.series)):
            self.assertTrue((h > l) or not(h > 0), f"四周规则上轨应该比下轨大：{h},{l} ; {type(h)}")
        self.assertTrue(len(CLOSE) == len(last_high), f"{len(CLOSE)} == {len(last_high)}")
        
    def test_four_week(self):
        n = 20
        fakedata = self.fakeMarketData()
        hh, ll = FOURWEEK(fakedata, fakedata, n, n)
        data = hh + ll
        print(data.series[n - 1:n + 20])
        last_high, last_low = FOURWEEKQTY(fakedata, fakedata, n, n)
        for count, item in enumerate(data.tolist()):
            if count >= n - 1:
                if data.series[count] > 0:
                    self.assertTrue(fakedata.series[count] > last_high.series[count - 1],
                        f"{count}: { data.series[count]} --> {fakedata.series[count]}, {last_high.series[count-1]} --> {last_low.series[count-1]}") 
                elif data.series[count] < 0:
                    self.assertTrue(fakedata.series[count] < last_low.series[count - 1],
                        f"{count}: { data.series[count]} --> {fakedata.series[count]}, {last_high.series[count-1]} --> {last_low.series[count-1]}") 

    def test_four_week2(self):
        n = 20
        hh, ll = FOURWEEK()
        data = hh + ll
        print(data.series[n - 1:n + 20])
        last_high, last_low = FOURWEEKQTY()
        print(f"CLose: {len(CLOSE)}\n", CLOSE.series[n - 1:20])
        print(f"high series: {len(last_high)}\n", last_high.series[n - 1:n + 20], "\nlow series:\n", last_low.series[n - 1:n + 20])
        print(data.series[-10:])
        for count, item in enumerate(data.tolist()):
            if count >= n - 1:
                if data.series[count]:
                    self.assertTrue(CLOSE.series[count] > last_high.series[count - 1] 
                        or CLOSE.series[count] < last_low.series[count - 1] ,
                        f"{count}: { data.series[count]} --> {CLOSE.series[count]}, {last_high.series[count-1]} --> {last_low.series[count-1]}") 

    def test_four_week_002124(self):
        n = 20
        code = "002124"
        S(code)
        hh, ll = FOURWEEK(high_n=n, low_n=n)
        data = hh + ll
        print(data.series[n - 1:])
        print(f"{symbol(code)}:", data.series[data.series == 1])
        last_high, last_low = FOURWEEKQTY(high_n=n, low_n=n)
        fakedata, _ = FOURWEEKQTY.__self__.default_quantity()
        for count, item in enumerate(data.tolist()):
            if count >= n - 1:
                if data.series[count] > 0:
                    self.assertTrue(fakedata.series[count] > last_high.series[count - 1],
                        f"{count}: { data.series[count]} --> {fakedata.series[count]}, {last_high.series[count-1]} --> {last_low.series[count-1]}")
                    # print() 
                elif data.series[count] < 0:
                    self.assertTrue(fakedata.series[count] < last_low.series[count - 1],
                        f"{count}: { data.series[count]} --> {fakedata.series[count]}, {last_high.series[count-1]} --> {last_low.series[count-1]}")
        # print(fakedata.__class__)
        self.assertTrue(type(fakedata) == type(CLOSE), f"类型不匹配：{type(fakedata)}")

    def test_four_week_399673(self):
        n = 20
        T("20210520")
        code = "399673.XSHE"
        S(code)
        hh, ll = FOURWEEK(high_n=n, low_n=n)
        data = hh + ll
        print(data.series[n - 1:])
        print(f"{symbol(code)}:", data.series[data.series == 1])
        # print(data.series[hh.series == 1])
        print(data.series[data.series == -1])
        last_high, last_low = FOURWEEKQTY(high_n=n, low_n=n)
        fakedata, _ = FOURWEEKQTY.__self__.default_quantity()
        for count, item in enumerate(data.tolist()):
            if count >= n - 1:
                if data.series[count] > 0:
                    self.assertTrue(fakedata.series[count] > last_high.series[count - 1],
                        f"{count}: { data.series[count]} --> {fakedata.series[count]}, {last_high.series[count-1]} --> {last_low.series[count-1]}")
                    # print() 
                elif data.series[count] < 0:
                    self.assertTrue(fakedata.series[count] < last_low.series[count - 1],
                        f"{count}: { data.series[count]} --> {fakedata.series[count]}, {last_high.series[count-1]} --> {last_low.series[count-1]}")
                 
        expect_result = [ 0, 0, 0, 0, 0, 0, 1, 0, 1, 1]
        self.assertListEqual(data.tolist()[-10:], expect_result, f"和预期不同：{data.tolist()[-10:]}\n{expect_result}")
