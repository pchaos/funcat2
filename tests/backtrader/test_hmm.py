# -*- coding: utf-8 -*-

from hmmlearn.hmm import GaussianHMM
import datetime
import numpy as np
from matplotlib import cm, pyplot as plt
import matplotlib.dates as dates
import pandas as pd
import seaborn as sns

import unittest
import numpy as np
import backtrader as bt
from funcat.api import *
from funcat.conditional_selection import *
from funcat.utils import FuncatTestCase

__updated__ = "2021-07-25"

class TestHMM(FuncatTestCase):
    @classmethod
    def setUp(cls) -> None:
        T("20210506")
        S("000001.XSHG")

    def test_hmm(self):
        sns.set_style('white')

        beginDate = '20100401'
        endDate = '20160317'
        data = DataAPI.MktIdxdGet(ticker='000001',beginDate=beginDate,endDate=endDate,field=['tradeDate','closeIndex','lowestIndex','highestIndex','turnoverVol'],pandas="1")
        data1 = DataAPI.FstTotalGet(exchangeCD=u"XSHE",beginDate=beginDate,endDate=endDate,field=['tradeVal'],pandas="1")
        data2 = DataAPI.FstTotalGet(exchangeCD=u"XSHG",beginDate=beginDate,endDate=endDate,field=['tradeVal'],pandas="1")
        tradeVal = data1 + data2
        tradeDate = pd.to_datetime(data['tradeDate'][5:])
        volume = data['turnoverVol'][5:]
        closeIndex = data['closeIndex']
        deltaIndex = np.log(np.array(data['highestIndex'])) - np.log(np.array(data['lowestIndex']))
        deltaIndex = deltaIndex[5:]
        logReturn1 = np.array(np.diff(np.log(closeIndex)))
        logReturn1 = logReturn1[4:]
        logReturn5 = np.log(np.array(closeIndex[5:])) - np.log(np.array(closeIndex[:-5]))
        logReturnFst = np.array(np.diff(np.log(tradeVal['tradeVal'])))[4:]
        closeIndex = closeIndex[5:]
        X = np.column_stack([logReturn1,logReturn5,deltaIndex,volume,logReturnFst])

        # Make an HMM instance and execute fit
        model = GaussianHMM(n_components=6, covariance_type="diag", n_iter=1000).fit([X])
        # Predict the optimal sequence of internal hidden state
        hidden_states = model.predict(X)

        #print("Transition matrix")
        #print(model.transmat_)
        #print()

        #print("Means and vars of each hidden state")
        #for i in range(model.n_components):
        #    print("{0}th hidden state".format(i))
        #    print("mean = ", model.means_[i])
        #    print("var = ", np.diag(model.covars_[i]))
            
        plt.figure(figsize=(15, 8))  
        for i in range(model.n_components):
            idx = (hidden_states==i)
            plt.plot_date(tradeDate[idx],closeIndex[idx],'.',label='%dth hidden state'%i,lw=1)
            plt.legend()
            plt.grid(1)

if __name__ == '__main__':
    unittest.main()


