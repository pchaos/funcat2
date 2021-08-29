# -*- coding: utf-8 -*-

import pandas as pd
import pymongo
import QUANTAXIS as QA
from QUANTAXIS.QAUtil.QAParameter import MARKET_TYPE

from qaenv import (eventmq_amqp, eventmq_ip, eventmq_password, eventmq_port,
                   eventmq_username, mongo_ip, mongo_uri)
#  from QARisk import QA_Risk
from qastockbase_etf import QAStrategyStockBase
from QAUser import QA_User


class Strategy(QAStrategyStockBase):
    def debug(self):
        self.running_mode = 'backtest'
        self.database = pymongo.MongoClient(mongo_ip).QUANTAXIS
        user = QA_User(username="admin", password='admin')
        port = user.new_portfolio(self.portfolio)
        self.acc = port.new_accountpro(
            account_cookie=self.strategy_id, init_cash=self.init_cash, market_type=self.market_type, frequence= self.frequence)
        #self.positions = self.acc.get_position(self.code)

        print(self.acc)

        print(self.acc.market_type)
        data = QA.QA_quotation(self.code, self.start, self.end, source=QA.DATASOURCE.MONGO,
                               frequence=self.frequence, market=self.market_type, output=QA.OUTPUT_FORMAT.DATASTRUCT)
        #挑选符合条件的历史时点数据
        df=data.data
        df.reset_index(inplace=True)
        df=df.assign(time=df.datetime.apply(lambda x:str(x)[11:]))
        df=df.loc[df.time=='14:30:00'].set_index(['datetime','code'])
        data.data=df
        print('回测数据：')
        print(data.data)
        data.data.apply(self.x1, axis=1)

    def on_bar(self,data):
        #print('*'*10)
        #print(data)
        #print(self.get_positions(data.name[1]))
        # print(self.market_data)
        if len(self.get_current_marketdata())==len(self.code) and str(self.market_datetime[-1])[11:]=='14:30:00':
            print('当前时间：')
            print(self.market_datetime[-1])
            
            df=QA.QA_DataStruct_Index_min(self.market_data)
            
            ind=df.add_func(select_etf)
            
            time_data=ind[-len(self.code):].sort_values(by='change')
            # print(time_data)
            code=time_data.iloc[-1].name[1]
            # print('排名第一的是：',code)
            price=self.get_current_marketdata().loc[(slice(None),time_data.iloc[-1].name[1]),'close'][0]
            # print('价格为：',price)
            # print('排序最大值：')
            # print(time_data.max()[0])
            print('当前持仓：')
            print(self.acc.hold_available)
            if time_data.max()[0]>0:
                if len(self.acc.hold_available)==0:# 如果没有持仓，买入排名第一的股票
                    print('可用资金：',self.acc.cash_available)
                    # self.send_order('BUY','OPEN',code=code,price=price,volume=10000)
                    money=self.acc.cash_available
                    self.send_order('BUY','OPEN',code=code,price=price,volume=get_volume_buy(price=price,money=money))
                elif self.acc.get_position(code).volume_long !=0:#如果持仓标的继续排名第一，则继续持有
                    print('持仓标的持续强势，继续持有！')
                else:
                    temp_s=self.acc.hold_available
                    code_sell=temp_s.index[0]
                    # print(code_sell)
                    price_sell=self.get_current_marketdata().loc[(slice(None),code_sell),'close'][0]
                    # print('卖出持仓，买入强势股')
                    # print('调仓前可用资金：',self.acc.cash_available)
                    self.send_order('SELL','CLOSE',code=code_sell,price=price_sell,volume=int(temp_s.loc[code_sell]))#卖出的时候 数量要加int
                    # print('调仓前卖出股票后可用资金：',self.acc.cash_available)
                    # self.send_order('BUY','OPEN',code=code,price=price,volume=10000)
                    money=self.acc.cash_available
                    self.send_order('BUY','OPEN',code=code,price=price,volume=get_volume_buy(price=price,money=money))
            else:
                if len(self.acc.hold_available)!=0:# 如果有持仓，卖出所有的股票
                    temp_s=self.acc.hold_available
                    code_sell=temp_s.index[0]
                    print(code_sell)
                    price_sell=self.get_current_marketdata().loc[(slice(None),code_sell),'close'][0]
                    print('所有标的均下跌，清仓！！！！')
                    # print('调仓前可用资金：',self.acc.cash_available)
                    self.send_order('SELL','CLOSE',code=code_sell,price=price_sell,volume=int(temp_s.loc[code_sell]))#卖出的时候 数量要加int
                    # print('调仓后可用资金：',self.acc.cash_available)
                else:
                    print('所有标的均下跌，暂不买入')
        print('当日持仓：')
        print(self.acc.hold_available)   
def get_volume_buy(price,money):
    """ 计算可买数量，这里考虑到手续费和税的问题，所有只用98%的可用资金"""
    volume=int(money*0.98/price//100100)
    return volume

def select_etf(data):
    """因为前面已经做了历史数据筛选，这里只需要按天计算长度就可以了"""
    close=data.close
    change=close.pct_change(5)
    return(pd.DataFrame({'change':change}))

if name == "main":
    code=[ '510500','159915','510300']

    s=Strategy(code, frequence='30min', start='2018-07-14', end='2020-07-10',market_type=MARKET_TYPE.INDEX_CN, strategy_id='rank_etf_30min_now_1c')

    data=QA.QA_fetch_index_min_adv(code,'2018-07-04','2018-07-13','30min').data
    df=data.reset_index()
    df=df.assign(time=df.datetime.apply(lambda x:str(x)[11:]))
    data=df.loc[df.time=='14:30:00'].set_index(['datetime','code'])
    print('历史追加数据：')
    print(data)
    s._market_data=[data.iloc[i] for i in range(len(data))]
    s.run_backtest()
