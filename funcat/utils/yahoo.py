# -*- coding: utf-8 -*-
"""使用proxy获取sp500，并保存为pickle格式
"""

import bs4 as bs
import datetime as dt
import os
from pathlib import Path  # Python 3.6+ only
import pandas as pd
import pandas_datareader.data as web
import pickle
import requests
from dotenv import load_dotenv

__updated__ = "2021-08-09"

# proxy servers for internet connection
env_path = f"{Path(__file__).parent}/.env"
load_dotenv(dotenv_path=env_path, verbose=True)

proxies = {
    'http': os.getenv("httpproxy", "127.0.0.1:8087"),
    'https': os.getenv("socks5", "socks5://127.0.0.1:1081"),
}

symbol_filename = "sp500tickers.pickle"
# 数据保存目录
symbol_dir = Path(f"{Path('.')}/../../datas").absolute()
symbol_filename = f"{symbol_dir}/{symbol_filename}" if os.path.exists(
    symbol_dir) else symbol_filename
print(f"{symbol_dir=} {symbol_filename=}")


def save_sp500_tickers():
    resp = requests.get(
        'http://en.wikipedia.org/wiki/List_of_S%26P_500_companies',
        proxies=proxies)
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        tickers.append(ticker)
    with open(symbol_filename, "wb") as f:
        pickle.dump(tickers, f)
    return tickers


def get_data_from_yahoo(reload_sp500=False):
    if reload_sp500 or not os.path.exists(symbol_filename):
        tickers = save_sp500_tickers()
    else:
        with open(symbol_filename, "rb") as f:
            tickers = pickle.load(f)

    stock_dfs = f"{symbol_dir}/stock_dfs"
    if not os.path.exists(stock_dfs):
        os.makedirs(stock_dfs)

    start = dt.datetime(2000, 1, 1)
    end = dt.datetime(dt.date.today().year,
                      dt.date.today().month,
                      dt.date.today().day)

    for ticker in tickers:
        ticker = ticker.replace("\n", "")
        csv_file = f'{stock_dfs}/{ticker}.csv'
        if not os.path.exists(csv_file):
            try:
                print(ticker)
                df = web.DataReader(ticker, "yahoo", start, end)
                df.to_csv(csv_file)
            except:
                print("No timeseries available for " + ticker)
        else:
            pass  # print('Already have {}'.format(ticker))


if __name__ == '__main__':

    #  os.environ["HTTP_PROXY"]=proxies['http']
    #  os.environ["HTTPS_PROXY"]=proxies['https']
    get_data_from_yahoo()
