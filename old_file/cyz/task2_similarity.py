import pandas as pd
import numpy as np
from sklearn import preprocessing
file_genre = './data/data_by_artist_with_genre.csv'
df1 = pd.read_csv(file_genre,sep=',')
df1=df1[~df1['genre'].isin(['Unknown','unknown'])] #删掉了流派为UNKNOW的行

df1=df1.drop(['artist_name'], axis=1)
df1=df1.drop(['popularity'], axis=1)
df1=df1.drop(['count'], axis=1)

features = ['danceability','energy','valence','tempo','loudness','mode','key',  'acousticness',  'instrumentalness',  'liveness',  'speechiness',  'duration_ms']


df_id_genre = df1[['artist_id','genre']]
# 暂时扔下
df1=df1.drop(['artist_id'], axis=1)
df1=df1.drop(['genre'], axis=1)

# 检查是否有NAN值
# print(df1.isnull().any(axis=0))

# min-max标准化
min_max = preprocessing.MinMaxScaler()
tmp = df1[features].values
tmp = min_max.fit_transform(tmp)
df1[features] = tmp
# print(df1.isnull().any(axis=0))




import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')
plt.rc('font', **{'family': 'Microsoft YaHei, SimHei'})

import seaborn as sns
ax = sns.heatmap(df1.corr(), annot=True)
# plt.show()
# annot=True: 显示相关系数矩阵的具体数值

# PCA 通常用中心标准化，也就是都转化成 Z 分数的形式
from sklearn.preprocessing import scale
arrdf1 = scale(df1)
from sklearn.decomposition import PCA
pca = PCA(n_components=12) # 直接与变量个数相同的主成分
print("original array 1st line", arrdf1[0,:])
arrdf1 = pca.fit_transform(arrdf1)
for i in range(12):
    print("PCA Component ", i)
    print(np.round(pca.components_[i], 3))
print("PCA explain ratio")
print(pca.explained_variance_ratio_)
# [0.2406647  0.14210962 0.10956446 0.10219684 0.08318082 0.07343635 0.06963039 0.06033335 0.05459716 0.02922784 0.0274117  0.00764676]

print(pca.singular_values_)
print(arrdf1[0,:])


# 选择前9个，方差解释度占比94%
PC_columns = ['PC1','PC2','PC3','PC4','PC5','PC6','PC7','PC8','PC9']



df_id_genre[PC_columns] = arrdf1[:,:9]
df_final = df_id_genre
# print(df_final.shape)
# print(df_final.isnull().any(axis=0))

# 写入csv
# df_final.to_csv('./data/data_by_artist_with_PCA.csv', index=False)

# 计算流派内部相似度：利用组内平均距离
df_final = df_final.drop(['artist_id'], axis=1)
print("df_final",df_final)

df_mean = df_final.groupby(['genre']).mean().reset_index()
# print(df_mean)


df_final[PC_columns] = df_final.groupby(['genre'])[PC_columns].transform(lambda x: x - x.mean())
# print(df_final)


arr_final = df_final[PC_columns].to_numpy()
arr_dist_inner = np.sqrt(np.sum(np.square(arr_final), axis=1))
# print(arr_dist.shape)
df_final['inner_dist'] = arr_dist_inner
# print(df_final.isnull().any(axis=0))

df_dist = df_final.groupby(['genre'])[['inner_dist']].mean().reset_index()
# print(df_dist)

# 计算流派间的距离
arr_genre_feature = df_mean[['PC1','PC2','PC3','PC4','PC5','PC6','PC7','PC8','PC9']].to_numpy()
num_genre = 19
arr_inter_dist = np.zeros((19,19))
for i in range(num_genre):
    for j in range(num_genre):
        arr_inter_dist[i,j] = np.sqrt(np.sum(np.square(arr_genre_feature[i,:]-arr_genre_feature[j,:])))


print(arr_inter_dist)


# 距离矩阵
df_dist[df_dist['genre']] = arr_inter_dist
print(df_dist.round(2))


df_similar = df_dist.drop(['genre'], axis=1)
df_similar = 1/(df_similar+1)
df_similar = df_similar.replace([np.inf], 1)
df_similar.insert(0, 'genre', df_dist['genre'])
df_similar.rename(columns={"inner_dist": "inner_sim"}, inplace=True)
print(df_similar.round(2))

df_similar.to_csv('./data/cyz_similarity_matrix.csv', index=False)