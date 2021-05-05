# -*- coding: utf-8 -*-
import unittest
from funcat.api import EMA, MA
from funcat.tools import tdx2python, tdx2func, file2exec_txt


# from funcat.indicators import trendline


class Test(unittest.TestCase):
    def test_tdx2python(self):
        filename = "trend.tdx"
        tp = tdx2python(filename=filename)
        self.assertTrue(len(tp) > 10, f"转换不成功：{tp}")

    def test_file2exec_txt(self):
        filename = "trend.tdx"
        funcName = "testfunc"
        funcname, txt = file2exec_txt(filename, funcName)
        self.assertTrue(funcName in funcname, f"返回名称不匹配{funcName},{funcname}")
        self.assertTrue(len(txt) > 10, f"转换结果不对。\n{txt}")
        print(txt)

    # def test_trendline(self):
    #     print(trendline())

    def test_func_name(self):
        # todo
        def afunc(a=4):
            if a.__name__.islowwer():
                return 1
            else:
                return 0

        print(afunc(1))

    def test_tdx2func(self):
        funcName = "testfunc"
        # 函数需要参数S1,S2
        with self.assertRaises(NameError):
            tdx2func("trend.tdx", funcName)
        testData = tdx2func("trend.tdx", funcName, "S1=5", "S2=100")
        self.assertTrue(len(testData) == 4, f"徐小明趋势线每日应该返回四条数据；{testData}")
        print(testData)
        testData = tdx2func("trend.tdx", funcName, "S1=5", "S2=100", S1=23, S2=99)
        print(testData)
        self.assertTrue(len(testData) == 4, f"徐小明趋势线每日应该返回四条数据；{testData}")
        testData = tdx2func("trend.tdx", funcName, "S1=5", "S2=110", S1=23, S2=99)
        print(testData)

    def test_tdx2func2(self):
        funcName = "testfunc"
        testData = tdx2func("trend.tdx", funcName, "S1=5", "S2=100", S1=23, S2=99)
        print(testData)
        self.assertTrue(len(testData) == 4, f"徐小明趋势线每日应该返回四条数据；{testData}")
        testData2 = tdx2func("trend.tdx", funcName, "S1=5", "S2=110", S1=23, S2=99)
        self.assertTrue(testData == testData2, f"返回数据应该相同")
        testData3 = tdx2func("trend.tdx", funcName, "S1=5", "S2=110", S1=23, S2=95)
        self.assertTrue(testData != testData3, f"参数不同，返回数据应该不相同")
        print(testData2)



if __name__ == '__main__':
    unittest.main()
