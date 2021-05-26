
# -*- coding: utf-8 -*-
import unittest
from matplotlib import rcParams
import matplotlib.pyplot as plt
import numpy as np
from pprint import pprint as print


class TestFuncat2TestCase(unittest.TestCase):

    def test_rank(self):

        my_array = np.array([[1, 56, 55, 15],
                             [5, 4, 33, 53],
                             [3, 6, 7, 19]])

        sorted_array = np.argsort(my_array, axis=0)
        print(f"These are ranks of array values: axis=0 \n {sorted_array}")

    def test_rank2(self):

        my_array = np.array([[1, 56, 55, 15],
                             [5, 4, 33, 53],
                             [3, 6, 7, 19]])

        sorted_array = np.argsort(my_array, axis=1)
        print(f"These are ranks of array values: axis=1 \n {sorted_array}")


if __name__ == '__main__':
    unittest.main()
