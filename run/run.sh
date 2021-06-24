#!/bin/bash
# 10日卡夫曼自适应均线选股
pytest -v  "../tests/funcat/test_ema_trends.py"::Test_ema_trend::test_condition_kama_ema3 && vim /tmp/kama_ema_*.txt