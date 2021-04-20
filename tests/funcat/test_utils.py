from unittest import TestCase
from funcat.utils import *


class TestUtils(TestCase):
    def test_get_str_date_from_int(self):
        data = get_str_date_from_int(20210101)
        self.assertTrue(data == '2021-01-01')
        data = get_str_date_from_int(20211011)
        self.assertTrue(data == '2021-10-11')