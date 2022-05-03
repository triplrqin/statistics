import pandas as pd
import numpy as np
from sklearn import preprocessing
import os
myDataDir = "./data/"
csv_artist = "data_by_artist.csv"
csv_influence = "influence_data.csv"

df_artist = pd.read_csv(os.path.join(myDataDir, csv_artist), sep=",")
df_influence = pd.read_csv(os.path.join(myDataDir, csv_influence), sep=",")

df1 = df_influence[["influencer_id", "influencer_main_genre", "influencer_active_start"]]
df1.rename(columns={"influencer_id": "artist_id", "influencer_main_genre": "genre", "influencer_active_start":"time"}, inplace=True)
df2 = df_influence[["follower_id", "follower_main_genre", "follower_active_start"]]
df2.rename(columns={"follower_id": "artist_id", "follower_main_genre": "genre", "follower_active_start":"time"}, inplace=True)

df_genre = pd.concat([df1, df2], axis=0)
print(df_genre.head())
print(df_genre.shape)
df_genre.drop_duplicates("artist_id", keep='first', inplace=True)
print(df_genre.shape)

print(df_artist.shape)
df_artist = pd.merge(left=df_artist, right=df_genre, how='left', on="artist_id")
print(df_artist.shape)
print(df_artist.head)

df_artist["genre"] = df_artist["genre"].replace(np.nan, "Unknown", regex=True)
df_artist = df_artist[~df_artist['genre'].isin(['Unknown','unknown'])] #删掉了流派为UNKNOW的行
print(df_artist.head)
df_artist = df_artist.drop(['popularity','count'], axis=1)

features = ["danceability","energy","valence","tempo","loudness","mode","key","acousticness","instrumentalness","liveness","speechiness","duration_ms"]

tmp = df_artist[features].values
min_max = preprocessing.MinMaxScaler()
tmp = min_max.fit_transform(tmp)
df_artist[features] = tmp
print(df_artist)
df_artist.to_csv("./data/data_task3.csv", index=False)