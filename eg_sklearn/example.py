#原始版本
# k-means 聚类
import numpy as np
from numpy import where
from sklearn.datasets import make_classification
import sklearn.cluster as sc
from sklearn.mixture import GaussianMixture
import matplotlib.pyplot as plt
# 定义数据集
X, _ = make_classification(n_samples=1000, n_features=5, n_informative=2, n_redundant=0, n_clusters_per_class=1, random_state=4)
# 定义模型

#常见聚类模型 以下10个聚类方法需要用谁把谁注释掉即可
#model = sc.AffinityPropagation(damping=0.9)#亲和力传播（运行太慢）
#model = sc.AgglomerativeClustering(n_clusters=10)# 聚合聚类
#model = sc.Birch(threshold=0.01, n_clusters=10)# birch聚类
#model = sc.DBSCAN(eps=0.30, min_samples=10)# dbscan 聚类
model = sc.KMeans(n_clusters=10)# k-means 聚类
#model = sc.MiniBatchKMeans(n_clusters=10)# mini-batch k均值聚类
#model = sc.MeanShift()# 均值漂移聚类（运行较慢）
#model = sc.OPTICS(eps=0.8, min_samples=10)#optics聚类
#model = sc.SpectralClustering(n_clusters=10)# spectral clustering（速度较慢，结果较散）
# model = GaussianMixture(n_components=10)#高斯混合模型

# 模型拟合与聚类预测
# 模型拟合
# 为每个示例分配一个集群
yhat = model.fit_predict(X)
#new1查看各个类数量
print(np.unique(yhat,return_counts=True))
# 检索唯一群集
clusters = np.unique(yhat)
# 为每个群集的样本创建散点图

for cluster in clusters:
    # 获取此群集的示例的行索引
    row_ix = where(yhat == cluster)

    # 创建这些样本的散布
    plt.scatter(X[row_ix, 0], X[row_ix, 1])
# 绘制散点图
plt.show()