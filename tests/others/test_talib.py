# -*- coding: utf-8 -*-
import unittest
import numpy as np
import talib
import matplotlib.pyplot as plt
from funcat.utils import handle_numpy_warning


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


if __name__ == '__main__':
    unittest.main()
