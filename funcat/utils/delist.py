# -*- coding: utf-8 -*-
"""退市列表"""

from functools import lru_cache
# from functools import cached_property
import akshare as ak
from funcat.context import ExecutionContext

__updated__ = "2021-06-01"


class DeList():
    """获取证券交易所终止(暂停)上市股票"""

    @classmethod
    def stock_info_sh_delist(cls, indicator="终止上市公司"):
        """
        获取上海证券交易所终止(暂停)上市股票
        :param indicator: indicator="终止上市公司"; choice of {"暂停上市公司", "终止上市公司"}
        """
        df = ak.stock_info_sh_delist(indicator)
        # print(df)
        df = df[["COMPANY_CODE", "LISTING_DATE", "CHANGE_DATE"]]
        df.columns = ["code", "LISTING_DATE", "CHANGE_DATE"]
        df.sort_values(by=['code'], inplace=True)
        return df

    @classmethod
    def stock_info_sz_delist(cls, indicator="终止上市公司"):
        """获取上海证券交易所终止(暂停)上市股票
        :param indicator: indicator="终止上市公司"; choice of {"暂停上市公司", "终止上市公司"}
        """

        df = ak.stock_info_sz_delist(indicator)
        # print(df)
        df = df[["证券代码", "上市日期", "终止上市日期"]]
        df.columns = ["code", "LISTING_DATE", "CHANGE_DATE"]
        df.sort_values(by=['code'], inplace=True)
        return df

    @classmethod
    def stock_info_sh_name_code(cls, indicator="主板A股"):
        """获取上证证券交易所股票代码和简称数据;不包含退市代码
        :param indicator: indicator="主板A股"; choice of {"主板A股", "主板B股", "科创板"}
        """
        df = ak.stock_info_sh_name_code(indicator)
        df = df[["COMPANY_CODE", "LISTING_DATE", "CHANGE_DATE"]]
        df.columns = ["code", "LISTING_DATE", "CHANGE_DATE"]
        # print(df.columns)
        # print(df.head(10))
        return df

    @classmethod
    def stock_info_sz_name_code(cls, indicator="A股列表"):
        """获取深证证券交易所股票代码和简称数据;不包含退市代码
        :param indicator: indicator="A股列表"; choice of {"A股列表", "B股列表", "CDR列表", "AB股列表"}
        """
        df = ak.stock_info_sz_name_code(indicator)
        df = df[["A股代码", "A股上市日期"]]
        df["终止上市日期"] = '-'
        df.columns = ["code", "LISTING_DATE", "CHANGE_DATE"]
        print(df.columns)
        print(df.head(10))
        return df

    @classmethod
    def stock_info(cls):
        data_backend = ExecutionContext.get_data_backend()
        stock_basics = data_backend.stock_basics
        print(stock_basics.columns)
        # print(stock_basics.head(10))
        return stock_basics
