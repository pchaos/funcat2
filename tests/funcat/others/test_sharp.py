# -*- coding: utf-8 -*-

import math
from math import sqrt
import numpy as np
import tushare as ts

pro = ts.pro_api()
df = pro.daily(ts_code='601318.SH',start_date='20190101', end_date='20200101') 
print(df.head())

#计算方法一：
# 计算日收益率的均值：
mm=np.mean(df['pct_chg'])
# 计算收益率的方差
# 收益率减不减去无风险收益率求方差都没有影响。
nn=df['pct_chg'].std()
# 日夏普率：
ss=mm-0.01059015326852
SR=ss/nn

# 年夏普率：
SR1=(mm-0.01059015326852)/nn*math.sqrt(252)
print(f"日夏普率：{SR=} ，年夏普率：{SR1=}")

""" 对于固定时间内的夏普比率还得乘上一个k值。
对于不同采样频率的k值情况：
Daily=sqrt(252)（最小粒度是按天计）
Weekly=sqrt(52)（最小粒度是按星期计）
Monthly=sqrt(12)（最小粒度是按月计）
"""

Daily=sqrt(252)
Weekly=sqrt(52)
Monthly=sqrt(12)

print(f"{SR*Daily=} {SR1=}")

# 计算方法二：
df1 = df['pct_chg'] - (4/252)
print(f"{(df1.mean() * math.sqrt(252))/df1.std()=}")