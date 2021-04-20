# -*- coding: utf-8 -*-

from cached_property import cached_property

from .backend import DataBackend
from ..utils import lru_cache, get_str_date_from_int, get_int_date


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
        return self.backend.QAFetch.QATdx.QA_fetch_get_stock_list('stock')

    @cached_property
    def code_name_map(self):
        code_name_map = self.stock_basics[["name"]].to_dict()["name"]
        return code_name_map

    def convert_code(self, order_book_id):
        return order_book_id.split(".")[0]

    @lru_cache(maxsize=4096)
    def get_price(self, order_book_id, start, end, freq):
        """
        :param order_book_id: e.g. 000002.XSHE
        :param start: 20160101
        :param end: 20160201
        :returns:
        :rtype: numpy.rec.array
        """
        start = get_str_date_from_int(start)
        end = get_str_date_from_int(end)
        code = self.convert_code(order_book_id)
        is_index = False
        if ((order_book_id.startswith("0") and order_book_id.endswith(".XSHG")) or
                (order_book_id.startswith("3") and order_book_id.endswith(".XSHE"))
        ):
            is_index = True
        ktype = freq
        if freq[-1] == "m":
            ktype = freq[:-1]
        elif freq == "1d":
            ktype = "D"
        # else W M

        df = self.ts.get_k_data(code, start=start, end=end, index=is_index, ktype=ktype)

        if freq[-1] == "m":
            df["datetime"] = df.apply(
                lambda row: int(row["date"].split(" ")[0].replace("-", "")) * 1000000 + int(
                    row["date"].split(" ")[1].replace(":", "")) * 100, axis=1)
        elif freq in ("1d", "W", "M"):
            df["datetime"] = df["date"].apply(lambda x: int(x.replace("-", "")) * 1000000)

        del df["code"]
        arr = df.to_records()

        return arr

    @lru_cache()
    def get_order_book_id_list(self):
        """获取所有的股票代码列表
        """
        # info = self.backend.get_stock_basics()
        info = self.stock_basics
        code_list = info.index.sort_values().tolist()
        order_book_id_list = [
           code for code, _ in code_list
        ]
        return order_book_id_list

    @lru_cache()
    def get_trading_dates(self, start, end):
        """获取所有的交易日

        :param start: 20160101
        :param end: 20160201
        """
        start = get_str_date_from_int(start)
        end = get_str_date_from_int(end)
        df = self.backend.QAFetch.QATdx.QA_fetch_get_index_day('000001',start,end)
        trading_dates = [get_int_date(date) for date in df.date.tolist()]
        return trading_dates

    @lru_cache(maxsize=4096)
    def symbol(self, order_book_id):
        """获取order_book_id对应的名字
        :param order_book_id str: 股票代码
        :returns: 名字
        :rtype: str
        """
        code = self.convert_code(order_book_id)
        return "{}[{}]".format(order_book_id, self.code_name_map.get(code))
