# -*- coding: utf-8 -*-
"""「我们所经历的上个世纪反复证明，市场的非理性是周期性爆发的。这强烈暗示投资者应尽力去学会应对下一个市场的非理性爆发。而这需要的是一剂解毒剂，我认为这剂解毒剂就是量化分析。如果你定量分析，你并不一定会出色，但是你也不会坠入疯狂。」
换句话说，量化择时可以根据：市场整体择时、板块行业轮动择时及个股的择时。那么，如果能选择牛市、规避熊市，将能够获得非常高超额收益。尤其是在系统性风险较高、波动性比较大的、相关性较强的期货市场，尤为有效。
严格来说，「量化择时」是一个很模糊的概念。因为从一个很大的范围来看，形态交易是择时，趋势交易是择时，统计套利是择时，市场情绪量化是择时、盘口交易也是一种择时，都是设置定量条件，然后观察价格或价差在何时突破这个条件，触发建仓和平仓信号。
"""

from .fcdata import PandasDataBase, addPandasData, MaxShares, CSVDataBase
from .fcIndicator import MQNIndicator, UpdownIndicator

__all__ = ["PandasDataBase",
           "addPandasData",
           "MaxShares",
           "CSVDataBase",

           "MQNIndicator",
           "UpdownIndicator",
           ]
