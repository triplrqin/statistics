import pandas as pd
import numpy as np
from sklearn import preprocessing
import sklearn.cluster as sc

#full_music_data = pd.read_csv('./data/full_music_data.csv')
#features = ['danceability','energy','valence','tempo','loudness',  'acousticness',  'instrumentalness',  'liveness',  'speechiness',  'duration_ms']
#pd.set_option('max_colwidth',100)
top_music = pd.read_csv('./data/music_top100_nolabel.csv')
PCA_list = ['PC1','PC2','PC3','PC4','PC5','PC6','PC7']

# min-max标准化
min_max = preprocessing.MinMaxScaler()
music_data = top_music[PCA_list].values
music_data = min_max.fit_transform(music_data)

num_clusters = 5
#常见聚类模型 以下10个聚类方法需要用谁把谁注释掉即可
#model = sc.AffinityPropagation(damping=0.9)#亲和力传播（运行太慢）
model = sc.AgglomerativeClustering(n_clusters=num_clusters)# 聚合聚类
#model = sc.Birch(threshold=0.01, n_clusters=num_clusters)# birch聚类
#model = sc.DBSCAN(eps=0.30, min_samples=10)# dbscan 聚类
model = sc.KMeans(n_clusters=num_clusters)# k-means 聚类
#model = sc.MiniBatchKMeans(n_clusters=num_clusters)# mini-batch k均值聚类
#model = sc.MeanShift()# 均值漂移聚类（运行较慢）
#model = sc.OPTICS(eps=0.8, min_samples=10)#optics聚类
#model = sc.SpectralClustering(n_clusters=num_clusters)# spectral clustering（速度较慢，结果较散）
# model = GaussianMixture(n_components=10)#高斯混合模型

# 模型拟合与聚类预测
# 模型拟合
# 为每个示例分配一个集群
yhat = model.fit_predict(music_data)
#查看各个类数量
print(np.unique(yhat, return_counts=True))

# 合并label
top_music['label'] = yhat

top_music.to_csv('./data/music_top100_5_label.csv')
print(0)