# -*- coding: utf-8 -*-
import unittest
from matplotlib import rcParams
import matplotlib.pyplot as plt
import numpy as np
# from pprint import pprint as print
from funcat import *
from funcat.api import *
from funcat.context import ExecutionContext
from funcat.helper import selectV
from funcat.utils import FuncatTestCase


class TestFuncat2TestCase(FuncatTestCase):

    @classmethod
    def setUpClass(cls) -> None:
        set_data_backend(QuantaxisDataBackend())
        cls.qdb = QuantaxisDataBackend()
        T("20201216")
        S("000001.XSHG")

    @classmethod
    def setUp(self) -> None:
        T("20201216")
        S("000001.XSHG")

    def test_select(self):
        # 选出涨停股
        data = select(
            lambda: C / C[1] - 1 >= 0.0995,
            start_date=20181231,
            end_date=20190104,
        )
        self.assertTrue(len(data) > 10, f"涨停股:{data}")

    def test_select2(self):
        # 选出涨停股
        data = select(
            lambda: C / REF(C, 1) - 1 >= 0.0995,
            start_date=20181231,
            end_date=20190104,
        )
        self.assertTrue(len(data) > 10, f"涨停股:{data}")

    def test_select3(self):
        # 选出最近30天K线实体最高价最低价差7%以内，最近100天K线实体最高价最低价差25%以内，
        # 最近10天，收盘价大于60日均线的天数大于3天
        n8 = "20180201"  # 开始时间
        print("手动设定选股开始时间格式n8", n8)
        n9 = "20180201"  # 结束时间
        print("手动设定选股结束时间格式n9", n9)
        select(
            lambda: ((HHV(MAX(C, O), 30) / LLV(MIN(C, O), 30) - 1 < 0.07)
                     & (HHV(MAX(C, O), 100) / LLV(MIN(C, O), 100) - 1 > 0.25)
                     & (COUNT(C > MA(C, 60), 10) > 3)),
            start_date=(n8),
            end_date=(n9),
        )

    def test_select4(self):
        # 选出最近3天每天的成交量小于20日成交量均线，最近3天最低价低于20日均线，最高价高于20日均线
        # 自定义选股回调函数
        n8 = "20180201"  # 开始时间
        print("手动设定选股开始时间格式n8", n8)
        n9 = "20180201"  # 结束时间
        print("手动设定选股结束时间格式n9", n9)

        def callback(date, order_book_id, symbol):
            print("Cool, 在", date, "选出", order_book_id, symbol)

        select(
            lambda:
            (EVERY(V < MA(V, 20) / 2, 3) & EVERY(L < MA(C, 20), 3) & EVERY(
                H > MA(C, 20), 3)),
            start_date=(n8),
            end_date=(n9),
            callback=callback,
        )

    def test_CLOSE(self):
        data_backend = ExecutionContext.get_data_backend()
        order_book_id_list = data_backend.get_order_book_id_list()[150:300]
        # 选出涨停股
        data = select(lambda: C > 50,
                      start_date=20181228,
                      end_date=20190104,
                      order_book_id_list=order_book_id_list)
        self.assertTrue(len(data) > 0, f"交易数据:{data}")
        print(data)

    def test_CLOSE_asyn(self):
        data_backend = ExecutionContext.get_data_backend()
        order_book_id_list = data_backend.get_order_book_id_list()[150:300]
        # 选出涨停股
        data = selectAsync(lambda: C > 50,
                           start_date=20181228,
                           end_date=20190104,
                           order_book_id_list=order_book_id_list)
        self.assertTrue(len(data) > 0, f"交易数据:{data}")
        print(data)

    def test_CLOSE_select2(self):
        data_backend = ExecutionContext.get_data_backend()
        order_book_id_list = data_backend.get_order_book_id_list()[150:300]
        # 选出涨停股
        data = select2(lambda: C > 40,
                       start_date=20181228,
                       end_date=20190104,
                       order_book_id_list=order_book_id_list)
        self.assertTrue(len(data) > 0, f"交易数据:{data}")
        print(data)

    def test_CLOSE_select2_2(self):
        data_backend = ExecutionContext.get_data_backend()
        order_book_id_list = data_backend.get_order_book_id_list()[150:300]
        # 选出涨停股
        data = select2(lambda: 30 > C > 20,
                       start_date=20181228,
                       end_date=20190104,
                       order_book_id_list=order_book_id_list)
        self.assertTrue(len(data) > 0, f"交易数据:{data}")
        print(data)
        for item in range(len(data)):
            for k, v in data[item].items():
                print(k, v, end=";")
            print("")

    def test_cross(self):
        # 0x02 均线金叉死叉
        ax = plt.subplot()
        ma1 = MA(L, 1)
        ma3 = MA(H, 3)
        ma5 = MA(H, 5)
        ma7 = MA(H, 7)
        ma11 = MA(H, 11)
        ma22 = MA(H, 22)
        ma66 = MA(H, 66)
        buy_signal = CROSS(ma1, ma7)
        sell_signal = CROSS(ma7, ma1)
        plt.plot(C.series, label="H", linewidth=2)
        plt.plot(ma1.series, label="ma1", alpha=0.7)
        plt.plot(ma3.series, label="ma3", alpha=0.7)
        plt.plot(ma5.series, label="ma5", alpha=0.7)
        plt.plot(ma7.series, label="ma7", alpha=0.7)
        plt.plot(ma11.series, label="ma11", alpha=0.7)
        plt.plot(ma22.series, label="ma22", alpha=0.7)
        plt.plot(ma66.series, label="ma66", alpha=0.7)
        plt.plot(np.where(buy_signal.series)[0],
                 C.series[np.where(buy_signal.series)[0]],
                 "^",
                 label="buy",
                 markersize=12,
                 color="red")
        plt.plot(np.where(sell_signal.series)[0],
                 C.series[np.where(sell_signal.series)[0]],
                 "v",
                 label="sell",
                 markersize=12,
                 color="green")
        plt.legend(loc="best")
        plt.show()

    def test_rsv(self):
        N, M1, M2 = 27, 9, 3
        RSV = (CLOSE - LLV(LOW, N)) / (HHV(HIGH, N) - LLV(LOW, N)) * 100
        K = EMA(RSV, (M1 * 2 - 1))
        D = EMA(K, (M2 * 2 - 1))
        J = K * 3 - D * 2
        print(K, D, J)
        f, (
            ax1,
            ax2,
        ) = plt.subplots(2, 1)
        ax1.plot(L.series, label="L")
        ax1.plot(MA(L, 7).series, label="ma7")
        ax1.plot(MA(H, 11).series, label="ma11")
        ax1.plot(MA(H, 22).series, label="ma22")
        ax1.plot(MA(H, 66).series, label="ma66")
        ax1.set_xlim(22)
        ax2.plot(K.series, label="K", linewidth=2)
        ax2.plot(D.series, label="D", alpha=0.7)
        ax2.plot(J.series, label="J", alpha=0.7)
        ax2.set_xlim(22)
        buy_signal = CROSS(J, K)
        sell_signal = CROSS(K, J)
        plt.plot(np.where(buy_signal.series)[0],
                 K.series[np.where(buy_signal.series)[0]],
                 "^",
                 label="buy",
                 markersize=12,
                 color="red")
        plt.plot(np.where(sell_signal.series)[0],
                 J.series[np.where(sell_signal.series)[0]],
                 "v",
                 label="sell",
                 markersize=12,
                 color="green")
        plt.legend(loc="best")
        plt.show()

    def test_callback(self):

        # 选出最近3天每天的成交量小于20日成交量均线，最近3天最低价低于20日均线，最高价高于20日均线
        # 自定义选股回调函数
        def callback(date, order_book_id, symbol):
            print("Cool, 在", date, "选出", order_book_id, symbol)

        data = select(
            lambda:
            (EVERY(V < MA(V, 20) / 2, 3) & EVERY(L < MA(C, 20), 3) & EVERY(
                H > MA(C, 20), 3)),
            start_date=20170104,
            end_date=20170104,
            callback=callback,
        )
        print(data)

    def test_callback2(self):

        # 使用函数方式测试select
        # 自定义选股回调函数
        def callback(date, order_book_id, symbol):
            print("Cool, 在", date, "选出", order_book_id, symbol)

        def myfunc():
            return (EVERY(V < MA(V, 20) / 2, 3) & EVERY(L < MA(C, 20), 3)
                    & EVERY(H > MA(C, 20), 3))

        data = select(
            myfunc,
            start_date=20170104,
            end_date=20170104,
            callback=callback,
        )
        data2 = select(
            lambda:
            (EVERY(V < MA(V, 20) / 2, 3) & EVERY(L < MA(C, 20), 3) & EVERY(
                H > MA(C, 20), 3)),
            start_date=20170104,
            end_date=20170104,
            callback=callback,
        )
        self.assertTrue(np.alltrue(data == data2), f"{data}\n{data2}")
        print(data)

    def test_user_func(self):
        # 选出豹子价格

        def myfunc():
            """检测豹子价格;
            例如：6.66 4.44， 77.77
            """

            def baozi(price):
                s = f"{np.round(price.value, 2):.2f}".replace(".", "")
                arr = np.fromiter(s, dtype=int)
                for i in range(1, len(arr)):
                    if arr[0] != arr[i]:
                        return False
                return True
                # return arr[0] == arr[1] and arr[-2] == arr[-1] and arr[0] == arr[-1] and (np.sum(arr) / arr[1]) == len(arr)

            return baozi(CLOSE) or baozi(LOW) or baozi(HIGH)

        data = selectAsync(
            myfunc,
            start_date=20210423,
            end_date=20210427,
        )
        print(f"豹子价：{data}")

    def test_2nd_stag(self):
        """当前股价处在50日、150日和200日线上方；
        50日线＞150日线＞200日线；
        200日均线至少上涨了1个月（大多数情况下，上涨4-5个月更好）；
        股价比最近一年最低价至少高30%，至少处在最近一年最高价的75%，距离最高价越近越好；
        交易量较大的几周中，上涨的交易周数量高于下跌的；
        RPS不低于70，最好80、90左右。
        RPS指标又称为股价相对强度指标，是由美国的欧奈尔提出，并运用于市场的分析的。RPS指标是指在一段时间内，个股涨幅在全部股票涨幅排名中的位次值，可通过官方资料得知。
        
        [{'date': 20210427, 'code': '000001', 'cname': '平安银行'}
 {'date': 20210427, 'code': '000012', 'cname': '南 玻Ａ'}
 {'date': 20210427, 'code': '000039', 'cname': '中集集团'} ...
 {'date': 20210423, 'code': '688363', 'cname': '华熙生物'}
 {'date': 20210423, 'code': '688368', 'cname': '晶丰明源'}
 {'date': 20210423, 'code': '688396', 'cname': '华润微'}]
        """

        def stage2():
            """参考：
            C>0 {收盘价>0}
            AND C>MA(C,150) {收盘价大于150日均线}
            AND MA(C,150)>MA(C,200) {150日均线大于200日均线}
            AND EVERY(MA(C,200)>REF(MA(C,200),1),20) {20日均线向上增长}
            AND C/LLV(L,250)>1.3 {收盘价距一年内新低的涨幅不低于30%}
            AND C/HHV(H,250)>0.75 {收盘价距一年内新高的距离低于25%}
            AND VOL>REF(HHV(V,10),1)*1.5 {成交量>前10日内成交量最高值的1.5倍}
            AND IF(RPS.RPS250<70,0,1); {股价相对强弱指标不低于70}
            """
            ma50 = MA(C, 50)
            ma150 = MA(C, 150)
            ma200 = MA(C, 200)
            ml = LLV(LOW, 250)
            mm = HHV(H, 250)
            return (CLOSE > mm * 0.75) & (CLOSE > ml * 1.3) & (CLOSE >= ma150) & (ma50 > ma150 > ma200) & \
                   EVERY(MA(C, 200) > REF(MA(C, 200), 1), 20)
            # return CLOSE > mm * 0.75 and CLOSE > ml * 1.3 and CLOSE >= ma150 and ma50 > ma150 > ma200 and \
                   # EVERY(MA(C, 200) > REF(MA(C, 200), 1), 20)

        data = selectAsync(
            stage2,
            start_date=20210423,
            end_date=20210427,
        )
        print(f"2nd stage：\n{data}\n{len(data)}")

    def test_2nd_stag_selectV(self):
        """当前股价处在50日、150日和200日线上方；
        50日线＞150日线＞200日线；
        200日均线至少上涨了1个月（大多数情况下，上涨4-5个月更好）；
        股价比最近一年最低价至少高30%，至少处在最近一年最高价的75%，距离最高价越近越好；
        交易量较大的几周中，上涨的交易周数量高于下跌的；
        RPS不低于70，最好80、90左右。
        RPS指标又称为股价相对强度指标，是由美国的欧奈尔提出，并运用于市场的分析的。RPS指标是指在一段时间内，个股涨幅在全部股票涨幅排名中的位次值，可通过官方资料得知。
[{'date': 20210427, 'code': '000001', 'cname': '平安银行'}
 {'date': 20210427, 'code': '000012', 'cname': '南 玻Ａ'}
 {'date': 20210427, 'code': '000039', 'cname': '中集集团'}
 {'date': 20210427, 'code': '000049', 'cname': '德赛电池'}
 {'date': 20210427, 'code': '000059', 'cname': '华锦股份'}
 {'date': 20210427, 'code': '000069', 'cname': '华侨城Ａ'}
 {'date': 20210427, 'code': '000100', 'cname': 'TCL科技'}
 {'date': 20210427, 'code': '000408', 'cname': '藏格控股'}
 {'date': 20210427, 'code': '000420', 'cname': '吉林化纤'}
 {'date': 20210427, 'code': '000422', 'cname': 'ST宜化'}
 {'date': 20210427, 'code': '000488', 'cname': '晨鸣纸业'}
 {'date': 20210427, 'code': '000509', 'cname': '*ST华塑'}
 {'date': 20210427, 'code': '000516', 'cname': '国际医学'}
 {'date': 20210427, 'code': '000528', 'cname': '柳 工'}
 {'date': 20210427, 'code': '000536', 'cname': '华映科技'}
 {'date': 20210427, 'code': '000550', 'cname': '江铃汽车'}
 {'date': 20210427, 'code': '000568', 'cname': '泸州老窖'}
 {'date': 20210427, 'code': '000572', 'cname': 'ST海马'}
 {'date': 20210427, 'code': '000584', 'cname': '哈工智能'}
 {'date': 20210427, 'code': '000587', 'cname': '*ST金洲'}
 {'date': 20210427, 'code': '000589', 'cname': '贵州轮胎'}
 {'date': 20210427, 'code': '000615', 'cname': '奥园美谷'}
 {'date': 20210427, 'code': '000626', 'cname': '远大控股'}
 {'date': 20210427, 'code': '000630', 'cname': '铜陵有色'}
 {'date': 20210427, 'code': '000633', 'cname': '合金投资'}
 {'date': 20210427, 'code': '000635', 'cname': '英 力 特'}
 {'date': 20210427, 'code': '000655', 'cname': '金岭矿业'}
 {'date': 20210427, 'code': '000657', 'cname': '中钨高新'}
 {'date': 20210427, 'code': '000659', 'cname': '珠海中富'}
 {'date': 20210427, 'code': '000663', 'cname': '*ST永林'}
 {'date': 20210427, 'code': '000669', 'cname': '*ST金鸿'}
 {'date': 20210427, 'code': '000673', 'cname': '*ST当代'}
 {'date': 20210427, 'code': '000683', 'cname': '远兴能源'}
 {'date': 20210427, 'code': '000709', 'cname': '河钢股份'}
 {'date': 20210427, 'code': '000717', 'cname': '韶钢松山'}
 {'date': 20210427, 'code': '000718', 'cname': '苏宁环球'}
 {'date': 20210427, 'code': '000723', 'cname': '美锦能源'}
 {'date': 20210427, 'code': '000725', 'cname': '京东方Ａ'}
 {'date': 20210427, 'code': '000727', 'cname': '冠捷科技'}
 {'date': 20210427, 'code': '000737', 'cname': '南风化工'}
 {'date': 20210427, 'code': '000751', 'cname': '锌业股份'}
 {'date': 20210427, 'code': '000780', 'cname': '*ST平能'}
 {'date': 20210427, 'code': '000786', 'cname': '北新建材'}
 {'date': 20210427, 'code': '000799', 'cname': '酒鬼酒'}
 {'date': 20210427, 'code': '000806', 'cname': '*ST银河'}
 {'date': 20210427, 'code': '000807', 'cname': '云铝股份'}
 {'date': 20210427, 'code': '000812', 'cname': '陕西金叶'}
 {'date': 20210427, 'code': '000820', 'cname': '*ST节能'}
 {'date': 20210427, 'code': '000825', 'cname': '太钢不锈'}
 {'date': 20210427, 'code': '000830', 'cname': '鲁西化工'}
 {'date': 20210427, 'code': '000837', 'cname': '秦川机床'}
 {'date': 20210427, 'code': '000858', 'cname': '五 粮 液'}
 {'date': 20210427, 'code': '000878', 'cname': '云南铜业'}
 {'date': 20210427, 'code': '000881', 'cname': '中广核技'}
 {'date': 20210427, 'code': '000890', 'cname': '法尔胜'}
 {'date': 20210427, 'code': '000893', 'cname': '亚钾国际'}
 {'date': 20210427, 'code': '000898', 'cname': '鞍钢股份'}
 {'date': 20210427, 'code': '000906', 'cname': '浙商中拓'}
 {'date': 20210427, 'code': '000911', 'cname': '南宁糖业'}
 {'date': 20210427, 'code': '000921', 'cname': '海信家电'}
 {'date': 20210427, 'code': '000928', 'cname': '中钢国际'}
 {'date': 20210427, 'code': '000930', 'cname': '中粮科技'}
 {'date': 20210427, 'code': '000932', 'cname': '华菱钢铁'}
 {'date': 20210427, 'code': '000933', 'cname': '神火股份'}
 {'date': 20210427, 'code': '000949', 'cname': '新乡化纤'}
 {'date': 20210427, 'code': '000960', 'cname': '锡业股份'}
 {'date': 20210427, 'code': '000963', 'cname': '华东医药'}
 {'date': 20210427, 'code': '000980', 'cname': '*ST众泰'}
 {'date': 20210427, 'code': '002001', 'cname': '新 和 成'}
 {'date': 20210427, 'code': '002003', 'cname': '伟星股份'}
 {'date': 20210427, 'code': '002006', 'cname': '精功科技'}
 {'date': 20210427, 'code': '002026', 'cname': '山东威达'}
 {'date': 20210427, 'code': '002027', 'cname': '分众传媒'}
 {'date': 20210427, 'code': '002054', 'cname': '德美化工'}
 {'date': 20210427, 'code': '002080', 'cname': '中材科技'}
 {'date': 20210427, 'code': '002088', 'cname': '鲁阳节能'}
 {'date': 20210427, 'code': '002099', 'cname': '海翔药业'}
 {'date': 20210427, 'code': '002111', 'cname': '威海广泰'}
 {'date': 20210427, 'code': '002113', 'cname': '*ST天润'}
 {'date': 20210427, 'code': '002122', 'cname': '*ST天马'}
 {'date': 20210427, 'code': '002129', 'cname': '中环股份'}
 {'date': 20210427, 'code': '002130', 'cname': '沃尔核材'}
 {'date': 20210427, 'code': '002138', 'cname': '顺络电子'}
 {'date': 20210427, 'code': '002139', 'cname': '拓邦股份'}
 {'date': 20210427, 'code': '002142', 'cname': '宁波银行'}
 {'date': 20210427, 'code': '002145', 'cname': '中核钛白'}
 {'date': 20210427, 'code': '002154', 'cname': '报 喜 鸟'}
 {'date': 20210427, 'code': '002158', 'cname': '汉钟精机'}
 {'date': 20210427, 'code': '002172', 'cname': '澳洋健康'}
 {'date': 20210427, 'code': '002176', 'cname': '江特电机'}
 {'date': 20210427, 'code': '002177', 'cname': '御银股份'}
 {'date': 20210427, 'code': '002179', 'cname': '中航光电'}
 {'date': 20210427, 'code': '002192', 'cname': '融捷股份'}
 {'date': 20210427, 'code': '002206', 'cname': '海 利 得'}
 {'date': 20210427, 'code': '002210', 'cname': '*ST飞马'}
 {'date': 20210427, 'code': '002219', 'cname': '*ST恒康'}
 {'date': 20210427, 'code': '002221', 'cname': '东华能源'}
 {'date': 20210427, 'code': '002230', 'cname': '科大讯飞'}
 {'date': 20210427, 'code': '002236', 'cname': '大华股份'}
 {'date': 20210427, 'code': '002240', 'cname': '盛新锂能'}
 {'date': 20210427, 'code': '002245', 'cname': '蔚蓝锂芯'}
 {'date': 20210427, 'code': '002249', 'cname': '大洋电机'}
 {'date': 20210427, 'code': '002255', 'cname': '海陆重工'}
 {'date': 20210427, 'code': '002256', 'cname': '*ST兆新'}
 {'date': 20210427, 'code': '002259', 'cname': '*ST升达'}
 {'date': 20210427, 'code': '002274', 'cname': '华昌化工'}
 {'date': 20210427, 'code': '002280', 'cname': '*ST联络'}
 {'date': 20210427, 'code': '002282', 'cname': '博深股份'}
 {'date': 20210427, 'code': '002290', 'cname': '禾盛新材'}
 {'date': 20210427, 'code': '002293', 'cname': '罗莱生活'}
 {'date': 20210427, 'code': '002311', 'cname': '海大集团'}
 {'date': 20210427, 'code': '002312', 'cname': '三泰控股'}
 {'date': 20210427, 'code': '002318', 'cname': '久立特材'}
 {'date': 20210427, 'code': '002319', 'cname': '乐通股份'}
 {'date': 20210427, 'code': '002324', 'cname': '普利特'}
 {'date': 20210427, 'code': '002327', 'cname': '富安娜'}
 {'date': 20210427, 'code': '002333', 'cname': 'ST罗普'}
 {'date': 20210427, 'code': '002340', 'cname': '格林美'}
 {'date': 20210427, 'code': '002345', 'cname': '潮宏基'}
 {'date': 20210427, 'code': '002372', 'cname': '伟星新材'}
 {'date': 20210427, 'code': '002378', 'cname': '章源钨业'}
 {'date': 20210427, 'code': '002390', 'cname': '信邦制药'}
 {'date': 20210427, 'code': '002402', 'cname': '和而泰'}
 {'date': 20210427, 'code': '002407', 'cname': '多氟多'}
 {'date': 20210427, 'code': '002408', 'cname': '齐翔腾达'}
 {'date': 20210427, 'code': '002415', 'cname': '海康威视'}
 {'date': 20210427, 'code': '002426', 'cname': '胜利精密'}
 {'date': 20210427, 'code': '002430', 'cname': '杭氧股份'}
 {'date': 20210427, 'code': '002435', 'cname': '长江健康'}
 {'date': 20210427, 'code': '002444', 'cname': '巨星科技'}
 {'date': 20210427, 'code': '002455', 'cname': '百川股份'}
 {'date': 20210427, 'code': '002469', 'cname': '三维化学'}
 {'date': 20210427, 'code': '002472', 'cname': '双环传动'}
 {'date': 20210427, 'code': '002484', 'cname': '江海股份'}
 {'date': 20210427, 'code': '002501', 'cname': '*ST利源'}
 {'date': 20210427, 'code': '002527', 'cname': '新时达'}
 {'date': 20210427, 'code': '002531', 'cname': '天顺风能'}
 {'date': 20210427, 'code': '002532', 'cname': '天山铝业'}
 {'date': 20210427, 'code': '002534', 'cname': '杭锅股份'}
 {'date': 20210427, 'code': '002535', 'cname': '*ST林重'}
 {'date': 20210427, 'code': '002539', 'cname': '云图控股'}
 {'date': 20210427, 'code': '002541', 'cname': '鸿路钢构'}
 {'date': 20210427, 'code': '002556', 'cname': '辉隆股份'}
 {'date': 20210427, 'code': '002563', 'cname': '森马服饰'}
 {'date': 20210427, 'code': '002568', 'cname': '百润股份'}
 {'date': 20210427, 'code': '002572', 'cname': '索菲亚'}
 {'date': 20210427, 'code': '002585', 'cname': '双星新材'}
 {'date': 20210427, 'code': '002586', 'cname': '*ST围海'}
 {'date': 20210427, 'code': '002595', 'cname': '豪迈科技'}
 {'date': 20210427, 'code': '002612', 'cname': '朗姿股份'}
 {'date': 20210427, 'code': '002614', 'cname': '奥佳华'}
 {'date': 20210427, 'code': '002630', 'cname': '华西能源'}
 {'date': 20210427, 'code': '002636', 'cname': '金安国纪'}
 {'date': 20210427, 'code': '002637', 'cname': '赞宇科技'}
 {'date': 20210427, 'code': '002645', 'cname': '华宏科技'}
 {'date': 20210427, 'code': '002648', 'cname': '卫星石化'}
 {'date': 20210427, 'code': '002677', 'cname': '浙江美大'}
 {'date': 20210427, 'code': '002716', 'cname': '*ST金贵'}
 {'date': 20210427, 'code': '002719', 'cname': '*ST麦趣'}
 {'date': 20210427, 'code': '002724', 'cname': '海洋王'}
 {'date': 20210427, 'code': '002727', 'cname': '一心堂'}
 {'date': 20210427, 'code': '002730', 'cname': '电光科技'}
 {'date': 20210427, 'code': '002738', 'cname': '中矿资源'}
 {'date': 20210427, 'code': '002741', 'cname': '光华科技'}
 {'date': 20210427, 'code': '002747', 'cname': '埃斯顿'}
 {'date': 20210427, 'code': '002756', 'cname': '永兴材料'}
 {'date': 20210427, 'code': '002766', 'cname': '*ST索菱'}
 {'date': 20210427, 'code': '002791', 'cname': '坚朗五金'}
 {'date': 20210427, 'code': '002805', 'cname': '丰元股份'}
 {'date': 20210427, 'code': '002810', 'cname': '山东赫达'}
 {'date': 20210427, 'code': '002812', 'cname': '恩捷股份'}
 {'date': 20210427, 'code': '002821', 'cname': '凯莱英'}
 {'date': 20210427, 'code': '002832', 'cname': '比音勒芬'}
 {'date': 20210427, 'code': '002833', 'cname': '弘亚数控'}
 {'date': 20210427, 'code': '002841', 'cname': '视源股份'}
 {'date': 20210427, 'code': '002865', 'cname': '钧达股份'}
 {'date': 20210427, 'code': '002867', 'cname': '周大生'}
 {'date': 20210427, 'code': '002876', 'cname': '三利谱'}
 {'date': 20210427, 'code': '002884', 'cname': '凌霄泵业'}
 {'date': 20210427, 'code': '002919', 'cname': '名臣健康'}
 {'date': 20210427, 'code': '002920', 'cname': '德赛西威'}
 {'date': 20210427, 'code': '002967', 'cname': '广电计量'}
 {'date': 20210427, 'code': '002978', 'cname': '安宁股份'}
 {'date': 20210427, 'code': '300005', 'cname': '探路者'}
 {'date': 20210427, 'code': '300012', 'cname': '华测检测'}
 {'date': 20210427, 'code': '300083', 'cname': '创世纪'}
 {'date': 20210427, 'code': '300089', 'cname': '文化长城'}
 {'date': 20210427, 'code': '300119', 'cname': '瑞普生物'}
 {'date': 20210427, 'code': '300121', 'cname': '阳谷华泰'}
 {'date': 20210427, 'code': '300122', 'cname': '智飞生物'}
 {'date': 20210427, 'code': '300146', 'cname': '汤臣倍健'}
 {'date': 20210427, 'code': '300151', 'cname': '昌红科技'}
 {'date': 20210427, 'code': '300196', 'cname': '长海股份'}
 {'date': 20210427, 'code': '300211', 'cname': '亿通科技'}
 {'date': 20210427, 'code': '300285', 'cname': '国瓷材料'}
 {'date': 20210427, 'code': '300307', 'cname': '慈星股份'}
 {'date': 20210427, 'code': '300316', 'cname': '晶盛机电'}
 {'date': 20210427, 'code': '300327', 'cname': '中颖电子'}
 {'date': 20210427, 'code': '300347', 'cname': '泰格医药'}
 {'date': 20210427, 'code': '300363', 'cname': '博腾股份'}
 {'date': 20210427, 'code': '300390', 'cname': '天华超净'}
 {'date': 20210427, 'code': '300408', 'cname': '三环集团'}
 {'date': 20210427, 'code': '300415', 'cname': '伊之密'}
 {'date': 20210427, 'code': '300421', 'cname': '力星股份'}
 {'date': 20210427, 'code': '300442', 'cname': '普丽盛'}
 {'date': 20210427, 'code': '300450', 'cname': '先导智能'}
 {'date': 20210427, 'code': '300454', 'cname': '深信服'}
 {'date': 20210427, 'code': '300475', 'cname': '聚隆科技'}
 {'date': 20210427, 'code': '300496', 'cname': '中科创达'}
 {'date': 20210427, 'code': '300517', 'cname': '海波重科'}
 {'date': 20210427, 'code': '300518', 'cname': '盛讯达'}
 {'date': 20210427, 'code': '300529', 'cname': '健帆生物'}
 {'date': 20210427, 'code': '300566', 'cname': '激智科技'}
 {'date': 20210427, 'code': '300593', 'cname': '新雷能'}
 {'date': 20210427, 'code': '300595', 'cname': '欧普康视'}
 {'date': 20210427, 'code': '300596', 'cname': '利安隆'}
 {'date': 20210427, 'code': '300604', 'cname': '长川科技'}
 {'date': 20210427, 'code': '300622', 'cname': '博士眼镜'}
 {'date': 20210427, 'code': '300642', 'cname': '透景生命'}
 {'date': 20210427, 'code': '300651', 'cname': '金陵体育'}
 {'date': 20210427, 'code': '300679', 'cname': '电连技术'}
 {'date': 20210427, 'code': '300687', 'cname': '赛意信息'}
 {'date': 20210427, 'code': '300692', 'cname': '中环环保'}
 {'date': 20210427, 'code': '300693', 'cname': '盛弘股份'}
 {'date': 20210427, 'code': '300705', 'cname': '九典制药'}
 {'date': 20210427, 'code': '300712', 'cname': '永福股份'}
 {'date': 20210427, 'code': '300726', 'cname': '宏达电子'}
 {'date': 20210427, 'code': '300750', 'cname': '宁德时代'}
 {'date': 20210427, 'code': '300751', 'cname': '迈为股份'}
 {'date': 20210427, 'code': '300759', 'cname': '康龙化成'}
 {'date': 20210427, 'code': '300760', 'cname': '迈瑞医疗'}
 {'date': 20210427, 'code': '300763', 'cname': '锦浪科技'}
 {'date': 20210427, 'code': '300782', 'cname': '卓胜微'}
 {'date': 20210427, 'code': '600012', 'cname': '皖通高速'}
 {'date': 20210427, 'code': '600019', 'cname': '宝钢股份'}
 {'date': 20210427, 'code': '600022', 'cname': '山东钢铁'}
 {'date': 20210427, 'code': '600025', 'cname': '华能水电'}
 {'date': 20210427, 'code': '600036', 'cname': '招商银行'}
 {'date': 20210427, 'code': '600039', 'cname': '四川路桥'}
 {'date': 20210427, 'code': '600054', 'cname': '黄山旅游'}
 {'date': 20210427, 'code': '600071', 'cname': '凤凰光学'}
 {'date': 20210427, 'code': '600076', 'cname': '康欣新材'}
 {'date': 20210427, 'code': '600089', 'cname': '特变电工'}
 {'date': 20210427, 'code': '600096', 'cname': '云天化'}
 {'date': 20210427, 'code': '600111', 'cname': '北方稀土'}
 {'date': 20210427, 'code': '600115', 'cname': '东方航空'}
 {'date': 20210427, 'code': '600117', 'cname': '西宁特钢'}
 {'date': 20210427, 'code': '600132', 'cname': '重庆啤酒'}
 {'date': 20210427, 'code': '600141', 'cname': '兴发集团'}
 {'date': 20210427, 'code': '600157', 'cname': '永泰能源'}
 {'date': 20210427, 'code': '600160', 'cname': '巨化股份'}
 {'date': 20210427, 'code': '600163', 'cname': '中闽能源'}
 {'date': 20210427, 'code': '600166', 'cname': '福田汽车'}
 {'date': 20210427, 'code': '600177', 'cname': '雅戈尔'}
 {'date': 20210427, 'code': '600188', 'cname': '兖州煤业'}
 {'date': 20210427, 'code': '600193', 'cname': 'ST创兴'}
 {'date': 20210427, 'code': '600219', 'cname': '南山铝业'}
 {'date': 20210427, 'code': '600231', 'cname': '凌钢股份'}
 {'date': 20210427, 'code': '600237', 'cname': '铜峰电子'}
 {'date': 20210427, 'code': '600238', 'cname': '海南椰岛'}
 {'date': 20210427, 'code': '600243', 'cname': '青海华鼎'}
 {'date': 20210427, 'code': '600255', 'cname': '鑫科材料'}
 {'date': 20210427, 'code': '600258', 'cname': '首旅酒店'}
 {'date': 20210427, 'code': '600280', 'cname': '中央商场'}
 {'date': 20210427, 'code': '600282', 'cname': '南钢股份'}
 {'date': 20210427, 'code': '600290', 'cname': 'ST华仪'}
 {'date': 20210427, 'code': '600292', 'cname': '远达环保'}
 {'date': 20210427, 'code': '600306', 'cname': '*ST商城'}
 {'date': 20210427, 'code': '600307', 'cname': '酒钢宏兴'}
 {'date': 20210427, 'code': '600358', 'cname': '国旅联合'}
 {'date': 20210427, 'code': '600362', 'cname': '江西铜业'}
 {'date': 20210427, 'code': '600399', 'cname': '抚顺特钢'}
 {'date': 20210427, 'code': '600406', 'cname': '国电南瑞'}
 {'date': 20210427, 'code': '600408', 'cname': 'ST安泰'}
 {'date': 20210427, 'code': '600433', 'cname': '冠豪高新'}
 {'date': 20210427, 'code': '600436', 'cname': '片仔癀'}
 {'date': 20210427, 'code': '600458', 'cname': '时代新材'}
 {'date': 20210427, 'code': '600460', 'cname': '士兰微'}
 {'date': 20210427, 'code': '600462', 'cname': 'ST九有'}
 {'date': 20210427, 'code': '600499', 'cname': '科达制造'}
 {'date': 20210427, 'code': '600507', 'cname': '方大特钢'}
 {'date': 20210427, 'code': '600515', 'cname': '*ST基础'}
 {'date': 20210427, 'code': '600519', 'cname': '贵州茅台'}
 {'date': 20210427, 'code': '600531', 'cname': '豫光金铅'}
 {'date': 20210427, 'code': '600532', 'cname': '未来股份'}
 {'date': 20210427, 'code': '600549', 'cname': '厦门钨业'}
 {'date': 20210427, 'code': '600552', 'cname': '凯盛科技'}
 {'date': 20210427, 'code': '600563', 'cname': '法拉电子'}
 {'date': 20210427, 'code': '600568', 'cname': 'ST中珠'}
 {'date': 20210427, 'code': '600582', 'cname': '天地科技'}
 {'date': 20210427, 'code': '600586', 'cname': '金晶科技'}
 {'date': 20210427, 'code': '600595', 'cname': '*ST中孚'}
 {'date': 20210427, 'code': '600623', 'cname': '华谊集团'}
 {'date': 20210427, 'code': '600660', 'cname': '福耀玻璃'}
 {'date': 20210427, 'code': '600674', 'cname': '川投能源'}
 {'date': 20210427, 'code': '600690', 'cname': '海尔智家'}
 {'date': 20210427, 'code': '600691', 'cname': '阳煤化工'}
 {'date': 20210427, 'code': '600696', 'cname': 'ST岩石'}
 {'date': 20210427, 'code': '600702', 'cname': '舍得酒业'}
 {'date': 20210427, 'code': '600707', 'cname': '彩虹股份'}
 {'date': 20210427, 'code': '600710', 'cname': '苏美达'}
 {'date': 20210427, 'code': '600733', 'cname': '北汽蓝谷'}
 {'date': 20210427, 'code': '600737', 'cname': '中粮糖业'}
 {'date': 20210427, 'code': '600746', 'cname': '江苏索普'}
 {'date': 20210427, 'code': '600753', 'cname': '东方银星'}
 {'date': 20210427, 'code': '600754', 'cname': '锦江酒店'}
 {'date': 20210427, 'code': '600763', 'cname': '通策医疗'}
 {'date': 20210427, 'code': '600771', 'cname': '广誉远'}
 {'date': 20210427, 'code': '600773', 'cname': '西藏城投'}
 {'date': 20210427, 'code': '600774', 'cname': '汉商集团'}
 {'date': 20210427, 'code': '600779', 'cname': '水井坊'}
 {'date': 20210427, 'code': '600782', 'cname': '新钢股份'}
 {'date': 20210427, 'code': '600792', 'cname': '云煤能源'}
 {'date': 20210427, 'code': '600798', 'cname': '宁波海运'}
 {'date': 20210427, 'code': '600803', 'cname': '新奥股份'}
 {'date': 20210427, 'code': '600808', 'cname': '马钢股份'}
 {'date': 20210427, 'code': '600809', 'cname': '山西汾酒'}
 {'date': 20210427, 'code': '600810', 'cname': '神马股份'}
 {'date': 20210427, 'code': '600817', 'cname': '宏盛科技'}
 {'date': 20210427, 'code': '600860', 'cname': '京城股份'}
 {'date': 20210427, 'code': '600877', 'cname': '电能股份'}
 {'date': 20210427, 'code': '600882', 'cname': '妙可蓝多'}
 {'date': 20210427, 'code': '600886', 'cname': '国投电力'}
 {'date': 20210427, 'code': '600892', 'cname': '大晟文化'}
 {'date': 20210427, 'code': '600926', 'cname': '杭州银行'}
 {'date': 20210427, 'code': '600966', 'cname': '博汇纸业'}
 {'date': 20210427, 'code': '600970', 'cname': '中材国际'}
 {'date': 20210427, 'code': '600971', 'cname': '恒源煤电'}
 {'date': 20210427, 'code': '600976', 'cname': '健民集团'}
 {'date': 20210427, 'code': '600983', 'cname': '惠而浦'}
 {'date': 20210427, 'code': '600985', 'cname': '淮北矿业'}
 {'date': 20210427, 'code': '600989', 'cname': '宝丰能源'}
 {'date': 20210427, 'code': '600997', 'cname': '开滦股份'}
 {'date': 20210427, 'code': '601003', 'cname': '柳钢股份'}
 {'date': 20210427, 'code': '601005', 'cname': '重庆钢铁'}
 {'date': 20210427, 'code': '601009', 'cname': '南京银行'}
 {'date': 20210427, 'code': '601021', 'cname': '春秋航空'}
 {'date': 20210427, 'code': '601028', 'cname': '玉龙股份'}
 {'date': 20210427, 'code': '601058', 'cname': '赛轮轮胎'}
 {'date': 20210427, 'code': '601088', 'cname': '中国神华'}
 {'date': 20210427, 'code': '601111', 'cname': '中国国航'}
 {'date': 20210427, 'code': '601113', 'cname': 'ST华鼎'}
 {'date': 20210427, 'code': '601126', 'cname': '四方股份'}
 {'date': 20210427, 'code': '601127', 'cname': '小康股份'}
 {'date': 20210427, 'code': '601155', 'cname': '新城控股'}
 {'date': 20210427, 'code': '601166', 'cname': '兴业银行'}
 {'date': 20210427, 'code': '601208', 'cname': '东材科技'}
 {'date': 20210427, 'code': '601225', 'cname': '陕西煤业'}
 {'date': 20210427, 'code': '601311', 'cname': '骆驼股份'}
 {'date': 20210427, 'code': '601339', 'cname': '百隆东方'}
 {'date': 20210427, 'code': '601377', 'cname': '兴业证券'}
 {'date': 20210427, 'code': '601388', 'cname': '怡球资源'}
 {'date': 20210427, 'code': '601598', 'cname': '中国外运'}
 {'date': 20210427, 'code': '601600', 'cname': '中国铝业'}
 {'date': 20210427, 'code': '601618', 'cname': '中国中冶'}
 {'date': 20210427, 'code': '601636', 'cname': '旗滨集团'}
 {'date': 20210427, 'code': '601677', 'cname': '明泰铝业'}
 {'date': 20210427, 'code': '601678', 'cname': '滨化股份'}
 {'date': 20210427, 'code': '601777', 'cname': '力帆科技'}
 {'date': 20210427, 'code': '601799', 'cname': '星宇股份'}
 {'date': 20210427, 'code': '601838', 'cname': '成都银行'}
 {'date': 20210427, 'code': '601866', 'cname': '中远海发'}
 {'date': 20210427, 'code': '601882', 'cname': '海天精工'}
 {'date': 20210427, 'code': '601886', 'cname': '江河集团'}
 {'date': 20210427, 'code': '601888', 'cname': '中国中免'}
 {'date': 20210427, 'code': '601898', 'cname': '中煤能源'}
 {'date': 20210427, 'code': '601899', 'cname': '紫金矿业'}
 {'date': 20210427, 'code': '601918', 'cname': '新集能源'}
 {'date': 20210427, 'code': '601919', 'cname': '中远海控'}
 {'date': 20210427, 'code': '601949', 'cname': '中国出版'}
 {'date': 20210427, 'code': '601965', 'cname': '中国汽研'}
 {'date': 20210427, 'code': '601966', 'cname': '玲珑轮胎'}
 {'date': 20210427, 'code': '603002', 'cname': '宏昌电子'}
 {'date': 20210427, 'code': '603008', 'cname': '喜临门'}
 {'date': 20210427, 'code': '603026', 'cname': '石大胜华'}
 {'date': 20210427, 'code': '603067', 'cname': '振华股份'}
 {'date': 20210427, 'code': '603076', 'cname': '乐惠国际'}
 {'date': 20210427, 'code': '603098', 'cname': '森特股份'}
 {'date': 20210427, 'code': '603100', 'cname': '川仪股份'}
 {'date': 20210427, 'code': '603110', 'cname': '东方材料'}
 {'date': 20210427, 'code': '603127', 'cname': '昭衍新药'}
 {'date': 20210427, 'code': '603128', 'cname': '华贸物流'}
 {'date': 20210427, 'code': '603161', 'cname': '科华控股'}
 {'date': 20210427, 'code': '603177', 'cname': '德创环保'}
 {'date': 20210427, 'code': '603180', 'cname': '金牌厨柜'}
 {'date': 20210427, 'code': '603198', 'cname': '迎驾贡酒'}
 {'date': 20210427, 'code': '603223', 'cname': '恒通股份'}
 {'date': 20210427, 'code': '603227', 'cname': '雪峰科技'}
 {'date': 20210427, 'code': '603259', 'cname': '药明康德'}
 {'date': 20210427, 'code': '603260', 'cname': '合盛硅业'}
 {'date': 20210427, 'code': '603267', 'cname': '鸿远电子'}
 {'date': 20210427, 'code': '603277', 'cname': '银都股份'}
 {'date': 20210427, 'code': '603298', 'cname': '杭叉集团'}
 {'date': 20210427, 'code': '603299', 'cname': '苏盐井神'}
 {'date': 20210427, 'code': '603300', 'cname': '华铁应急'}
 {'date': 20210427, 'code': '603306', 'cname': '华懋科技'}
 {'date': 20210427, 'code': '603337', 'cname': '杰克股份'}
 {'date': 20210427, 'code': '603345', 'cname': '安井食品'}
 {'date': 20210427, 'code': '603358', 'cname': '华达科技'}
 {'date': 20210427, 'code': '603392', 'cname': '万泰生物'}
 {'date': 20210427, 'code': '603456', 'cname': '九洲药业'}
 {'date': 20210427, 'code': '603486', 'cname': '科沃斯'}
 {'date': 20210427, 'code': '603501', 'cname': '韦尔股份'}
 {'date': 20210427, 'code': '603519', 'cname': '立霸股份'}
 {'date': 20210427, 'code': '603555', 'cname': '*ST贵人'}
 {'date': 20210427, 'code': '603588', 'cname': '高能环境'}
 {'date': 20210427, 'code': '603599', 'cname': '广信股份'}
 {'date': 20210427, 'code': '603612', 'cname': '索通发展'}
 {'date': 20210427, 'code': '603613', 'cname': '国联股份'}
 {'date': 20210427, 'code': '603683', 'cname': '晶华新材'}
 {'date': 20210427, 'code': '603698', 'cname': '航天工程'}
 {'date': 20210427, 'code': '603733', 'cname': '仙鹤股份'}
 {'date': 20210427, 'code': '603737', 'cname': '三棵树'}
 {'date': 20210427, 'code': '603801', 'cname': '志邦家居'}
 {'date': 20210427, 'code': '603806', 'cname': 'DR福斯特'}
 {'date': 20210427, 'code': '603816', 'cname': '顾家家居'}
 {'date': 20210427, 'code': '603826', 'cname': '坤彩科技'}
 {'date': 20210427, 'code': '603833', 'cname': '欧派家居'}
 {'date': 20210427, 'code': '603877', 'cname': '太平鸟'}
 {'date': 20210427, 'code': '603882', 'cname': '金域医学'}
 {'date': 20210427, 'code': '603885', 'cname': '吉祥航空'}
 {'date': 20210427, 'code': '603899', 'cname': '晨光文具'}
 {'date': 20210427, 'code': '603901', 'cname': '永创智能'}
 {'date': 20210427, 'code': '603906', 'cname': '龙蟠科技'}
 {'date': 20210427, 'code': '603915', 'cname': '国茂股份'}
 {'date': 20210427, 'code': '603966', 'cname': '法兰泰克'}
 {'date': 20210427, 'code': '603970', 'cname': '中农立华'}
 {'date': 20210427, 'code': '603979', 'cname': '金诚信'}
 {'date': 20210427, 'code': '603991', 'cname': '至正股份'}
 {'date': 20210427, 'code': '603996', 'cname': '*ST中新'}
 {'date': 20210427, 'code': '688005', 'cname': '容百科技'}
 {'date': 20210427, 'code': '688099', 'cname': '晶晨股份'}
 {'date': 20210427, 'code': '688139', 'cname': '海尔生物'}
 {'date': 20210427, 'code': '688169', 'cname': '石头科技'}
 {'date': 20210427, 'code': '688188', 'cname': '柏楚电子'}
 {'date': 20210427, 'code': '688202', 'cname': '美迪西'}
 {'date': 20210427, 'code': '688357', 'cname': '建龙微纳'}
 {'date': 20210427, 'code': '688363', 'cname': '华熙生物'}
 {'date': 20210427, 'code': '688368', 'cname': '晶丰明源'}
 {'date': 20210427, 'code': '688388', 'cname': '嘉元科技'}
 {'date': 20210427, 'code': '688396', 'cname': '华润微'}]
        """

        def stage2():
            """参考：
            C>0 {收盘价>0}
            AND C>MA(C,150) {收盘价大于150日均线}
            AND MA(C,150)>MA(C,200) {150日均线大于200日均线}
            AND EVERY(MA(C,200)>REF(MA(C,200),1),20) {20日均线向上增长}
            AND C/LLV(L,250)>1.3 {收盘价距一年内新低的涨幅不低于30%}
            AND C/HHV(H,250)>0.75 {收盘价距一年内新高的距离低于25%}
            AND VOL>REF(HHV(V,10),1)*1.5 {成交量>前10日内成交量最高值的1.5倍}
            AND IF(RPS.RPS250<70,0,1); {股价相对强弱指标不低于70}
            """
            ma50 = MA(C, 50)
            ma150 = MA(C, 150)
            ma200 = MA(C, 200)
            ml = LLV(LOW, 250)
            mm = HHV(H, 250)
            return (CLOSE > mm * 0.75) & (CLOSE > ml * 1.3) & (CLOSE >= ma150) & (ma50 > ma150 > ma200) & \
                   EVERY(MA(C, 200) > REF(MA(C, 200), 1), 20)

        data = selectV(
            stage2,
            start_date=20210423,
            end_date=20210428,
        )
        print(f"2nd stage：\n{data}\n查询到数量：{len(data)}")

    def _getmas(self, a_time_serie):
      ma50 = MA(a_time_serie, 50)
      ma150 = MA(a_time_serie, 150)
      ma200 = MA(a_time_serie, 200)
      return ma50, ma150, ma200

    def test_3_compare(self):
        """测试stage1, stage2两种写法。
        最后stage1的结果是正确的，stage2的结果错误。
        stage2:当前一个判断ma50>ma150,并且ma200>0,和预期的判断不一样;见stage3
        """

        def stage1(a_time_serie):
          ma50, ma150, ma200 = self._getmas(a_time_serie)
          return (ma50 > ma150) & (ma150 > ma200)

        def stage2(a_time_serie):
          ma50, ma150, ma200 = self._getmas(a_time_serie)
          return ma50 > ma150 > ma200

        def stage3(a_time_serie):
          ma50, ma150, ma200 = self._getmas(a_time_serie)
          return (ma50 > ma150) & (ma200 > 0)
         
        def compare_3_var(arr):
          fakedata = self.fakeMarketData(arr)
          # fakedata = self.fakeMarketData(arr)*1000
          # fakedata._series = np.round(fakedata.series*1000, 3)
          s1 = stage1(fakedata)
          s2 = stage2(fakedata)
          if not np.alltrue(s1.series == s2.series):
            s = s1 == s2
            print(s2.series[-20:])
            print(f"stage1 vs stage2 not all true\n{len(s)}\n:{s.series}")
            for i in range(len(s1)):
              ma50, ma150, ma200 = self._getmas(fakedata)
              if s1 is not None and s1.series[i] != s2.series[i]:
                print(f"{i}, {s1.series[i]}, {s2.series[i]}, {ma50.series[i]}, {ma150.series[i]}, {ma200.series[i]}")
              s3 = stage3(fakedata)
              self.assertTrue(np.alltrue(s3.series == s3.series), f"input:{arr}")
            return s
          self.assertTrue(np.alltrue(s1.series == s2.series), f"input:{arr}")
          print(s1.series[-20:])
          return None

        arr = np.array(range(300))
        compare_3_var(arr)
        arr = np.array(np.random.random(300))
        arr = np.round(arr * 1000, 3)
        compare_3_var(arr)

    def test_3_compare2(self):

        def stage1():
            ma50 = MA(C, 50)
            ma150 = MA(C, 150)
            ma200 = MA(C, 200)
            ml = LLV(LOW, 250)
            mm = HHV(H, 250)
            return (ma50 > ma150) & (ma150 > ma200)
          
        def stage2():
            ma50 = MA(C, 50)
            ma150 = MA(C, 150)
            ma200 = MA(C, 200)
            ml = LLV(LOW, 250)
            mm = HHV(H, 250)
            return ma50 > ma150 > ma200

        data = selectV(
            stage2,
            start_date=20210423,
            end_date=20210427,
        )

        data2 = selectV(
            stage2,
            start_date=20210423,
            end_date=20210427,
        )
        print(f"2nd stage1：\n{data}\n查询到数量：{len(data)}")
        print(f"2nd stage2：\n{data2}\n查询到数量：{len(data2)}")

    def test_finacial(self):
        """总市值<(总资产-负债总额)
        FINANCE（41）/1000<(FINANCE（10）-FINANCE（15）-FINANCE（16）);
        通达信软件里没有“负债总额”函数，只有“流动负债”（FINANCE（15））、“长期负债”（FINANCE（16））函数。
        """
        # todo
        self.assertTrue(True == False)


if __name__ == '__main__':
    unittest.main()
