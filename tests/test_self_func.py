# -*- coding: utf-8 -*-
import unittest
import talib

class AClass():
    func = 1
    func2 = talib.MA

    def __init__(self, arg):
        print(self.func, arg)

    def a(self):
        print(self.func)
        return self.func

    def getfunc2(self):
        return self.func2


class BClass(AClass):
    func = 2
    func2 = talib.EMA


class MyTestCase(unittest.TestCase):
    def test_something(self):
        A = AClass
        B = BClass
        print(A(3).a())
        print(B(4).a())
        self.assertFalse(A(1).a() == B(1).a())
        self.assertFalse(A(1).getfunc2() == B(1).getfunc2())
        print(A(1).getfunc2(), B(1).getfunc2())


if __name__ == '__main__':
    unittest.main()
