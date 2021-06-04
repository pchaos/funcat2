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

    def test_stock_info(self):
        df = DeList.stock_info()
        print(df.head(20))
        print(f"code counts:{len(df)}")

    def test_stock_info_sh_name_code(self):
        df = DeList.stock_info_sh_name_code()
        self.assertTrue(len(df) > 1500, f"stock_info_sh_name_code: {len(df)}")
        print(df.head(10))

    def test_stock_info_sh_name_code_delist(self):
        df = DeList.stock_info_sh_name_code()
        df_delist = DeList.stock_info_sh_delist()
        codelist = df['code'].tolist()
        codelist_delist = df_delist['code'].tolist()
        print(codelist_delist)
        for i in range(len(codelist_delist)):
            self.assertFalse(
                codelist_delist[i] in codelist, f"{codelist_delist[i]}")

    def test_stock_info_sz_name_code(self):
        df = DeList.stock_info_sz_name_code()
        self.assertTrue(len(df) > 2000, f"stock_info_sh_name_code: {len(df)}")

    def test_stock_info_code(self):
        df1 = DeList.stock_info_sh_name_code()
        df2 = DeList.stock_info_sz_name_code()
        df = df1.append(df2)
        self.assertTrue(len(df) == len(df1) + len(df2),
                        f"{len(df)} == {len(df1)} + {len(df2)}")
        print(f"{len(df)} == {len(df1)} + {len(df2)}")

    def test_(self):
        """list_status    str    N    上市状态 L上市 D退市 P暂停上市，默认是L"""
        ts.pro_api().stock_basic(exchange='', list_status='D').set_index('symbol', drop=True)


if __name__ == '__main__':
    FuncatTestCase.main()
