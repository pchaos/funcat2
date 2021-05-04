# -*- coding: utf-8 -*-
"""小白量化--通达信/大智慧公式转Python代码
https://blog.csdn.net/hepu8/article/details/104130585
"""

import os

print('小白量化--通达信/大智慧公式转Python代码\n')


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
    print(fullname)
    if os.path.exists(fullname):
        gs = open(fullname).readlines()
    return gs
    raise Exception(f"not find file :{fullname}")


def tdx2python(filename):
    """"""
    gs = read_tdx(filename)
    ovar = ''
    gs3 = []
    for s in gs:
        s = s.replace(':=', '=')
        if s.find(':') > 0:
            if len(ovar) > 0:
                ovar = ovar + ',' + s[0:s.find(':')]
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
    print('Python代码:\n', gs4)
    return gs4
