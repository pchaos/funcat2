# -*- coding: utf-8 -*-
import unittest

import numpy as np

from funcat.api import *
from funcat.conditional_selection import *
from funcat.utils import FuncatTestCase
# from funcat.context import ExecutionContext


class TestSelection(FuncatTestCase):
    @classmethod
    def setUp(cls) -> None:
        T("20210506")
        S("000001.XSHG")

    def test_bit_and(self):
        S("601636")
        T("20210506")
        start_date = 20210414
        set_start_date(start_date)
        DAYS = 3
        COND1 = (REF(C, DAYS - 1) / REF(C, DAYS) - 1)
        COND2 = (REF(C, DAYS - 2) / REF(C, DAYS - 1) - 1)
        COND3 = (REF(C, DAYS - 3) / REF(C, DAYS - 2) - 1)
        print(CLOSE.series)
        for i in range(1, DAYS + 1):
            print(DAYS - i, REF(CLOSE, DAYS - i).series[-10:])
        print((COND2 > COND1).series)
        print((COND3 > COND2).series)
        a = COND3 > COND2 & COND2 > COND1
        print("A, COND3 > COND2 & COND2 > COND1\n", a.series)
        b = COND3 > COND2 and COND2 > COND1
        print("B, COND3 > COND2 and COND2 > COND1\n", b.series)
        c = (COND3 > COND2) & (COND2 > COND1)
        print(f"只有这个是正确的\n", c.series)
        for i in range(1, len(b)):
            if b[i] != c[i]:
                print(f"数据不同步:-{i}, {b[i]} != {c[i]}")

    def test_hong_san_bing(self):
        S("601636")
        T("20210506")
        data = HSB()
        # print(hsb.series)
        self.assertTrue(len(data) > 0)

    def test_hong_san_bing2(self):
        # 旗滨集团 四月底～五月初有三红兵
        S("601636")
        T("20210506")
        start_date = 20210401
        set_start_date(start_date)
        data = HSB()
        print(data.series)
        print(CLOSE.series)
        print((CLOSE / REF(CLOSE, 1)).series)
        print((VOL / REF(VOL, 1)).series)
        self.assertTrue(len(data) > 0)
        print(data.series)

    def test_hong_san_bing_select(self):
        """搜索出来 旗滨集团 三星医疗 睿能科技
        [{'date': 20210506, 'code': '601567', 'cname': '三星医疗'}
         {'date': 20210506, 'code': '601636', 'cname': '旗滨集团'}
         {'date': 20210430, 'code': '603933', 'cname': '睿能科技'}]
        """
        order_book_id_list = self.BE.get_order_book_id_list()[3000:4000]
        # 选出红三兵
        data = select(HSB,
                      start_date=20210429,
                      end_date=20210506,
                      order_book_id_list=order_book_id_list)
        self.assertTrue(len(data) > 0, f"交易数据:{data}")

        print(data)

    def test_hong_san_bing_select2(self):
        """ 搜索出来
        [{'date': 20210506, 'code': '601567', 'cname': '三星医疗'}
         {'date': 20210506, 'code': '601636', 'cname': '旗滨集团'}
         {'date': 20210430, 'code': '603933', 'cname': '睿能科技'}
         {'date': 20210429, 'code': '000718', 'cname': '苏宁环球'}]
        """
        order_book_id_list = self.BE.get_order_book_id_list()
        # 选出红三兵
        data = select(HSB,
                      start_date=20210426,
                      end_date=20210506,
                      order_book_id_list=order_book_id_list)
        self.assertTrue(len(data) > 0, f"交易数据:{data}")

        print(data)

    def test_hong_san_bing_select3(self):
        """ 搜索出来
    [{'date': 20210416, 'code': '002738', 'cname': '中矿资源'}
     {'date': 20210416, 'code': '603721', 'cname': '中广天择'}
     {'date': 20210415, 'code': '000978', 'cname': '桂林旅游'}
     {'date': 20210415, 'code': '603721', 'cname': '中广天择'}
     {'date': 20210414, 'code': '600200', 'cname': '江苏吴中'}
     {'date': 20210413, 'code': '300268', 'cname': '佳沃股份'}]
        """
        from funcat.utils import FuncCounter
        order_book_id_list = self.BE.get_order_book_id_list()
        start, end = 20210413, 20210416
        # 选出红三兵
        data = select(HSB,
                      start_date=start,
                      end_date=end,
                      order_book_id_list=order_book_id_list)
        self.assertTrue(len(data) > 0, f"交易数据:{data}")

        print(data)
        print(f'计算红三兵需要调用get_bars({FuncCounter.instance().get("get_bars")})次')

    def test_hong_san_bing_select_index(self):
        """ 搜索出来
        [{'date': 20210222, 'code': '880036.XSHG', 'cname': '创业停板'}
         {'date': 20210218, 'code': '880325.XSHG', 'cname': '铜'}
         {'date': 20210210, 'code': '880325.XSHG', 'cname': '铜'}]
        """
        from funcat.utils import FuncCounter
        order_book_id_list = self.BE.get_order_book_id_list("index")
        start, end = 20210413, 20210516
        # 选出红三兵
        data = select(HSB,
                      start_date=start,
                      end_date=end,
                      order_book_id_list=order_book_id_list)
        self.assertTrue(len(data) > 0, f"交易数据:{data}")

        print(data)
        print(f'计算红三兵需要调用get_bars({FuncCounter.instance().get("get_bars")})次')

    def test_hong_san_bing_selectV(self):
        """ 搜索出来
        [{'date': 20210415, 'code': '000978', 'cname': '桂林旅游'}
         {'date': 20210416, 'code': '002738', 'cname': '中矿资源'}
         {'date': 20210413, 'code': '300268', 'cname': '佳沃股份'}
         {'date': 20210414, 'code': '600200', 'cname': '江苏吴中'}
         {'date': 20210415, 'code': '603721', 'cname': '中广天择'}
         {'date': 20210416, 'code': '603721', 'cname': '中广天择'}]
          216.536s
        """
        from funcat.utils import FuncCounter
        from funcat.helper import selectV
        order_book_id_list = self.BE.get_order_book_id_list("stock")
        start, end = 20210413, 20210416
        # 选出红三兵
        data = selectV(HSB,
                      start_date=start,
                      end_date=end,
                      order_book_id_list=order_book_id_list)
        self.assertTrue(len(data) > 0, f"交易数据:{data}")

        print(data)
        print(f'计算红三兵需要调用get_bars({FuncCounter.instance().get("get_bars")})次')
        
    def test_hong_san_bing_selectV_to_now(self):
        """ 20210401截止到当前时间搜索
        
[{'date': 20210408, 'code': '000056', 'cname': '皇庭国际'}
 {'date': 20210507, 'code': '000572', 'cname': 'ST海马'}
 {'date': 20210402, 'code': '000605', 'cname': '渤海股份'}
 {'date': 20210428, 'code': '000615', 'cname': '奥园美谷'}
 {'date': 20210406, 'code': '000620', 'cname': '新华联'}
 {'date': 20210407, 'code': '000620', 'cname': '新华联'}
 {'date': 20210407, 'code': '000632', 'cname': '三木集团'}
 {'date': 20210429, 'code': '000718', 'cname': '苏宁环球'}
 {'date': 20210430, 'code': '000718', 'cname': '苏宁环球'}
 {'date': 20210507, 'code': '000762', 'cname': '西藏矿业'}
 {'date': 20210409, 'code': '000825', 'cname': '太钢不锈'}
 {'date': 20210415, 'code': '000978', 'cname': '桂林旅游'}
 {'date': 20210406, 'code': '000993', 'cname': '闽东电力'}
 {'date': 20210409, 'code': '002053', 'cname': '云南能投'}
 {'date': 20210507, 'code': '002177', 'cname': '御银股份'}
 {'date': 20210409, 'code': '002378', 'cname': '章源钨业'}
 {'date': 20210420, 'code': '002413', 'cname': '雷科防务'}
 {'date': 20210408, 'code': '002490', 'cname': '山东墨龙'}
 {'date': 20210416, 'code': '002738', 'cname': '中矿资源'}
 {'date': 20210507, 'code': '002875', 'cname': '安奈儿'}
 {'date': 20210507, 'code': '002893', 'cname': '华通热力'}
 {'date': 20210420, 'code': '002997', 'cname': '瑞鹄模具'}
 {'date': 20210428, 'code': '003020', 'cname': '立方制药'}
 {'date': 20210409, 'code': '003025', 'cname': '思进智能'}
 {'date': 20210420, 'code': '003036', 'cname': '泰坦股份'}
 {'date': 20210422, 'code': '300061', 'cname': '旗天科技'}
 {'date': 20210429, 'code': '300222', 'cname': '科大智能'}
 {'date': 20210419, 'code': '300241', 'cname': '瑞丰光电'}
 {'date': 20210413, 'code': '300268', 'cname': '佳沃股份'}
 {'date': 20210420, 'code': '300302', 'cname': '同有科技'}
 {'date': 20210407, 'code': '300405', 'cname': '科隆股份'}
 {'date': 20210506, 'code': '300487', 'cname': '蓝晓科技'}
 {'date': 20210421, 'code': '300573', 'cname': '兴齐眼药'}
 {'date': 20210506, 'code': '300672', 'cname': '国科微'}
 {'date': 20210419, 'code': '300742', 'cname': '越博动力'}
 {'date': 20210407, 'code': '300840', 'cname': '酷特智能'}
 {'date': 20210421, 'code': '300896', 'cname': '爱美客'}
 {'date': 20210420, 'code': '600059', 'cname': '古越龙山'}
 {'date': 20210426, 'code': '600172', 'cname': '黄河旋风'}
 {'date': 20210414, 'code': '600200', 'cname': '江苏吴中'}
 {'date': 20210408, 'code': '600231', 'cname': '凌钢股份'}
 {'date': 20210420, 'code': '600623', 'cname': '华谊集团'}
 {'date': 20210419, 'code': '600769', 'cname': '祥龙电业'}
 {'date': 20210412, 'code': '600818', 'cname': '中路股份'}
 {'date': 20210412, 'code': '600896', 'cname': '*ST海医'}
 {'date': 20210506, 'code': '601567', 'cname': '三星医疗'}
 {'date': 20210506, 'code': '601636', 'cname': '旗滨集团'}
 {'date': 20210420, 'code': '601882', 'cname': '海天精工'}
 {'date': 20210419, 'code': '601890', 'cname': '亚星锚链'}
 {'date': 20210401, 'code': '603080', 'cname': '新疆火炬'}
 {'date': 20210422, 'code': '603198', 'cname': '迎驾贡酒'}
 {'date': 20210412, 'code': '603227', 'cname': '雪峰科技'}
 {'date': 20210423, 'code': '603260', 'cname': '合盛硅业'}
 {'date': 20210507, 'code': '603396', 'cname': '金辰股份'}
 {'date': 20210415, 'code': '603721', 'cname': '中广天择'}
 {'date': 20210416, 'code': '603721', 'cname': '中广天择'}
 {'date': 20210430, 'code': '603900', 'cname': '莱绅通灵'}
 {'date': 20210420, 'code': '603919', 'cname': '金徽酒'}
 {'date': 20210430, 'code': '603933', 'cname': '睿能科技'}
 {'date': 20210506, 'code': '603933', 'cname': '睿能科技'}
 {'date': 20210420, 'code': '688228', 'cname': '开普云'}
 {'date': 20210419, 'code': '688338', 'cname': '赛科希德'}
 {'date': 20210421, 'code': '688516', 'cname': '奥特维'}]
        """
        from funcat.utils import FuncCounter
        from funcat.helper import selectV
        order_book_id_list = self.BE.get_order_book_id_list("stock")
        start, end = 20210401, None
        # 选出红三兵
        data = selectV(HSB,
                      start_date=start,
                      end_date=end,
                      order_book_id_list=order_book_id_list)
        self.assertTrue(len(data) > 0, f"交易数据:{data}")

        print(data)
        print(f'计算红三兵需要调用get_bars({FuncCounter.instance().get("get_bars")})次; {FuncCounter.counter}')
        
    def test_hong_san_bing_selectV_index(self):
        """ 搜索出来

        """
        from funcat.utils import FuncCounter
        from funcat.helper import selectV
        order_book_id_list = self.BE.get_order_book_id_list("index")
        start, end = 20210413, 20210516
        # 选出红三兵
        data = selectV(HSB,
                      start_date=start,
                      end_date=end,
                      order_book_id_list=order_book_id_list)
        self.assertTrue(len(data) == 0, f"交易数据:{data}")

        print(data)
        print(f'计算红三兵需要调用get_bars({FuncCounter.instance().get("get_bars")})次; {FuncCounter.counter}')
        
    def test_hong_san_bing_selectV_etf(self):
        """ 搜索出来
        [{'date': 20210430, 'code': '167302.etf', 'cname': '湾区LOF'}]
        """
        from funcat.utils import FuncCounter
        from funcat.helper import selectV
        order_book_id_list = self.BE.get_order_book_id_list("etf")
        start, end = 20210413, 20210516
        # 选出红三兵
        data = selectV(HSB,
                      start_date=start,
                      end_date=end,
                      order_book_id_list=order_book_id_list)
        self.assertTrue(len(data) > 0, f"交易数据:{data}")

        print(data)
        print(f'计算红三兵需要调用get_bars({FuncCounter.instance().get("get_bars")})次; {FuncCounter.counter}')

    def test_hong_san_bing_counter(self):
        from funcat.utils import FuncCounter
        data = HSB()
        # print(hsb.series)
        self.assertTrue(len(data) > 0)
        print(f'计算一次红三兵需要调用get_bars({FuncCounter.instance().get("get_bars")})次')

    def test_chcount(self):
        from funcat.conditional_selection import CHCOUNT
        from funcat.utils import FuncCounter
        data = CHCOUNT()
        self.assertTrue(0 < data < 10, "指标空范围在1～9之间。计算值：{data}")
        print(f'计算一次红三兵需要调用get_bars({FuncCounter.instance().get("get_bars")})次; {FuncCounter.counter}')
        print(data.series)
        print(MA(data, 5).series)
        print(data.series[-10:])


if __name__ == '__main__':
    unittest.main()
