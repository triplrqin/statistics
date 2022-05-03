import pandas as pd
import numpy as np
from tqdm import tqdm

datapath1 = 'qzj/data/influence_data.csv'
datapath2 = 'qzj/data/data_by_artist.csv'
datapath3 = 'cyz/data/data_by_artist_with_genre.csv'

influence_data = pd.read_csv(datapath1)
data_by_artist = pd.read_csv(datapath2)
artist_genre = pd.read_csv(datapath3)
unknown_artist_id = artist_genre.loc[artist_genre['genre'] == 'Unknown']
unknown_artist_id = unknown_artist_id['artist_id'].to_list()

data_by_artist['follower_num'] = 0

links_id = influence_data[['influencer_name', 'follower_name']].values.tolist()
# df.drop(df.index[2])
#for person in influence_data[['influencer_name']]:
#    sub_influence = []
# 使用ID不会出现乱码
sub_influence_df = influence_data.groupby(['influencer_id'])[['follower_id']].count()
sub_influence_df.rename(columns={'follower_id': 'follower_num'})
influence_data = influence_data.set_index('influencer_id')

data_by_artist = data_by_artist[~data_by_artist['artist_id'].isin(unknown_artist_id)]

data_by_artist_origin = data_by_artist
data_by_artist = data_by_artist.set_index('artist_id')

#for_count = 0
for artist_id in tqdm(data_by_artist_origin['artist_id']):
    #tmp = data_by_artist.loc[data_by_artist_origin['artist_id']==artist_id]
    if artist_id in sub_influence_df.index.to_list():
        data_by_artist.loc[artist_id, 'follower_num'] = sub_influence_df.loc[artist_id].values[0]
        #for_count = for_count + 1
    else:
        data_by_artist.loc[artist_id, 'follower_num'] = 0
        #for_count = for_count + 1

matrix = data_by_artist.reset_index()
matrix = matrix[['artist_id', 'popularity', 'count', 'follower_num']]
matrix.to_csv('qzj/data/entropy_weight.csv')
print(1)