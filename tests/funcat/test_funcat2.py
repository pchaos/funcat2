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
        T("20201216")
        S("000001.XSHG")

    def test_select(self):
        # 选出涨停股
        data = select(
            lambda: C / C[1] - 1 >= 0.0995,
            start_date=20181231,
            end_date=20190104,
        )
        self.assertTrue(len(data) > 10, f"涨停股:{data}")

    def test_select2(self):
        # 选出涨停股
        data = select(
            lambda: C / REF(C, 1) - 1 >= 0.0995,
            start_date=20181231,
            end_date=20190104,
        )
        self.assertTrue(len(data) > 10, f"涨停股:{data}")

    def test_select3(self):
        # 选出最近30天K线实体最高价最低价差7%以内，最近100天K线实体最高价最低价差25%以内，
        # 最近10天，收盘价大于60日均线的天数大于3天
        n8 = "20180201"  # 开始时间
        print("手动设定选股开始时间格式n8", n8)
        n9 = "20180201"  # 结束时间
        print("手动设定选股结束时间格式n9", n9)
        select(
            lambda: ((HHV(MAX(C, O), 30) / LLV(MIN(C, O), 30) - 1 < 0.07)
                     & (HHV(MAX(C, O), 100) / LLV(MIN(C, O), 100) - 1 > 0.25)
                     & (COUNT(C > MA(C, 60), 10) > 3)
                     ),
            start_date=(n8),
            end_date=(n9),
        )

    def test_select4(self):
        # 选出最近3天每天的成交量小于20日成交量均线，最近3天最低价低于20日均线，最高价高于20日均线
        # 自定义选股回调函数
        n8 = "20180201"  # 开始时间
        print("手动设定选股开始时间格式n8", n8)
        n9 = "20180201"  # 结束时间
        print("手动设定选股结束时间格式n9", n9)

        def callback(date, order_book_id, symbol):
            print("Cool, 在", date, "选出", order_book_id, symbol)

        select(
            lambda: (EVERY(V < MA(V, 20) / 2, 3) & EVERY(L < MA(C, 20), 3) & EVERY(H > MA(C, 20), 3)),
            start_date=(n8),
            end_date=(n9),
            callback=callback,
        )

    def test_CLOSE(self):
        data_backend = ExecutionContext.get_data_backend()
        order_book_id_list = data_backend.get_order_book_id_list()[150:300]
        # 选出涨停股
        data = select(
            lambda: C > 50,
            start_date=20181228,
            end_date=20190104,
            order_book_id_list=order_book_id_list
        )
        self.assertTrue(len(data) > 0, f"交易数据:{data}")
        print(data)

    def test_CLOSE_asyn(self):
        data_backend = ExecutionContext.get_data_backend()
        order_book_id_list = data_backend.get_order_book_id_list()[150:300]
        # 选出涨停股
        data = selectAsync(
            lambda: C > 50,
            start_date=20181221,
            end_date=20190104,
            order_book_id_list=order_book_id_list
        )
        self.assertTrue(len(data) > 0, f"交易数据:{data}")
        print(data)

    def test_CLOSE_select2(self):
        data_backend = ExecutionContext.get_data_backend()
        order_book_id_list = data_backend.get_order_book_id_list()[150:300]
        # 选出涨停股
        data = select2(
            lambda: C > 40,
            start_date=20181221,
            end_date=20190104,
            order_book_id_list=order_book_id_list
        )
        self.assertTrue(len(data) > 0, f"交易数据:{data}")
        print(data)

    def test_CLOSE_select2_2(self):
        data_backend = ExecutionContext.get_data_backend()
        order_book_id_list = data_backend.get_order_book_id_list()[150:300]
        # 选出涨停股
        data = select2(
            lambda: 30 > C > 20,
            start_date=20181221,
            end_date=20190104,
            order_book_id_list=order_book_id_list
        )
        self.assertTrue(len(data) > 0, f"交易数据:{data}")
        print(data)
        for item in range(len(data)):
            for key, value in data[item].items():
                print(key, value, end=";")
            print("")

    def test_cross(self):
        # 0x02 均线金叉死叉
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

    def test_rsv(self):
        N, M1, M2 = 27, 9, 3
        RSV = (CLOSE - LLV(LOW, N)) / (HHV(HIGH, N) - LLV(LOW, N)) * 100
        K = EMA(RSV, (M1 * 2 - 1))
        D = EMA(K, (M2 * 2 - 1))
        J = K * 3 - D * 2
        print(K, D, J)
        f, (ax1, ax2,) = plt.subplots(2, 1)
        ax1.plot(L.series, label="L")
        ax1.plot(MA(L, 7).series, label="ma7")
        ax1.plot(MA(H, 11).series, label="ma11")
        ax1.plot(MA(H, 22).series, label="ma22")
        ax1.plot(MA(H, 66).series, label="ma66")
        ax1.set_xlim(22)
        ax2.plot(K.series, label="K", linewidth=2)
        ax2.plot(D.series, label="D", alpha=0.7)
        ax2.plot(J.series, label="J", alpha=0.7)
        ax2.set_xlim(22)
        buy_signal = CROSS(J, K)
        sell_signal = CROSS(K, J)
        plt.plot(np.where(buy_signal.series)[0], K.series[np.where(buy_signal.series)[0]], "^", label="buy",
                 markersize=12, color="red")
        plt.plot(np.where(sell_signal.series)[0], J.series[np.where(sell_signal.series)[0]], "v", label="sell",
                 markersize=12, color="green")
        plt.legend(loc="best")
        plt.show()

    def test_callback(self):
        # 选出最近3天每天的成交量小于20日成交量均线，最近3天最低价低于20日均线，最高价高于20日均线
        # 自定义选股回调函数
        def callback(date, order_book_id, symbol):
            print("Cool, 在", date, "选出", order_book_id, symbol)

        select(
            lambda: (EVERY(V < MA(V, 20) / 2, 3) & EVERY(L < MA(C, 20), 3) & EVERY(H > MA(C, 20), 3)),
            start_date=20170104,
            end_date=20170104,
            callback=callback,
        )


if __name__ == '__main__':
    unittest.main()
