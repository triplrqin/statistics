'''
sklearn 最近邻算法 示例 Nearest Neighbor
https://scikit-learn.org/stable/modules/neighbors.html#classification
'''

from sklearn import neighbors
# K最近邻（KNN，K-NearestNeighbor）分类
n_neighbors = 1 #k值小，噪声大；k值大，分类效果差
# we create an instance of Neighbours Classifier and fit the data.
# x_shape: (n_samples, n_features)
x = [[0,0], [1,1], [2,2], [3,3]]
# 分类标签 y
y = [1, 1, 1, 2]

# 分类器 weights 可以选择"uniform"或者"distance", 前者意味着k个最近邻各自贡献相同，后者使用距离加权
clf = neighbors.KNeighborsClassifier(n_neighbors, weights="uniform")

# 一定半径的近邻分类
# radius = ?
#clf = neighbors.RadiusNeighborsClassifier(radius, weights="uniform") # weights="distance"

clf.fit(x, y)
res = clf.predict([[3.5, 3.5]])
print(res)
'''
k近邻算法中文解释： https://zhuanlan.zhihu.com/p/25994179
'''




# Nearest Centroid Classifier 根据离各个类别点的中心的距离进行分类
# 类似与 K-means
from sklearn.neighbors import NearestCentroid
import numpy as np
X = np.array([[-1, -1], [-2, -1], [-3, -2], [1, 1], [2, 1], [3, 2]])
Y = np.array([1, 1, 1, 2, 2, 2])
clf = NearestCentroid()
clf.fit(X, Y)
print(clf.predict([[-0.8, -1]]))
