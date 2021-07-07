# -*- coding: utf-8 -*-
import unittest
import numpy as np
import talib
import matplotlib.pyplot as plt
from funcat.utils import handle_numpy_warning

__updated__ = "2021-06-24"


@handle_numpy_warning
def f(x):
    return np.int(x)


class MyTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.close = np.random.random(100)

    def test_ma(self):
        close = self.close
        print(f"数据类型：{type(close)}")
        output = talib.MA(close)
        print(f"输出数据类型：{type(output)}")
        print(output - close)

    def test_sma(self):
        close = self.close
        print(f"数据类型：{type(close)}")
        output = talib.SMA(close, 10)
        print(f"输出数据类型：{type(output)}")
        print(output - close)

    def test_raiseexception(self):
        x = np.arange(1, 15.1, 0.1)
        with self.assertRaises(TypeError):
            # look at the call signature of np.int
            f(x)

    def test_raiseexception_2(self):
        x = np.arange(1, 15.1, 0.1)
        f2 = np.vectorize(f)

        plt.plot(x, f2(x))
        plt.show()

    def test_stddev(self):
        """样本标准偏差
        https://www.cnblogs.com/citycomputing/p/10447657.html
        """
        alist = [3606.86, 3580.15, 3411.49]
        arr = np.array(alist)
        print(arr)
        n = len(arr)
        a = (n / (n - 1)) ** 0.5  # [n/(n-1)]的平方根
        astd = talib.STDDEV(arr, len(arr))
        print(f"talib.STDDEV:{astd}")
        print(f"这个是正确 talib.STDDEV * {a}:{astd*a}")
        astd2 = talib.STDDEV(arr * (n / (n - 1)), n)
        print(f"talib.STDDEV:{astd2}")
        astd3 = talib.STDDEV(arr, n) * (n / (n - 1))
        print(f"talib.STDDEV:{astd3}")
        astd31 = talib.STDDEV(arr, n, nbdev=1)
        print(f"talib.STDDEV nbdev=1:{astd31}")
        astd4 = np.std(arr)
        print(f"np.std也不是样本方差:{astd4}")
        astd5 = np.std(arr, ddof=1)
        print(f"np.std 参数ddof=1是样本方差:{astd5}")


if __name__ == '__main__':
    unittest.main()
