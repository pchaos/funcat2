# -*- coding: utf-8 -*-
"""退市列表"""

from functools import lru_cache
# from functools import cached_property
import akshare as ak

__updated__ = "2021-05-31"


class DeList():
    """获取证券交易所终止(暂停)上市股票"""

    @classmethod
    def stock_info_sh_delist(cls, indicator="终止上市公司"):
        """
        获取上海证券交易所终止(暂停)上市股票
        :param indicator: indicator="终止上市公司"; choice of {"暂停上市公司", "终止上市公司"}
        """
        df = ak.stock_info_sh_delist(indicator="终止上市公司")
        print(df)
        return df[["COMPANY_CODE", "LISTING_DATE", "CHANGE_DATE"]]

    @classmethod
    def stock_info_sz_delist(cls, indicator="终止上市公司"):
        """获取上海证券交易所终止(暂停)上市股票
        :param indicator: indicator="终止上市公司"; choice of {"暂停上市公司", "终止上市公司"}
        """

        df = ak.stock_info_sz_delist(indicator="终止上市公司")
        print(df)
        return df[["证券代码", "上市日期", "终止上市日期"]]
