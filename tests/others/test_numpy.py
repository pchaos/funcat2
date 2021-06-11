# -*- coding: utf-8 -*-
import unittest
from matplotlib import rcParams
import matplotlib.pyplot as plt
import numpy as np
from pprint import pprint as print

__updated__ = "2021-06-11"


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

    def test_rank3(_self_training):
        array = np.array([4, 2, 7, 1])
        order = array.argsort()
        ranks = order.argsort()

    def test_rank4(self):
        array = np.array([4, 2, 7, 1])
        temp = array.argsort()
        ranks = np.empty_like(temp)
        ranks[temp] = np.arange(len(array))

    def test_rank5(self):
        a = np.array([4, 1, 6, 8, 4, 1, 6])

        # a = np.array([4, 2, 7, 2, 1])
        rank = a.argsort().argsort()
        print(f"rank:{rank}")

        unique, inverse = np.unique(a, return_inverse=True)
        print(f"unique, inverse = :{unique}, {inverse}")
        unique_rank_sum = np.zeros_like(unique)
        np.add.at(unique_rank_sum, inverse, rank)
        unique_count = np.zeros_like(unique)
        np.add.at(unique_count, inverse, 1)
        unique_rank_mean = unique_rank_sum.astype(np.float) / unique_count
        rank_mean = unique_rank_mean[inverse]
        print(rank_mean)

    def test_rank6(self):
        def ranks(v):
            t = np.argsort(v)
            r = np.empty(len(v), int)
            r[t] = np.arange(len(v))
            for i in range(1, len(r)):
                if v[t[i]] <= v[t[i - 1]]:
                    r[t[i]] = r[t[i - 1]]
            return r

        # test it
        a = np.array([4, 1, 6, 8, 4, 1, 6])
        print(sorted(zip(ranks(a), a)))

    def test_rank7(self):
        x = np.array([3, 1, np.nan, 2])
        print(f"x={x}")
        print(f"sorted x = {x[x.argsort()]}")
        print(f"sort with np.nan:{x.argsort().argsort()}")

    def test_transpose(self):
        t = np.arange(4)  # 插入值0-3
        print(f"原始：{t}")
        print(f"转置对于一维数组而言，np.transpose()是不起作用的：{ t.transpose()}")

    def test_transpose2(self):
        t = np.arange(16).reshape(4, 4)   # 插入0-15，形状为4*4
        print(f"原始：{t}")
        print(
            f"对于二维数组,数组两个轴axis为（x，y），对应的下标为（0,1），np.transpose()传入的参数为（1,0），即将原数组的0,1轴互换。综上，对二维数组的transpose操作就是对原数组的转置操作。：{ t.transpose()}")

    def test_transpose3(self):
        """二维以上的维数组进行transpose的话，不传参则默认将维度反序
        即将原数组的各个axis进行reverse一下，three原始axis排列为（0,1,2），那numpy.transpose()默认的参数为（2，1，0）得到转置后的数组的视图，不影响原数组的内容以及大小。
        我们一步一步来分析这个过程：axis（0，1，2）———>axis(2，1，0) ，transpose后的数组相对于原数组来说，相当于交换了原数组的0轴和2轴。ndarray.shape (2,3,3) ->(3,3,2)
        (2, 1, 0) 分别代表 维度d,  行l, 列c

        #对原始three数组的位置索引下标写出来，如下：
        A=[
               [ [ (0,0,0) , (0,0,1) , (0,0,2)],
               [ (0,1,0) , (0,1,1) , (0,1,2)],
               [ (0,2,0) , (0,2,1) , (0,2,2)]],

               [[ (1,0,0) , (1,0,1) , (1,0,2)],
                [ (1,1,0) , (1,1,1) , (1,1,2)],
                [ (1,2,0) , (1,2,1) , (1,2,2)]]
          ]

        #接着把上述每个三元组的第一个数和第三个数进行交换，得到以下的数组

        B=[[[ (0,0,0) , (1,0,0) , (2,0,0)],
          [ (0,1,0) , (1,1,0) , (2,1,0)],
          [ (0,2,0) , (1,2,0) , (2,2,0)]],

          [[ (0,0,1) , (1,0,1) , (2,0,1)],
          [ (0,1,1) , (1,1,1) , (2,1,1)],
          [ (0,2,1) , (1,2,1) , (2,2,1)]]]

        #最后在原数组中把B对应的下标的元素，写到相应的位置，如（0，2，1）代表放置到d = 0，行 = 2，列 = 1
        #对比看一下，这是原数组
        [[[ 0,  1,  2],
          [ 3,  4,  5],
          [ 6,  7,  8]],

          [[ 9, 10, 11],
           [12, 13, 14],
           [15, 16, 17]]]
        # 按照B的映射关系得到最终的数组。
        C=[[[ 0,  9],
          [ 3,  12],
          [ 6,  15]],

          [[ 1, 10],
           [4, 13],
           [7, 16]]

           [[ 2, 11],
           [5, 14],
           [8, 17]]
        ]
        # 最终的结果也就是数组C

        再看自己定义的转置格式：
        arr = np.arange(24).reshape(3, 4, 2)
        print(arr)
        tran_arr = np.transpose(arr, (1, 0, 2)) # axis索引（0，1，2）变为（1，0，2） 
        print(tran_arr)


        因为索引号由（0,1,2）变成了（1,0,2），axis第一个和第二个交换，shape 由(3,4,2)变成了(4,3,2)，可知结果矩阵为d = 4，行3，列2。等效于

        arr = np.arange(24).reshape(3, 4, 2)
        np.swapaxes(arr,0,1) #交换axis 0，1

        再展开矩阵的位置下标，每个元素交换第一个和第二个，得到最终的位置下标。

        输出结果：

        [[[ 0  1]
          [ 2  3]
          [ 4  5]
          [ 6  7]]

         [[ 8  9]
          [10 11]
          [12 13]
          [14 15]]

         [[16 17]
          [18 19]
          [20 21]
          [22 23]]]

        [[[ 0  1]
          [ 8  9]
          [16 17]]

         [[ 2  3]
          [10 11]
          [18 19]]

         [[ 4  5]
          [12 13]
          [20 21]] 

         [[ 6 7 ]
          [14 15]
          [22 23]]]
        一般用reshape()进行维度转换比较多，直接传入新的维度就行，而不是用下标代替   
        arr = arr.reshape(4,3,2)
         但是实际上二者是有很大区别的，transpose()会将数组进行转置，而reshape()则是按照数组原有的排布顺序，重新按照新维度生成一个依然有序的数组，从以上两图也能看出来
        """
        t = np.arange(18).reshape(2, 3, 3)
        print(f"原始：{t}")
        print("二维以上的维数组进行transpose的话，不传参则默认将维度反序;")
        print(
            f"对于三维数组,数组两个轴axis为（x，y），对应的下标为（0,1），np.transpose()传入的参数为（1,0），即将原数组的0,1轴互换。综上，对二维数组的transpose操作就是对原数组的转置操作。：{ t.transpose()}")

    def test_concatenate(self):
        # Program to concatenate two 2D arrays column-wise
        # Creating two 2D arrays
        arr1 = np.arange(1, 10).reshape(3, 3)
        arr2 = np.arange(10, 19).reshape(3, 3)
        print(f"arr1: {arr1}")
        print(f"arr2: {arr2}")

        # Concatenating operation
        # axis = 1 implies that it is being done column-wise
        arr = np.concatenate((arr1, arr2), axis=1)
        print(f"np.concatenate((arr1, arr2), axis=1): {arr}")

        # axis = 0 implies that it is being done row-wise
        arr = np.concatenate((arr1, arr2), axis=0)
        print(f"np.concatenate((arr1, arr2), axis=0): {arr}")

    def test_stack(self):
        arr1 = np.arange(1, 10).reshape(3, 3)
        arr2 = np.arange(10, 19).reshape(3, 3)
        print(f"arr1: {arr1}")
        print(f"arr2: {arr2}")
        # Concatenating operation
        # axis = 1 implies that it is being
        # done row-wise
        arr = np.stack((arr1, arr2), axis=1)
        print(f"np.stack((arr1, arr2), axis=1): {arr}")

        # Concatenating operation
        # axis = 2 implies that it is being done
        # along the height
        arr = np.stack((arr1, arr2), axis=2)
        print(f"np.stack((arr1, arr2), axis=2): {arr}")

    def test_hstack(self):
        arr1 = np.arange(1, 10).reshape(3, 3)
        arr2 = np.arange(10, 19).reshape(3, 3)
        print(f"arr1: {arr1}")
        print(f"arr2: {arr2}")
        # Concatenating operation
        arr = np.hstack((arr1, arr2))
        print(f"np.hstack((arr1, arr2)): {arr}")

    def test_vstack(self):
        arr1 = np.arange(1, 10).reshape(3, 3)
        arr2 = np.arange(10, 19).reshape(3, 3)
        print(f"arr1: {arr1}")
        print(f"arr2: {arr2}")
        # Concatenating operation
        arr = np.vstack((arr1, arr2))
        print(f"np.vstack(arr1, arr2): {arr}")

    def test_dstack(self):
        arr1 = np.arange(1, 10).reshape(3, 3)
        arr2 = np.arange(10, 19).reshape(3, 3)
        print(f"arr1: {arr1}")
        print(f"arr2: {arr2}")
        # Concatenating operation
        arr = np.dstack((arr1, arr2))
        print(f"np.dstack(arr1, arr2): {arr}")


if __name__ == '__main__':
    unittest.main()
