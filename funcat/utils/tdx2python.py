# -*- coding: utf-8 -*-
"""小白量化--通达信/大智慧公式转Python代码
see: https://blog.csdn.net/hepu8/article/details/104130585
"""

import os
import numpy as np
from functools import lru_cache
from ..api import *


def read_tdx(filename):
    """
    gs=```
        RSV:=(CLOSE-LLV(LOW,N))/(HHV(HIGH,N)-LLV(LOW,N))*100;
        K:SMA(RSV,M1,1);
        D:SMA(K,M2,1);
        J:3*K-2*D;
        ```
    todo 优先查找用户当前目录
    """
    currDir = os.path.join(os.path.join(os.path.abspath(os.path.dirname(__file__)), ".."),
                           "usrFunc")
    fullname = os.path.join(f"{currDir}", filename)
    # print(fullname)
    if os.path.exists(fullname):
        with open(fullname) as f:
            gs = f.readlines()
        print(f"Reading file: {filename}")
        return gs
    raise Exception(f"not find file :{fullname}")


@lru_cache()
def tdx2python(filename) -> str:
    """将文件（filename)转换成python语句
    """
    gs = read_tdx(filename)
    ovar = ''
    gs3 = []
    for s in gs:
        s = s.replace(':=', '=')
        if s.find(':') > 0:
            if len(ovar) > 0:
                ovar = ovar + f",{s[0:s.find(':')].strip()}"
            else:
                ovar = s[0:s.find(':')]
            s = s.replace(':', '=')
        s = s.strip()
        if (len(s)) > 0:
            if s[-1] == ';':
                s = s[0:len(s) - 1]
        gs3.append(s)
    gs4 = "\n".join(gs3)
    gs4 = gs4 + '\nreturn ' + ovar
    # print('Python代码:\n', gs4)
    return gs4


@lru_cache()
def file2exec_txt(filename, *args):
    """读取文件（filename）， 转换成python function
    """
    gs = tdx2python(filename)
    if len(gs) > 0:
        gs = gs.replace("\n", "\n\t")  # 缩进
        funcPara = ""  # 函数参数
        if len(args) > 0:
            i = 0
            for arg in args:
                if i == 0:
                    funcName = args[0]
                else:
                    if i == 1:
                        funcPara += f"{arg.strip()}"
                    else:
                        funcPara += f", {arg.strip()}"
                i += 1
        execTxt = f"def {funcName}({funcPara}):\n\t{gs}"
        # print(execTxt)
        return funcName, execTxt
    return "", ""

@lru_cache()
def _func_para(**kwargs):
    """根据（**kwargs）生成参数形式。
        默认会把参数名转换成大写；
    """
    i = 0
    funcPara = ""
    for kw in kwargs:
        if i == 0:
            funcPara = f"{kw}={kwargs[kw]}"
        else:
            funcPara += f", {kw}={kwargs[kw]}"
        i += 1
    return funcPara


def tdx2func(filename, *args, **kwargs):
    """从文件filename读取通达信公式，并返回结果

    """
    funcName, execTxt = file2exec_txt(filename, *args)
    if len(execTxt) > 0:
        # 添加globals后，能在exec后执行函数
        execTxt = f"{execTxt}\nglobals()[\"{funcName}\"]={funcName}"
        exec(execTxt, globals(), locals())
        return eval(f"{funcName}({_func_para(**kwargs)})", globals(), locals())

    else:
        print(f"error in {filename}! at least function name is given.")
        return np.array([])
