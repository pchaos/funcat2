#!/bin/bash
pytest -v  "../tests/funcat/test_ema_trends.py"::Test_ema_trend::test_condition_kama_ema3
