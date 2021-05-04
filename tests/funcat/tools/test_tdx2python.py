from unittest import TestCase
from funcat.tools import tdx2python


class Test(TestCase):
    def test_tdx2python(self):
        filename = "trend.tdx"
        tp = tdx2python(filename=filename)
        self.assertTrue(len(tp) > 10, f"转换不成功：{tp}")
