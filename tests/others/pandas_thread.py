# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import time
from multiprocessing import Pool, cpu_count


def f(row):
    # 直接对某列进行操作
    return sum(row) + 2


def f1_1(row):
    # 对某一列进行操作，我这里的columns=range(0,2)，此处是对第0列进行操作
    return row[0]**2


def f1_2(row1):
    # 对某一列进行操作，我这里的columns=range(0,2)，此处是对第0列进行操作
    return row1**2


def f2_1(row):
    # 对某两列进行操作，我这里的columns=range(0,2)，此处是对第0，2列进行操作
    return pd.Series([row[0]**2, row[1]**2], index=['1_1', '1_2'])


def f2_2(row1, row2):
    # 对某两列进行操作，我这里的columns=range(0,2)，此处是对第0，2列进行操作
    return pd.Series([row1**2, row2**2], index=['2_1', '2_2'])


def apply_f(df):
    return df.apply(f, axis=1)


def apply_f1_1(df):
    return df.apply(f1_1, axis=1)


def apply_f1_2(df):
    return df[0].apply(f1_2)


def apply_f2_1(df):
    return df.apply(f2_1, axis=1)


def apply_f2_2(df):
    return df.apply(lambda row: f2_2(row[0], row[1]), axis=1)


def init_process(global_vars):
    global a
    a = global_vars


def time_compare():
    '''直接调用和多线程调用时间对比'''
    a = 2
    np.random.seed(0)
    df = pd.DataFrame(np.random.rand(10**5, 2), columns=range(0, 2))
    print(df.columns)

    t1 = time.time()
    result_serial = df.apply(f, axis=1)
    t2 = time.time()
    print("Serial time =", t2 - t1)
    print(result_serial.head())

    df_parts = np.array_split(df, 200)
    print(len(df_parts), type(df_parts[0]))
    with Pool(processes=cpu_count(), initializer=init_process, initargs=(a,)) as pool:
        # with Pool(processes=8) as pool:
        result_parts = pool.map(apply_f, df_parts)
    result_parallel = pd.concat(result_parts)
    t3 = time.time()
    print("Parallel time =", t3 - t2)
    print(result_parallel.head())


def apply_fun():
    '''多种apply函数的调用'''
    a = 2
    np.random.seed(0)
    df = pd.DataFrame(np.random.rand(10**5, 2), columns=range(0, 2))
    print(df.columns)
    df_parts = np.array_split(df, 20)
    print(len(df_parts), type(df_parts[0]))
    with Pool(processes=cpu_count(), initializer=init_process, initargs=(a,)) as pool:
        # with Pool(processes=8) as pool:
        res_part0 = pool.map(apply_f, df_parts)
        res_part1 = pool.map(apply_f1_1, df_parts)
        res_part2 = pool.map(apply_f1_2, df_parts)
        res_part3 = pool.map(apply_f2_1, df_parts)
        res_part4 = pool.map(apply_f2_2, df_parts)

    res_parallel0 = pd.concat(res_part0)
    res_parallel1 = pd.concat(res_part1)
    res_parallel2 = pd.concat(res_part2)
    res_parallel3 = pd.concat(res_part3)
    res_parallel4 = pd.concat(res_part4)

    print("f:\n", res_parallel0.head())
    print("f1:\n", res_parallel1.head())
    print("f2:\n", res_parallel2.head())
    print("f3:\n", res_parallel3.head())
    print("f4:\n", res_parallel4.head())

    df = pd.concat([df, res_parallel0], axis=1)
    df = pd.concat([df, res_parallel1], axis=1)
    df = pd.concat([df, res_parallel2], axis=1)
    df = pd.concat([df, res_parallel3], axis=1)
    df = pd.concat([df, res_parallel4], axis=1)

    print(df.head())


if __name__ == '__main__':
    time_compare()
    apply_fun()
