# -*- coding: utf-8 -*-
"""隐马尔科夫链模型对于沪深300指数建模的进一步研究
https://uqer.datayes.com/v3/community/share/5703fde7228e5b48feeb403e
"""

from hmmlearn.hmm import GaussianHMM
import numpy as np
from matplotlib import cm, pyplot as plt
import matplotlib.dates as dates
import pandas as pd
import datetime

from scipy import stats # To perform box-cox transformation
from sklearn import preprocessing # To center and standardize the data.

# Source Code from previous HMM modeling

# Note that numbers of hidden states are modified to be 3, instead of 6.

beginDate = '2005-01-01'
endDate = '2015-12-31'
n = 3 # Hidden states are set to be 3 instead of 6
data = get_price('CSI300.INDX',start_date=beginDate, end_date=endDate,frequency='1d')
data[0:9]

volume = data['TotalVolumeTraded']
close = data['ClosingPx']

logDel = np.log(np.array(data['HighPx'])) - np.log(np.array(data['LowPx']))
logDel

logRet_1 = np.array(np.diff(np.log(close)))#这个作为后面计算收益使用
logRet_5 = np.log(np.array(close[5:])) - np.log(np.array(close[:-5]))
logRet_5

logVol_5 = np.log(np.array(volume[5:])) - np.log(np.array(volume[:-5]))
logVol_5

logDel = logDel[5:]
logRet_1 = logRet_1[4:]
close = close[5:]
Date = pd.to_datetime(data.index[5:])

# the histogram of the raw observation sequences

n, bins, patches = plt.hist(logDel, 50, normed=1, facecolor='green', alpha=0.75)

plt.show()

n, bins, patches = plt.hist(logRet_5, 50, normed=1, facecolor='green', alpha=0.75)

plt.show()

n, bins, patches = plt.hist(logVol_5, 50, normed=1, facecolor='green', alpha=0.75)

plt.show()

# Box-Cox Transformation of the observation sequences

boxcox_logDel, _ = stats.boxcox(logDel)

# Standardize the observation sequence distribution

rescaled_boxcox_logDel = preprocessing.scale(boxcox_logDel, axis=0, with_mean=True, with_std=True, copy=False)

rescaled_logRet_5 = preprocessing.scale(logRet_5, axis=0, with_mean=True, with_std=True, copy=False)

rescaled_logVol_5 = preprocessing.scale(logVol_5, axis=0, with_mean=True, with_std=True, copy=False)

# the histogram of the rescaled observation sequences

n, bins, patches = plt.hist(rescaled_boxcox_logDel, 50, normed=1, facecolor='green', alpha=0.75)

plt.show()

n, bins, patches = plt.hist(rescaled_logRet_5, 50, normed=1, facecolor='green', alpha=0.75)

plt.show()

n, bins, patches = plt.hist(rescaled_logVol_5, 50, normed=1, facecolor='green', alpha=0.75)

plt.show()

# Observation sequences matrix 
A = np.column_stack([logDel,logRet_5,logVol_5]) 

# Rescaled observation sequences matrix 
rescaled_A = np.column_stack([rescaled_boxcox_logDel, rescaled_logRet_5, rescaled_logVol_5])

# HMM modeling based on raw observation sequences

model = GaussianHMM(n_components= 3, covariance_type="full", n_iter=2000).fit([A])
hidden_states = model.predict(A)
hidden_states

# Plot the hidden states
plt.figure(figsize=(25, 18)) 
for i in range(model.n_components):
    pos = (hidden_states==i)
    plt.plot_date(Date[pos],close[pos],'o',label='hidden state %d'%i,lw=2)
    plt.legend(loc="left")

# Trading test according to the hidden states
for i in range(3):
    pos = (hidden_states==i)
    pos = np.append(0,pos[:-1])#第二天进行买入操作
    df = res.logRet_1
    res['state_ret%s'%i] = df.multiply(pos)
    plt.plot_date(Date,np.exp(res['state_ret%s'%i].cumsum()),'-',label='hidden state %d'%i)
    plt.legend(loc="left")

# Trading test2 according to the hidden states
long = (hidden_states==0)  #做多
short = (hidden_states == 1)  #做空
long = np.append(0,long[:-1]) #第二天才能操作
short = np.append(0,short[:-1]) #第二天才能操作

# Yield Curve
res['ret'] =  df.multiply(long) - df.multiply(short)  
plt.plot_date(Date,np.exp(res['ret'].cumsum()),'r-')

# HMM modeling based on processed observation sequences

rescaled_model = GaussianHMM(n_components= 3, covariance_type="full", n_iter=2000).fit([rescaled_A])
rescaled_hidden_states = rescaled_model.predict(rescaled_A)
rescaled_hidden_states

# Plot the hidden states
plt.figure(figsize=(25, 18)) 
for i in range(model.n_components):
    pos = (rescaled_hidden_states==i)
    plt.plot_date(Date[pos],close[pos],'o',label='hidden state %d'%i,lw=2)
    plt.legend(loc="left")

# Trading test according to the hidden states
for i in range(3):
    pos = (rescaled_hidden_states==i)
    pos = np.append(0,pos[:-1])#第二天进行买入操作
    df = res.logRet_1
    res['state_ret%s'%i] = df.multiply(pos)
    plt.plot_date(Date,np.exp(res['state_ret%s'%i].cumsum()),'-',label='hidden state %d'%i)
    plt.legend(loc="left")

# Trading test2 according to the hidden states
long = (rescaled_hidden_states==0)  #做多
short = (rescaled_hidden_states==1) + (rescaled_hidden_states == 2)  #做空
long = np.append(0,long[:-1]) #第二天才能操作
short = np.append(0,short[:-1]) #第二天才能操作

# Yield Curve
res['ret'] =  df.multiply(long) - df.multiply(short)  
plt.plot_date(Date,np.exp(res['ret'].cumsum()),'r-')

