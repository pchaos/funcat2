# -*- coding: utf-8 -*-
"""条件选股

Author: p19992003, <p19992003#gmail.com>
"""

from .selection import hong_san_bing, chcount as CHCOUNT

from .turtle import FOURWEEK, FOURWEEKQTY

HSB = hong_san_bing

__all__ = ["hong_san_bing", "HSB",
           "CHCOUNT",
           "FOURWEEK",
           "FOURWEEKQTY",
           ]
