# -*- coding: utf-8 -*-
"""退市列表"""

from functools import lru_cache
# from functools import cached_property
import akshare as ak

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
        return df
