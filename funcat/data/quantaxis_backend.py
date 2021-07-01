# -*- coding: utf-8 -*-
import pandas as pd
from cached_property import cached_property
from functools import lru_cache

from .backend import DataBackend
from ..utils import get_str_date_from_int, get_int_date

__updated__ = "2021-06-30"


class QuantaxisDataBackend(DataBackend):

    @cached_property
    def backend(self):
        try:
            import QUANTAXIS as qa
            return qa
        except ImportError:
            print("-" * 50)
            print(">>> Missing QUANTAXIS. Please run `pip install quantaxis`")
            print("-" * 50)
            raise

    @cached_property
    def stock_basics(self):
        df_index = self.backend.QA_fetch_index_list_adv()
        df_index["code"] = df_index["code"] + \
            df_index["sse"].apply(lambda x: ".XSHG" if x == "sh" else ".XSHE")
        df_etf = self.backend.QA_fetch_etf_list()
        df_etf["code"] = df_etf["code"].apply(lambda x: f"{x}.etf")

        return pd.concat([self.backend.QA_fetch_stock_list_adv(), df_index, df_etf])
        # return self.backend.QAFetch.QATdx.QA_fetch_get_stock_list('stock')

    @cached_property
    def code_name_map(self):
        code_name_map = self.stock_basics[["name"]].to_dict()["name"]
        return code_name_map

    def convert_code(self, order_book_id):
        return order_book_id.split(".")[0]

    @lru_cache(maxsize=6000)
    def get_price(self, order_book_id, start, end, freq, is_index=False):
        """
        :param order_book_id: e.g. 000002
        :param start: 20160101
        :param end: 20160201
        :param is_index: 默认为False：查询股票
        :returns:
        :rtype: numpy.rec.array
        """
        # if order_book_id.endswith(".XSHG") or
        # order_book_id.endswith(".XSHE"):
        if len(order_book_id) > 6:
            # 判断指数
            is_index = True
        try:
            if is_index:
                data = self.get_index_price(order_book_id, start, end, freq)
            else:
                data = self.get_stock_price(order_book_id, start, end, freq)

            if freq == "W":
                df = data.week.rename(columns={"vol": "volume"})
            elif freq == "M":
                df = data.month.rename(columns={"vol": "volume"})
            else:
                df = data.data
        except Exception:
            return pd.DataFrame().to_records()
        if freq[-1] == "m":
            df["datetime"] = df.apply(
                lambda row: int(row["date"].split(" ")[0].replace("-", "")) * 1000000 + int(
                    row["date"].split(" ")[1].replace(":", "")) * 100, axis=1)
        elif freq in ("1d", "W", "M"):
            dt = df.index.levels[0].to_list()
            df["date"] = pd.DataFrame(
                {"datetime": [f"{dt[i]:%Y-%m-%d}" for i in range(len(dt))]}, index=df.index)
            df["datetime"] = pd.DataFrame({"datetime": [1000000 * (10000 * dt[i].year + 100 * dt[i].month + dt[i].day)
                                                        for i in range(len(dt))]}, index=df.index)
            # df["datetime"] = df["date"].apply(lambda x: int(x.replace("-", "")) * 1000000)
            # df.reset_index(drop=False, inplace=True)
            # del df["code"]
            df = df[['date', 'open', 'close', 'high', 'low', 'volume', 'datetime']]
            df.reset_index(drop=True, inplace=True)
            # getprice字段：Index(['date', 'open', 'close', 'high', 'low', 'volume', 'datetime'], dtype='object')
            # print(f"quantaxis getprice字段：{df.columns}")
            result_records = df.to_records()
        return result_records

    # @lru_cache(maxsize=4096)
    def get_stock_price(self, order_book_id, start, end, freq):
        """
        :param order_book_id: e.g. 000002
        :param start: 20160101
        :param end: 20160201
        :returns:
        :rtype: numpy.rec.array
        """
        start = get_str_date_from_int(start)
        end = get_str_date_from_int(end)
        code = self.convert_code(order_book_id)
        ktype = freq
        if freq[-1] == "m":
            ktype = freq[:-1]
        elif freq == "1d":
            ktype = "D"
        # else W M
        return self.backend.QA_fetch_stock_day_adv(code, start=start, end=end)

    # @lru_cache(maxsize=4096)
    def get_index_price(self, order_book_id, start, end, freq):
        """
        :param order_book_id: e.g. 000002
        :param start: 20160101
        :param end: 20160201
        :returns:
        :rtype: numpy.rec.array
        """
        start = get_str_date_from_int(start)
        end = get_str_date_from_int(end)
        code = self.convert_code(order_book_id)
        ktype = freq
        if freq[-1] == "m":
            ktype = freq[:-1]
        elif freq == "1d":
            ktype = "D"
        return self.backend.QA_fetch_index_day_adv(code, start=start, end=end)

    @lru_cache()
    def get_order_book_id_list(self, code_type="stock") -> list:
        """获取股票代码列表
        Args:
            code_type (str): 代码类型;取值范围： "stock, "etf", "index", "all";
                                    分别对应： 股票， etf， 指数， 全部
        Returns:
            类型code_type对应的代码列表
        """

        code_types = {"stock": lambda x: len(x) == 6,
                      "etf": lambda x: x.endswith(".etf"),
                      "index": lambda x: x.endswith(".XSH", 5, -1),
                      "all": lambda x: True,
                      "none": lambda x: False}
        info = self.stock_basics
        if code_type:
            info = info[info["code"].apply(code_types.get(code_type.lower(),
                                                          code_types.get("none")))]
        code_list = info.index.sort_values().to_list()
        order_book_id_list = [
            code for code in code_list
        ]
        return order_book_id_list

    @lru_cache(maxsize=100)
    def get_trading_dates(self, start, end, order_book_id="000001.XSHG") -> list:
        """获取所有的交易日
        Args:
            start: 20160101
            end: 20160201
            order_book_id: stock code;默认为上证指数 "000001.XSHG"
        Returns:
            股票（order_book_id）start~end时间段内交易日期列表
        """
        start = get_str_date_from_int(start)
        end = get_str_date_from_int(end)
        df = self.get_price(order_book_id, start, end, "1d")
        if len(df) == 0:
              # 提示数据库可能无数据
            print(f"maybe your data is empty, please check it. {order_book_id}:{start}~{end}")
        trading_dates = [get_int_date(date) for date in df.date.tolist()]
        return trading_dates

    @lru_cache(maxsize=6000)
    def symbol(self, order_book_id):
        """获取order_book_id对应的名字
        :param order_book_id str: 股票代码
        :returns: 名字
        :rtype: str
        """
        # code = self.convert_code(order_book_id)
        # todo 转化etf index
        return f'{self.code_name_map.get(order_book_id)}'
        # return f'{self.code_name_map.get((code, "sz"), self.code_name_map.get((code, "sh")))}'
        # return "{}[{}]".format(order_book_id, self.code_name_map.get((code,
        # "sz"), self.code_name_map.get((code, "sh"))))

    def finacial(self, n: int):
        """todo 获取专业金融数据
         """
        res = self.backend().QA_fetch_financial_report(['000001', '600100'], [
            '2017-03-31', '2017-06-30', '2017-09-31', '2017-12-31', '2018-03-31'])
        return res
