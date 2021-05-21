# -*- coding: utf-8 -*-
import unittest

import numpy as np


class MyTestCase(unittest.TestCase):
    """测试单元基类
    """

    @classmethod
    def setUpClass(cls) -> None:
        from funcat import QuantaxisDataBackend as BACKEND, set_data_backend
        set_data_backend(BACKEND())
        cls.BE = BACKEND()

    @classmethod
    def tearDown(self):
        super().tearDown(self)
        try:
            # 打印当前交易信息
            from funcat import get_start_date, get_current_date, get_current_security
            from funcat.context import ExecutionContext
            start_date = get_start_date()
            current_date = get_current_date()
            trading_dates = ExecutionContext.get_data_backend().get_trading_dates(start=start_date, end=current_date)
            print(f"|| --> {get_current_security()},trading dates:{trading_dates[0]}~{trading_dates[-1]}")
        except Exception:
            pass
        
    @classmethod
    def tearDownClass(cls):
        from funcat.utils import FuncCounter
        super(MyTestCase, cls).tearDownClass()
        print(f"调用记录：{FuncCounter()}")
        
    def fakeMarketData(self, arr=None):
        from funcat.time_series import MarketDataSeries
        """产生模拟交易数据,便于校验数据
        默认返回MarketDataSeries子类，子类series为np.array(range(100))
        """
        if arr is None:
            fakeData = np.array(range(100))
        else:
            fakeData = arr
        name = "fake"
        dtype = float
        cls = type("{}Series".format(name.capitalize()), (MarketDataSeries,), {"name": name, "dtype": dtype})
        obj = cls(dynamic_update=False)
        obj._series = fakeData
        print(f"{obj}, {obj.series}")
        return obj
