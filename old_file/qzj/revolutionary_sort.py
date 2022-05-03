import numpy as np
import pandas as pd
from tqdm import tqdm

datapath = 'zjy/100_atrist.csv'
rev_df = pd.read_csv(datapath)
#rev_id_list = rev_df['himself_id'].to_list()

entropy_df = pd.read_csv('qzj/data/entropy_weight_sort.csv')
data_by_artist1 = pd.read_csv('qzj/data/data_by_artist.csv')
def get_name_by_id(artist_id):
    artist_id_df = data_by_artist1[data_by_artist1['artist_id'] == artist_id]
    artist_name = artist_id_df['artist_name']
    return artist_name.values[0]

def get_weight(ID):
    tmp = entropy_df[entropy_df['artist_id'] == ID]
    return tmp['entropy_weight'].values[0]

rev_df['num_ratio'] = rev_df['follower_num']/(rev_df['influencer_num']+1)
rev_df['num_ratio_one'] = rev_df['num_ratio']/rev_df['num_ratio'].max()

rev_df['similarity_ratio'] = rev_df['follower_score']/(rev_df['influencer_score']+1)
rev_df['similarity_ratio_one'] = rev_df['similarity_ratio']/rev_df['similarity_ratio'].max()

rev_df['entropy_weight'] = 0
rev_df['artist_name'] = ''
count = 0
for himself in rev_df['himself_id']:
    tmp = rev_df[rev_df['himself_id'] == himself]
    weight = get_weight(himself)
    rev_df.loc[count, 'entropy_weight'] = weight
    name = get_name_by_id(himself)
    rev_df.loc[count, 'artist_name'] = name
    count = count + 1

rev_df['entropy_weight_one'] = rev_df['entropy_weight']/rev_df['entropy_weight'].max()

rev_df['revolution_add'] = rev_df['similarity_ratio_one'] + rev_df['num_ratio_one'] + rev_df['entropy_weight_one']
rev_df['revolution_multi'] = rev_df['similarity_ratio_one'] * rev_df['num_ratio_one'] * rev_df['entropy_weight_one']

rev_df.to_csv('qzj/revolution_sort_100.csv')
print(1)