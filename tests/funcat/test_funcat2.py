# -*- coding: utf-8 -*-
import unittest
from funcat import *
from funcat.api import *



class TestFuncat2TestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        set_data_backend(QuantaxisDataBackend())
        cls.qdb = QuantaxisDataBackend()

    def test_something(self):
        # 选出涨停股
        data = select(
            lambda: C / C[1] - 1 >= 0.0995,
            start_date=20161231,
            end_date=20170104,
        )
        self.assertTrue(len(data)> 10)


if __name__ == '__main__':
    unittest.main()
