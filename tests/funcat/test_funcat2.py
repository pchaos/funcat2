# -*- coding: utf-8 -*-
import unittest
from matplotlib import rcParams
import matplotlib.pyplot as plt
import numpy as np
from funcat import *
from funcat.api import *
from funcat.context import ExecutionContext


class TestFuncat2TestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        set_data_backend(QuantaxisDataBackend())
        cls.qdb = QuantaxisDataBackend()

    def test_select(self):
        # 选出涨停股
        data = select(
            lambda: C / C[1] - 1 >= 0.0995,
            start_date=20181231,
            end_date=20190104,
        )
        self.assertTrue(len(data) > 10, f"涨停股:{data}")

    def test_CLOSE(self):
        data_backend = ExecutionContext.get_data_backend()
        order_book_id_list = data_backend.get_order_book_id_list()[:300]
        # 选出涨停股
        data = select(
            lambda: C > 50,
            start_date=20181221,
            end_date=20190104,
            order_book_id_list=order_book_id_list
        )
        self.assertTrue(len(data) > 10, f"交易数据:{data}")

    def test_CLOSE_asyn(self):
        data_backend = ExecutionContext.get_data_backend()
        order_book_id_list = data_backend.get_order_book_id_list()[:150]
        # 选出涨停股
        data = selectAsync(
            lambda: C > 50,
            start_date=20181221,
            end_date=20190104,
            order_book_id_list=order_book_id_list
        )
        self.assertTrue(len(data) > 10, f"交易数据:{data}")

    def test_cross(self):
        # 0x02 均线金叉死叉
        T("20201216")
        S("000001.XSHG")
        ax = plt.subplot()
        ma1 = MA(L, 1)
        ma3 = MA(H, 3)
        ma5 = MA(H, 5)
        ma7 = MA(H, 7)
        ma11 = MA(H, 11)
        ma22 = MA(H, 22)
        ma66 = MA(H, 66)
        buy_signal = CROSS(ma1, ma7)
        sell_signal = CROSS(ma7, ma1)
        plt.plot(C.series, label="H", linewidth=2)
        plt.plot(ma1.series, label="ma1", alpha=0.7)
        plt.plot(ma3.series, label="ma3", alpha=0.7)
        plt.plot(ma5.series, label="ma5", alpha=0.7)
        plt.plot(ma7.series, label="ma7", alpha=0.7)
        plt.plot(ma11.series, label="ma11", alpha=0.7)
        plt.plot(ma22.series, label="ma22", alpha=0.7)
        plt.plot(ma66.series, label="ma66", alpha=0.7)
        plt.plot(np.where(buy_signal.series)[0], C.series[np.where(buy_signal.series)[0]], "^", label="buy",
                 markersize=12, color="red")
        plt.plot(np.where(sell_signal.series)[0], C.series[np.where(sell_signal.series)[0]], "v", label="sell",
                 markersize=12, color="green")
        plt.legend(loc="best")
        plt.show()

if __name__ == '__main__':
    unittest.main()
