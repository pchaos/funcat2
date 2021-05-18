# -*- coding: utf-8 -*-
import numpy as np
from ..time_series import NumericSeries

def hong_san_bing2(DAYS=3, PERCENT=3):
    """红三兵
    连续上涨三天，涨幅要一天比一天大，其中第一天的上涨幅度不小于三个点。
    成交量也要一天比一天大
    """
    from funcat.api import REF, C, CLOSE, UPNDAY, NDAY, O, OPEN, V, VOL, VOLUME
    COND1 = (REF(C, DAYS - 1) / REF(C, DAYS) - 1)
    COND2 = (REF(C, DAYS - 2) / REF(C, DAYS - 1) - 1)
    COND3 = (REF(C, DAYS - 3) / REF(C, DAYS - 2) - 1)

    KSTAR = UPNDAY(CLOSE, DAYS) & NDAY(CLOSE, OPEN, DAYS) & \
            UPNDAY(VOL, DAYS) & \
            (COND1 * 100 >= PERCENT) & \
            (COND2 > COND1) & \
            (COND3 > COND2)
    return KSTAR


def hong_san_bing(DAYS=3, PERCENT=3):
    """红三兵
    连续上涨三天，涨幅要一天比一天大，其中第一天的上涨幅度不小于三个点(或者涨停)。
    成交量也要一天比一天大
    """
    from funcat.api import REF, C, CLOSE, UPNDAY, NDAY, O, OPEN, V, VOL, VOLUME
    COND1 = (REF(C, DAYS - 1) / REF(C, DAYS) - 1)
    COND2 = (REF(C, DAYS - 2) / REF(C, DAYS - 1) - 1)
    COND3 = (REF(C, DAYS - 3) / REF(C, DAYS - 2) - 1)
    higher = 0.095
    KSTAR = UPNDAY(CLOSE, DAYS) & NDAY(CLOSE, OPEN, DAYS) & \
            UPNDAY(VOL, DAYS) & \
            (COND1 * 100 >= PERCENT) & \
            ((COND2 >= COND1) | (COND2 > higher)) & \
            ((COND3 >= COND2) | (COND2 > higher))
    return KSTAR


def chcount(DAYS=[5, 13, 21, 34, 55, 89, 144, 233], maxsize=9999) -> NumericSeries:
    """缠板强弱
    选用以斐波那契数列5，13，21，34，55，89，144，233为参数的均线构成均线系统，用该系统建立一个完全的分类去判断走势的强弱与先后。股价位于所有均线之上为第9类，为最强走势[注：最强走势不一定完全在均线之上，这里进行了简化处理]；股价在所有均线之下为最弱走势，为第1类；之间根据站上均线的数量，依次为2-9。
    Args:
        DAYS:时间序列;用于计算CLOSE > MA(CLOSE, day)
        maxsize: 最多用于计算的天数
    Return:
        返回缠板强弱强度（1～9）
    """
    from funcat.api import CLOSE, MA
    minimal_size = len(CLOSE) if len(CLOSE) < maxsize else maxsize
    CNT = NumericSeries(np.ones(minimal_size, dtype=int))
    for day in DAYS:
        CNT = CNT + (CLOSE > MA(CLOSE, day))
    return CNT
