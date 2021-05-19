# -*- coding: utf-8 -*-
import unittest
import numpy as np
from funcat.api import *
from funcat.utils import MyTestCase


class TestTurtle(MyTestCase):

    @classmethod
    def setUp(cls) -> None:
        T("20210506")
        S("000001.XSHG")
        
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

    def test_four_week(self):
        n = 20
        fakedata = self.fakeMarketData()
        hh, ll = FOURWEEK(fakedata, fakedata, n, n)
        data = hh or ll
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
        data = hh or ll
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
