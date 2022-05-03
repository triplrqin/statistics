import pandas as pd
from tqdm import tqdm
import json

dataset = pd.read_csv('cyz/data/task3_time_genre_influence_new.csv')

x_data = [1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010]
color_list = ['#F71B1B', '#FAFA16', '#16F816', '#1BF6F6', '#1A1AFA', '#F72DF7', '#4BF637', '#2DFD59', '#24F893', '#0FF9D4', '#31D8F8', '#2C9BFE', '#1545F9', '#4B37F5', '#6E0BF6', '#C62DFD', '#F914ED', '#FD1AA9', '#F53370', '#FC0606']

follower_main_genre_list = dataset['follower_main_genre'].unique()
influencer_name_list = dataset['influencer_main_genre'].unique()
name_list = influencer_name_list.tolist()
name_color = dict(zip(name_list, color_list))
follower_main_genre_list = ['Pop/Rock', 'R&B;', 'Jazz', 'Country', 'Latin', 'Electronic']
for follower_genre in tqdm(follower_main_genre_list):
    # 针对一个follower
    follower_df = dataset[dataset['follower_main_genre'] == follower_genre]
    
    datalist = []
    ratiolist = [0,0,0,0,0,0,0,0,0]
    
    for name in influencer_name_list:
        tmp = follower_df[follower_df['influencer_main_genre'] == name]
        tmp = tmp.reset_index(drop=True)
        x_df = pd.DataFrame(x_data)
        x_df['ratio'] = 0
        x_df = x_df.set_index(0)
        #count = 0
        for year in tmp['follower_active_start']:
            tmp2 = tmp[tmp['follower_active_start'] == year]
            x_df.loc[year, 'ratio'] = tmp2['ratio'].values[0]
            #count = count + 1

        ratiolist = x_df['ratio'].to_list()
        color = name_color[name]
        for a in range(1,len(ratiolist)):
            if ratiolist[a] == 0:
                ratiolist[a] = ratiolist[a-1]
        datalist.append({"name":name, "data":ratiolist, "color":color})

    filename = 'qzj/task3_time_genre_influence/new_color/' + follower_genre.replace('/', '') + '.json'
    #json.dumps(datalist)
    with open(filename,"w") as f:
        json.dump(datalist,f)

    #print(2)


print(1)