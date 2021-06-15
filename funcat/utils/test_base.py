# -*- coding: utf-8 -*-
import unittest
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

__updated__ = "2021-06-15"


class FuncatTestCase(unittest.TestCase):
    """测试单元基类
    """

    @classmethod
    def setUpClass(cls) -> None:
        """默认使用QuantaxisDataBackend"""
        from funcat import QuantaxisDataBackend as BACKEND, set_data_backend
        set_data_backend(BACKEND())
        cls.BE = BACKEND()

    @classmethod
    def tearDown(self):
        super().tearDown(self)
        try:
            # 打印当前统计信息
            from funcat import get_start_date, get_current_date, get_current_security
            from funcat.context import ExecutionContext
            start_date = get_start_date()
            current_date = get_current_date()
            trading_dates = ExecutionContext.get_data_backend(
            ).get_trading_dates(start=start_date, end=current_date)
            print(
                f"|| --> {get_current_security()},trading dates:{trading_dates[0]}~{trading_dates[-1]}")
        except Exception:
            pass

    @classmethod
    def tearDownClass(cls):
        from funcat.utils import FuncCounter
        super(FuncatTestCase, cls).tearDownClass()
        print(f"调用记录：{FuncCounter()}")

    def fakeMarketData(self, arr=None):
        """产生模拟交易数据,便于校验数据
        默认返回MarketDataSeries子类，子类series为np.array(range(100))
        """
        from funcat.time_series import MarketDataSeries
        if arr is None:
            # fakeData = np.array(range(100))
            fakeData = np.arange(100)
        else:
            fakeData = arr
        name = "fake"
        dtype = float
        cls = type("{}Series".format(name.capitalize()),
                   (MarketDataSeries,), {"name": name, "dtype": dtype})
        obj = cls(dynamic_update=False)
        obj._series = fakeData
        print(f"{obj}, {obj.series}")
        return obj

    def show(self, x, y):
        """x,y画图"""
        from ..api import DATETIME

        def prepare_plt(var):
            if var is DATETIME:
                var = var.series // 1000000
                var = pd.to_datetime(var.astype(str)).values
            elif hasattr(var, "series"):
                var = var.series
            return var
        x = prepare_plt(x)
        y = prepare_plt(y)

        plt.figure(figsize=(15, 9))
        plt.plot(x, y)
        plt.show()
