# -*- coding: utf-8 -*-
"""退市列表"""

import akshare as ak
from funcat.utils import FuncatTestCase
from funcat.utils import DeList

__updated__ = "2021-05-31"


class TestDeList(FuncatTestCase):
    """获取证券交易所终止(暂停)上市股票"""

    def test_stock_info_sh_delist(self):
        df = DeList.stock_info_sh_delist()
        print(df[["COMPANY_CODE", "LISTING_DATE", "CHANGE_DATE"]])

    def test_stock_info_sz_delist(self):
        df = ak.stock_info_sz_delist(indicator="终止上市公司")
        print(df)
        print(df[["证券代码", "上市日期", "终止上市日期"]])


if __name__ == '__main__':
    FuncatTestCase.main()
