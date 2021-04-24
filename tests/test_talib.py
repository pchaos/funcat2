# -*- coding: utf-8 -*-
import unittest
import numpy as np
import talib
import matplotlib.pyplot as plt


class MyTestCase(unittest.TestCase):
    @classmethod
    def setUp(self) -> None:
        self.close = np.random.random(100)

    def test_ma(self):
        close = self.close
        print(f"数据类型：{type(close)}")
        output = talib.SMA(close)
        print(f"输出数据类型：{type(output)}")
        print(output-close)

    def test_raiseexception(self):
        def f(x):
            return np.int(x)

        x = np.arange(1, 15.1, 0.1)
        self.assertRaises(f(x), " look at the call signature of np.int")

    def test_raiseexception_2(self):
        def f(x):
            return np.int(x)

        x = np.arange(1, 15.1, 0.1)
        f2 = np.vectorize(f)

        plt.plot(x, f2(x))
        plt.show()

if __name__ == '__main__':
    unittest.main()
