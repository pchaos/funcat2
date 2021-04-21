# -*- coding: utf-8 -*-
import numpy as np
from funcat import *
from funcat.data.mongodb_backend import MongodbBackend


B2 = MongodbBackend()
a2 = B2.get_price('688389.XSHE', '2020-08-01', '2020-08-06', '1d')
d2 = B2.symbol('000001.XSHG')
b2 = B2.get_order_book_id_list()
c2 = B2.get_trading_dates('2020-05-01', '2020-05-30')
print(a2)
print(f"{d2}, \n{b2},\n {c2}")
