import unittest


class AClass():
    func = 1

    def __init__(self, arg):
        print(self.func, arg)

    def a(self):
        print(self.func)
        return self.func


class BClass(AClass):
    func = 2


class MyTestCase(unittest.TestCase):
    def test_something(self):
        A = AClass
        B = BClass
        print(A(3).a())
        print(B(4).a())
        self.assertFalse(A(1).a() == B(1).a())


if __name__ == '__main__':
    unittest.main()
