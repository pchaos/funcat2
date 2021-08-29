# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np

__updated__ = "2021-08-29"


class DataBackend(object):
    skip_suspended = True

    def get_price(self, order_book_id, start, end, freq):
        """
        :param order_book_id: e.g. 000002.XSHE
        :param start: 20160101
        :param end: 20160201
        :param freq: 1m 1d 5m 15m ...
        :returns:
        :rtype: numpy.rec.array
        """
        raise NotImplementedError

    def get_order_book_id_list(self):
        """获取所有的
        """
        raise NotImplementedError

    def get_trading_dates(self, start, end):
        """获取所有的交易日

        :param start: 20160101
        :param end: 20160201
        """
        raise NotImplementedError

    def symbol(self, order_book_id):
        """获取order_book_id对应的名字
        :param order_book_id str: 股票代码
        :returns: 名字
        :rtype: str
        """
        raise NotImplementedError

    def get_dataFrames(self, codes, start, end, freq):
        """返回pd.dataFrame格式
        """
        if not isinstance(codes, list):
            codes = [codes]
        dfs = []
        for code in codes:
            data = self.get_price(code, start, end, freq)
            dfs.append(pd.DataFrame(data)[[
                       'open', 'close', 'high', 'low', 'volume', 'datetime']])
        return dfs
