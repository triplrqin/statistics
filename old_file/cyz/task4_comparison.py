import pandas as pd
import matplotlib.pyplot as plt
from random import seed
from random import random
import numpy as np
from sklearn import preprocessing
from scipy import stats

file_influ_foll = "./data/influence_data.csv"
file_feature = "./data/data_by_artist_with_genre.csv"

df_infl_fol = pd.read_csv(file_influ_foll, sep=',')
df_feature = pd.read_csv(file_feature, sep=',')

features = ['danceability','energy','valence','tempo','loudness','mode','key',  'acousticness',  'instrumentalness',  'liveness',  'speechiness',  'duration_ms']

min_max = preprocessing.MinMaxScaler()
tmp = df_feature[features].values
tmp = min_max.fit_transform(tmp)
df_feature[features] = tmp

genre = 'Pop/Rock'
# 只讨论POP/ROCK这个流派
df_infl_fol = df_infl_fol.loc[(df_infl_fol['influencer_main_genre']==genre)&(df_infl_fol['follower_main_genre']==genre)]

influencer_id = int(df_infl_fol.sample()['influencer_id'])
influencer_id = 894465 # Rolling Stone
# influencer_id = 754032 # The Beatles
# influencer_id = 66915 # Bob Dylan
print("influencer_id:", influencer_id)
artist_name = df_feature.loc[df_feature['artist_id']==influencer_id]['artist_name'].values[0]
print("artist name:", artist_name)

df_fol_ids = df_infl_fol[df_infl_fol['influencer_id']==influencer_id]['follower_id']
df_ex_fol_ids = df_infl_fol[~df_infl_fol['influencer_id']==influencer_id]['follower_id']




df_genre = df_feature.loc[df_feature['genre']==genre]



df_influ = df_genre.loc[df_genre['artist_id']==influencer_id]
df_fol = df_genre.loc[df_genre['artist_id'].isin(df_fol_ids)]
df_ex_fol = df_genre.loc[~df_genre['artist_id'].isin(df_fol_ids)]



arr_influ = df_influ[features].to_numpy()
arr_fol = df_fol[features].to_numpy()
arr_ex_fol = df_ex_fol[features].to_numpy()

norm_fol = np.sqrt(np.sum(np.square(arr_fol),axis=1))
norm_ex_fol = np.sqrt(np.sum(np.square(arr_ex_fol),axis=1))
norm_influ = np.sqrt(np.sum(np.square(arr_influ),axis=1))

num_fol = norm_fol.shape[0]
num_ex_fol = norm_ex_fol.shape[0]
print("follower number:", num_fol)
print("non-follower number:", num_ex_fol)

sim_fol = np.sum(arr_influ*arr_fol,axis=1)/(norm_fol*norm_influ)
sim_ex_fol = np.sum(arr_influ*arr_ex_fol,axis=1)/(norm_ex_fol*norm_influ)

# 精确到小数点后2位便于划分区间
sim_fol = np.round(sim_fol, 2)
sim_ex_fol = np.round(sim_ex_fol, 2)

df_sim_fol = pd.DataFrame(sim_fol, columns=['cos_sim'])
df_sim_ex_fol = pd.DataFrame(sim_ex_fol, columns=['cos_sim'])
df_sim_fol = df_sim_fol.sort_values(['cos_sim'])
df_sim_ex_fol = df_sim_ex_fol.sort_values(['cos_sim'])





# KS test
res = stats.kstest(df_sim_fol['cos_sim'], df_sim_ex_fol['cos_sim'], N=100, alternative='two-sided') # 'two-sided'
print(res)


# 概率分布函数
# df_sim_ex_fol['count'] = 1
# df_sim_fol['count'] = 1
# df_sim_fol = df_sim_fol.groupby('cos_sim')['count'].sum().reset_index()
# df_sim_ex_fol = df_sim_ex_fol.groupby('cos_sim')['count'].sum().reset_index()
# plt.subplot(1,2,1)
# plt.bar(df_sim_fol['cos_sim'], df_sim_fol['count']/num_fol, width=0.01, label="Followers")
# plt.xlim([0,1])
# plt.xlabel("Cosine similarity")
# plt.ylim([0, 0.15])
# plt.legend()
# plt.grid()


# plt.subplot(1,2,2)
# plt.bar(df_sim_ex_fol['cos_sim'], df_sim_ex_fol['count']/num_ex_fol, width=0.01, color='darkorange', label='Non-followers')
# plt.xlim([0,1])
# plt.xlabel("Cosine similarity")
# plt.ylim([0, 0.15])
# plt.legend()
# plt.grid()

# plt.savefig("./data/PDF {}.png".format(artist_name))
# plt.show()


# 累计概率分布函数
# fig, ax = plt.subplots(figsize=(8, 4))
# ax.hist(df_sim_fol['cos_sim'], bins=100, density=True, histtype='step', cumulative=True, label='CDF of followers')
# ax.hist(df_sim_ex_fol['cos_sim'], bins=100, density=True, histtype='step', cumulative=True, label='CDF of non-followers')
# ax.legend()
# ax.grid()
# plt.savefig("./data/CDF {}.png".format(artist_name))
# plt.show()
