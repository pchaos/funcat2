# sklearn例程:无监督学习可视化股票市场结构

## 可视化股票市场结构简介
本示例采用了几种无监督学习技术，以从历史报价的变化中提取股票市场结构。

我们使用的数量是报价的每日变化：关联报价在一天中往往会一起波动。

下面是数据分析方法：

## 学习图结构
我们使用稀疏逆协方差估计来查找哪些报价跟其他报价条件相关。具体来说，稀疏逆协方差给出了一个图，即一个连接列表。在图中对于每个符号(Symbol)来说，它所连接的其他符号可以用来解释其波动。

## 聚类
我们使用聚类将表现相似的报价分组在一起。在scikit-learn中可用的[各种聚类技术](https://scikit-learn.org/stable/modules/clustering.html#clustering)中，我们选用[亲和力传播](https://scikit-learn.org/stable/modules/clustering.html#affinity-propagation)([Affinity Propagation](https://scikit-learn.org/stable/modules/clustering.html#affinity-propagation))模型，因为它不强制要求大小相同的簇，并且可以从数据中自动选择簇数。

请注意，这给了我们与图不同的表示，因为图反映了变量之间的条件关系，而聚类反映了边际属性：聚类在一起的变量对整个股票市场具有相似的影响。

## 嵌入2D空间
出于可视化目的，我们需要在2D画布上布置不同的符号(Symbol)。为此，我们使用流形学习(Manifold learning )技术获取2D嵌入(Embedding)。

## 可视化
将3个模型的输出组合成2D图，其中节点表示股票符号(Symbol)：

* 聚类标记，用于定义节点的颜色
* 稀疏协方差模型，用于显示边的强度
* 2D嵌入，用于定位节点

此示例包含大量可视化相关的代码，挑战之一是如何放置标签以最大程度地减少重叠。为此，我们使用基于每个轴上最近邻居的方向的启发式方法。

