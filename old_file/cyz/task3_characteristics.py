import pandas as pd
import numpy as np
from sklearn import preprocessing
file_genre = './data/data_by_artist_with_genre.csv'
df1 = pd.read_csv(file_genre,sep=',')

df1=df1.drop(['artist_name'], axis=1)

df1=df1[~df1['genre'].isin(['Unknown','unknown'])] #删掉了流派为UNKNOW的行

# 舍弃popularity和count这两列
df1=df1.drop(['popularity'], axis=1)
df1=df1.drop(['count'], axis=1)
print(df1.isnull().any(axis=0))
features = ['danceability','energy','valence','tempo','loudness','mode','key',  'acousticness',  'instrumentalness',  'liveness',  'speechiness',  'duration_ms']
df_id_genre = df1[['artist_id','genre']]


# min-max标准化
min_max = preprocessing.MinMaxScaler()
tmp = df1[features].values
tmp = min_max.fit_transform(tmp)
print(tmp.shape)
df1[features] = tmp
# print(df1.isnull().any(axis=0))


print(df1)
# 检查是否有NAN值
print(df1.isnull().any(axis=0))

df_avg = df1.groupby(["genre"])[features].mean().reset_index()
print(df_avg)

df_avg.to_csv("./data/TASK3_GENRE_AVERAGE.csv", index=False)