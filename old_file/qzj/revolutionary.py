import numpy as np
import pandas as pd
from tqdm import tqdm

datapath2 = 'qzj/data/entropy_weight_sort.csv'
entropy_df = pd.read_csv(datapath2) 
entropy_id_list = entropy_df['artist_id'].to_list()
entropy_id_list = entropy_id_list[0:100]

datapath = 'qzj/data/influence_data.csv'
dataset = pd.read_csv(datapath) # 影响力数据
count = 1
for chosen in entropy_id_list:
    chosen_df = pd.DataFrame()
    follower_df = dataset[dataset['influencer_id'] == chosen]
    #chosen_df['himself_id'] = follower_df['influencer_id']
    tmp1 = follower_df['follower_id']
    tmp1 = tmp1.reset_index(drop=True)

    influencer_df = dataset[dataset['follower_id'] == chosen]
    tmp2 = influencer_df['influencer_id']
    tmp2 = tmp2.reset_index(drop=True)

    chosen_df = pd.concat([tmp1, tmp2], axis=1)
    chosen_df['himself_id'] = chosen

    filename = 'qzj/revolutionary/' + str(count) + '.csv'
    chosen_df.to_csv(filename)
    count = count + 1
    #print(2)

print(1)