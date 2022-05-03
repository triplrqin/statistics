import pandas as pd
import numpy as np
import os
myDataDir = "./data/"
csv_artist = "data_by_artist.csv"
csv_influence = "influence_data.csv"

df_artist = pd.read_csv(os.path.join(myDataDir, csv_artist), sep=",")
df_influence = pd.read_csv(os.path.join(myDataDir, csv_influence), sep=",")

df1 = df_influence[["influencer_id", "influencer_main_genre"]]
df1.rename(columns={"influencer_id": "artist_id", "influencer_main_genre": "genre"}, inplace=True)
df2 = df_influence[["follower_id", "follower_main_genre"]]
df2.rename(columns={"follower_id": "artist_id", "follower_main_genre": "genre"}, inplace=True)

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
print(df_artist)

df_artist.to_csv("./data/data_by_artist_with_genre.csv", index=False)