# -*- coding: utf-8 -*-
#

def hong_san_bing(DAYS=3, PERCENT=3):
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
