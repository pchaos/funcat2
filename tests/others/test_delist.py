# -*- coding: utf-8 -*-
"""退市列表"""

import akshare as ak
from funcat.utils import FuncatTestCase
from funcat.utils import DeList

__updated__ = "2021-06-01"


class TestDeList(FuncatTestCase):
    """获取证券交易所终止(暂停)上市股票"""

    def test_stock_info_sh_delist(self):
        df = DeList.stock_info_sh_delist()
        print(df[["code", "LISTING_DATE", "CHANGE_DATE"]])

    def test_stock_info_sz_delist(self):
        df = DeList.stock_info_sz_delist(indicator="终止上市公司")
        print(df)
        print(df[["code", "LISTING_DATE", "CHANGE_DATE"]])


if __name__ == '__main__':
    FuncatTestCase.main()
