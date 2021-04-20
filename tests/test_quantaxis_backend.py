# -*- coding: utf-8 -*-

from unittest import TestCase
from funcat import *
from funcat.data.quantaxis_backend import QuantaxisDataBackend


class TestQuantaxisDataBackend(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        set_data_backend(QuantaxisDataBackend())

    def test_stock_basics(self):
        T("20161216")
        S("000001.XSHG")
