# -*- coding: utf-8 -*-
""""""

from matplotlib import pyplot as plt
import pandas as pd

from funcat.utils import FuncatTestCase
from funcat import CLOSE, DATETIME
from funcat.time_series import MarketDataSeries

__updated__ = "2021-06-11"


class test_arima(FuncatTestCase):
    def test_arima(self):
        x = DATETIME
        y = CLOSE
        self.show(x, y)

    def show(self, x, y):
        def prepare_plt(var):
            if var is DATETIME:
                var = var.series // 1000000
                var = pd.to_datetime(var.astype(str)).values
            elif hasattr(var, "series"):
                var = var.series
            return var
        x = prepare_plt(x)
        y = prepare_plt(y)

        plt.figure(figsize=(10, 6))
        plt.plot(x, y)
        plt.show()

    def test_arima_diff(self):
        x = DATETIME
        y = CLOSE.series - CLOSE.shift().series
        self.show(x, y)


if __name__ == '__main__':
    FuncatTestCase.main()
