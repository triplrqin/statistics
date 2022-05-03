import pandas as pd
import numpy as np

file_genre = './data/influence_data.csv'
df_init = pd.read_csv(file_genre,sep=',')
df_init['count'] = 1
print(df_init.head())

df_init = df_init[~df_init['follower_main_genre'].isin(['Unknown','unknown'])]
df_init = df_init[~df_init['influencer_main_genre'].isin(['Unknown','unknown'])]

df_time_genre_influence = df_init.groupby(["follower_main_genre", "follower_active_start", "influencer_main_genre"])['count'].count().reset_index()
df_time_genre_influence = df_time_genre_influence.groupby(["follower_main_genre", "follower_active_start", "influencer_main_genre"])['count'].sum().groupby(["follower_main_genre", "influencer_main_genre"]).cumsum().reset_index()
print(df_time_genre_influence.head(10))

df_time_cumulative_influence = df_init.groupby(["follower_main_genre", "follower_active_start"])['count'].count().reset_index()
print(df_time_cumulative_influence)

# cumulative sum for genre with a cumulation in time
df_time_cumulative_influence = df_time_cumulative_influence.groupby(["follower_main_genre", "follower_active_start"])['count'].sum().groupby("follower_main_genre").cumsum().reset_index()
print(df_time_cumulative_influence)

df_time_genre_influence = pd.merge(left=df_time_genre_influence, right=df_time_cumulative_influence, how='left', on=["follower_main_genre", "follower_active_start"])
print(df_time_genre_influence.loc[df_time_genre_influence["influencer_main_genre"]=="Unknown"])
print(df_time_genre_influence.loc[df_time_genre_influence["follower_main_genre"]=="Unknown"])



df_time_genre_influence['ratio'] = df_time_genre_influence['count_x']/df_time_genre_influence['count_y']
print(df_time_genre_influence[:50].round(2))

df_time_genre_influence.to_csv('./data/task3_time_genre_influence.csv', index=False)

