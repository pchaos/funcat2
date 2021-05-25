# -*- coding: utf-8 -*-
"""Visualizing the stock market structure（改编为上证50成分股聚类可视化）
原文：https://scikit-learn.org/dev/auto_examples/applications/plot_stock_market.html#sphx-glr-auto-examples-applications-plot-stock-market-py
"""

# Author: Gael Varoquaux gael.varoquaux@normalesup.org
# License: BSD 3 clause
import statistics
import unittest
import numpy as np
import sys
import datetime
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

import pandas as pd

from sklearn import cluster, covariance, manifold

from funcat import *
from funcat.api import UPNDAY, DOWNNDAY, NDAY
from funcat.utils import FuncatTestCase

print(__doc__)


class TestPlotStockSZ50(FuncatTestCase):
    def get_symbola__from_block(self, blockname="上证50"):
        """默认返回上证50板块哦列表、
        """
        symbols = self.BE.backend.QA_fetch_stock_block_adv(blockname=blockname).data.index.levels[1].to_list()
        return symbols

    def get_open_close(self, symbols, start_date=20200101, end_date=20201231):
        """获取开盘价，收盘价
        调整连续交易日时间序列
        """
        quotes = []
        # date_range = pd.date_range(start=str(start_date), end=str(end_date), freq='B')
        trading_dates = self.BE.get_trading_dates(start=start_date, end=end_date)
        dr = pd.DataFrame(trading_dates, columns=["date"])
        # dr = pd.DataFrame(data=date_range, columns=['date'])
        dr.date = dr.date.map(lambda x: datetime.datetime.strptime(str(x), '%Y%m%d'))
        for symbol in symbols:
            # 前复权
            df = pd.DataFrame(self.BE.get_price(symbol, start_date, end_date, "1d"))
            # 字符串转日期
            df.date = df.date.map(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'))
            # 与日期序列合并，使数据日期连续
            df = pd.merge(dr, df, how='left', on='date')
            quotes.append(df)
            print(symbol, end=",")

        close_prices = np.vstack([q['close'] for q in quotes])
        open_prices = np.vstack([q['open'] for q in quotes])
        return close_prices, open_prices, symbols

    def get_open_close2(self, symbols, start_date=20200101, end_date=20201231):
        """非正常交易日期截断"""
        quotes = []
        lastdates = []
        counts = []
        print('Fetching quote history for')
        for symbol in symbols:
            print(' %r' % symbol, file=sys.stderr, end=",", flush=True)
            data = pd.DataFrame(self.BE.get_price(symbol, start_date, end_date, "1d"))
            quotes.append(data)
            lastdates.append(data["date"][-1:].values[0])
            counts.append(int(data.count()[0]))
        normal_date = statistics.mode(lastdates)
        normal_count = statistics.mode(counts)
        for i in range(len(quotes) - 1, 0, -1):
            if lastdates[i] != normal_date:
                # 剔除最后交易日期不同的数据
                quotes.pop(i)
                symbols.pop(i)
                print(i, "-->", normal_count, counts[i])
            else:
                if counts[i] != normal_count:
                    # 剔除长度不一致的数据
                    quotes.pop(i)
                    symbols.pop(i)
                    print(i, normal_count, counts[i])
        close_prices = np.vstack([q['close'] for q in quotes])
        open_prices = np.vstack([q['open'] for q in quotes])
        return close_prices, open_prices, symbols

    def _visualize(self, names, close_prices, open_prices):
        # The daily variations of the quotes are what carry most information
        variation = close_prices - open_prices
        # NaN值赋值为0，下面在调用GraphLassoCV的时候会报一些除0的RuntimeWarning，但是可以通过
        variation[np.isnan(variation)] = 0
        # #############################################################################
        # Learn a graphical structure from the correlations
        edge_model = covariance.GraphicalLassoCV()
        # standardize the time series: using correlations rather than covariance
        # is more efficient for structure recovery
        X = variation.copy().T
        X /= X.std(axis=0)
        edge_model.fit(X)
        # #############################################################################
        # Cluster using affinity propagation
        _, labels = cluster.affinity_propagation(edge_model.covariance_,
                                                 random_state=0)
        n_labels = labels.max()
        for i in range(n_labels + 1):
            print('Cluster %i: %s' % ((i + 1), ', '.join(names[labels == i])))
        # #############################################################################
        # Find a low-dimension embedding for visualization: find the best position of
        # the nodes (the stocks) on a 2D plane
        # We use a dense eigen_solver to achieve reproducibility (arpack is
        # initiated with random vectors that we don't control). In addition, we
        # use a large number of neighbors to capture the large-scale structure.
        node_position_model = manifold.LocallyLinearEmbedding(
            n_components=2, eigen_solver='dense', n_neighbors=6)
        embedding = node_position_model.fit_transform(X.T).T
        # #############################################################################
        # Visualization
        # 支持中文
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
        plt.figure(1, facecolor='w', figsize=(15, 12))
        plt.clf()
        ax = plt.axes([0., 0., 1., 1.])
        plt.axis('off')
        # Display a graph of the partial correlations
        partial_correlations = edge_model.precision_.copy()
        d = 1 / np.sqrt(np.diag(partial_correlations))
        partial_correlations *= d
        partial_correlations *= d[:, np.newaxis]
        non_zero = (np.abs(np.triu(partial_correlations, k=1)) > 0.02)
        # Plot the nodes using the coordinates of our embedding
        plt.scatter(embedding[0], embedding[1], s=100 * d ** 2, c=labels,
                    cmap=plt.cm.nipy_spectral)
        # Plot the edges
        start_idx, end_idx = np.where(non_zero)
        # a sequence of (*line0*, *line1*, *line2*), where::
        #            linen = (x0, y0), (x1, y1), ... (xm, ym)
        segments = [[embedding[:, start], embedding[:, stop]]
                    for start, stop in zip(start_idx, end_idx)]
        values = np.abs(partial_correlations[non_zero])
        lc = LineCollection(segments,
                            zorder=0, cmap=plt.cm.hot_r,
                            norm=plt.Normalize(0, .7 * values.max()))
        lc.set_array(values)
        lc.set_linewidths(15 * values)
        ax.add_collection(lc)
        # Add a label to each node. The challenge here is that we want to
        # position the labels to avoid overlap with other labels
        for index, (name, label, (x, y)) in enumerate(
                zip(names, labels, embedding.T)):

            dx = x - embedding[0]
            dx[index] = 1
            dy = y - embedding[1]
            dy[index] = 1
            this_dx = dx[np.argmin(np.abs(dy))]
            this_dy = dy[np.argmin(np.abs(dx))]
            if this_dx > 0:
                horizontalalignment = 'left'
                x = x + .002
            else:
                horizontalalignment = 'right'
                x = x - .002
            if this_dy > 0:
                verticalalignment = 'bottom'
                y = y + .002
            else:
                verticalalignment = 'top'
                y = y - .002
            plt.text(x, y, name, size=10,
                     horizontalalignment=horizontalalignment,
                     verticalalignment=verticalalignment,
                     bbox=dict(facecolor='w',
                               edgecolor=plt.cm.nipy_spectral(label / float(n_labels)),
                               alpha=.6))
        plt.xlim(embedding[0].min() - .15 * embedding[0].ptp(),
                 embedding[0].max() + .10 * embedding[0].ptp(), )
        plt.ylim(embedding[1].min() - .03 * embedding[1].ptp(),
                 embedding[1].max() + .03 * embedding[1].ptp())
        plt.show()

    def test_plot_stock(self):
        start_date = 20190101
        end_date = 20201231
        symbols = self.get_symbola__from_block("上证50")
        close_prices, open_prices, symbols = self.get_open_close(symbols, start_date, end_date)
        names = np.array([self.BE.symbol(item) for item in symbols])
        self._visualize(names, close_prices, open_prices)

    def test_plot_stock2(self):
        start_date = 20190101
        end_date = 20201231
        symbols = self.get_symbola__from_block()
        close_prices, open_prices, symbols = self.get_open_close2(symbols, start_date, end_date)
        names = np.array([self.BE.symbol(item) for item in symbols])
        self._visualize(names, close_prices, open_prices)


if __name__ == '__main__':
    unittest.main()
