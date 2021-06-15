# -*- coding: utf-8 -*-
"""ARIMA预测模型
https://zhuanlan.zhihu.com/p/342764105
"""

from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import adfuller
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import statsmodels.api as sm

from funcat.utils import FuncatTestCase
from funcat import CLOSE, DATETIME
from funcat.time_series import MarketDataSeries

__updated__ = "2021-06-11"


class test_arima(FuncatTestCase):
    @classmethod
    def setUpClass(cls)->None:
        super().setUpClass()
        # plt.figure(figsize=(15, 9))

    def test_arima(self):
        x = DATETIME
        y = CLOSE
        self.show(x, y)

    def test_arima_diff(self):
        x = DATETIME
        y = CLOSE.series - CLOSE.shift().series
        self.show(x, y)

    def test_adf(self):
        """单位根检验，确定数据为平稳时间序列
         (-7.699822523069757, # ADF检验的结果
        1.3486110988090724e-11, # P值
        6, # 滞后数量
        422,# 用于ADF回归和临界值计算的数量
        # 字典：1% 5% 10% 临界值 
        {'1%': -3.44594128742536, '5%': -2.868413360220551, '10%': -2.570431271085555}, 
        4067.5945920134773)
        """
        data_diff = CLOSE.series - CLOSE.shift().series
        data_diff = data_diff[~np.isnan(data_diff)]
        adf = adfuller(data_diff)
        print(adf)

    def test_adf_log(self):
        """单位根检验，确定数据为平稳时间序列
         (-7.699822523069757, # ADF检验的结果
        1.3486110988090724e-11, # P值
        6, # 滞后数量
        422,# 用于ADF回归和临界值计算的数量
        # 字典：1% 5% 10% 临界值 
        {'1%': -3.44594128742536, '5%': -2.868413360220551, '10%': -2.570431271085555}, 
        4067.5945920134773)
        """
        data_diff = np.log10(CLOSE.series) - np.log10(CLOSE.shift().series)
        data_diff = data_diff[~np.isnan(data_diff)]
        adf = adfuller(data_diff)
        print(adf)

    def test_acorr(self):
        """Q检验-检验数据是否具有相关性
        """
        data_diff = np.log10(CLOSE.series) - np.log10(CLOSE.shift().series)
        # data_diff = np.log10(CLOSE.series - CLOSE.shift().series)
        data_diff = data_diff[~np.isnan(data_diff)]
        data = pd.DataFrame(data_diff, index=DATETIME.series[-len(data_diff):])
        acr = acorr_ljungbox(data, lags=6)  # 第一个数：统计值； 第二个数：p值
        print(acr)

    def test_pacf(self):
        data_diff = np.log10(CLOSE.series) - np.log10(CLOSE.shift().series)
        # data_diff = np.log10(CLOSE.series - CLOSE.shift().series)
        data_diff = data_diff[~np.isnan(data_diff)]
        data = pd.DataFrame(data_diff, index=DATETIME.series[-len(data_diff):])
        pacf = plot_pacf(data, lags=20)

        plt.title('PACF')
        pacf.show()
        acf = plot_acf(data, lags=20)
        plt.title('ACF')
        acf.show()

    def test_pacf2(self):
        """https://www.codercto.com/a/41483.html"""
        data_diff = np.log10(CLOSE.series) - np.log10(CLOSE.shift().series)
        # data_diff = np.log10(CLOSE.series - CLOSE.shift().series)
        data_diff = data_diff[~np.isnan(data_diff)]
        data = pd.DataFrame(data_diff, index=DATETIME.series[-len(data_diff):])
        fig = plt.figure(figsize=(12, 8))
        ax1 = fig.add_subplot(211)
        fig = sm.graphics.tsa.plot_acf(data, lags=20, ax=ax1)
        ax2 = fig.add_subplot(212)
        fig = sm.graphics.tsa.plot_pacf(data, lags=20, ax=ax2)
        plt.show()


if __name__ == '__main__':
    FuncatTestCase.main()
