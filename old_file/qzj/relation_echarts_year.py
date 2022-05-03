import json
import os
from pyecharts import options as opts
from pyecharts.charts import Graph, Page
import numpy as np
import pandas as pd
from tqdm import tqdm
import random
import time

time_start=time.time()

data_by_artist1 = pd.read_csv('qzj/data/data_by_artist.csv')

def get_id_by_name(artist_name):
    artist_name_df = data_by_artist1[data_by_artist1['artist_name'] == artist_name]
    artist_id = artist_name_df['artist_id']
    try:
        a = artist_id.values[0]
    except:
        a = 'none'
    return a
weightdf = pd.read_csv('qzj/data/entropy_weight_sort.csv')
def get_weight(name):
    ids = get_id_by_name(name)
    weight_df = weightdf[weightdf['artist_id'] == ids]
    weight = weight_df['entropy_weight']
    try:
        b = weight.values[0]
    except:
        b = 0
    return b

def randomcolor():
    colorArr = ['1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']
    color = ""
    for i in range(6):
        color += colorArr[random.randint(0,14)]
    return "#"+color

def get_name_by_id(artist_id):
    artist_id_df = data_by_artist1[data_by_artist1['artist_id'] == artist_id]
    artist_name = artist_id_df['artist_name']
    return artist_name.values[0]

datapath3 = 'cyz/data/data_by_artist_with_genre.csv'
def get_genre_by_name(artistname):
    genre_tmp = pd.read_csv(datapath3)
    genre_df = genre_tmp[genre_tmp['artist_name'] == artistname]
    return genre_df['genre'].values[0]


datapath = 'qzj/data/influence_data.csv'
dataset = pd.read_csv(datapath)  #读取数据

data_by_artist = pd.read_csv('cyz/data/data_by_artist_with_genre.csv') 

chosen_genre = 'world'
#chosen_df = dataset[dataset['follower_main_genre'] == chosen_genre]
chosen_df = dataset
years = chosen_df['influencer_active_start'].unique()

color_list = ['#FE0000', '#F35A13', '#FDA40A', '#F9ED0D', '#BCFD04', '#84FE2B', '#4BF637', '#2DFD59', '#24F893', '#0FF9D4', '#31D8F8', '#2C9BFE', '#1545F9', '#4B37F5', '#6E0BF6', '#C62DFD', '#F914ED', '#FD1AA9', '#F53370', '#FC0606']
follower_main_genre_list = dataset['follower_main_genre'].unique()
influencer_name_list = dataset['influencer_main_genre'].unique()
name_list = influencer_name_list.tolist()
name_color = dict(zip(name_list, color_list))

nodes = []
nodes_list = []
cat_list = []
#nodes = np.append(follower_id_list, influencer_id_list)
nodes = data_by_artist['artist_name'].tolist()
nodes = np.unique(nodes)

for i in tqdm(nodes):
    #i = get_name_by_id(i)
        
    cat_df = data_by_artist[data_by_artist['artist_name'] == i]
    try:
        cat = cat_df['genre'].values[0]
    except:
        cat = 'none'
    cat_list.append(cat)
    color = name_color[cat]
    weight = get_weight(i)
    symbol = 13000*weight
    if symbol > 7:
        nodes_list.append({'name':i, 'symbolSize':symbol, 'category':cat, "label_opts": opts.LabelOpts(color=color)})

links_num_list = []
# ['Pop/Rock' 'Electronic' 'Reggae' 'Jazz' 'Country' 'Comedy/Spoken' 'R&B;' 'Classical' 'Latin' 'Vocal' 'Folk' 'Easy Listening' 'International' 'Avant-Garde' 'Blues' 'Stage & Screen' 'New Age' 'Religious' "Children's" 'Unknown']
#genre_increase = "Country"
# 按时间分为不同的HTML，catageroy还是genre
for year in years:
    #year = 1930
    
    links = []
    categories = []
    tmp_df1 = chosen_df.groupby(['influencer_active_start']).get_group(year)
    # 如果要累加的话，在这里写个year的循环，将当前year之前的所有year都get_group到tmp_df1里面
    
    new_year_list = [year-10*x for x in range(0 , 11) if (year-10*x)>1929]
    tmp_df1 = pd.DataFrame()
    for i in new_year_list:
        tmp_df0 = chosen_df.groupby(['influencer_active_start']).get_group(i)
        tmp_df1 = pd.concat([tmp_df0, tmp_df1])
    
    follower_id_list = tmp_df1['follower_id'].unique()
    influencer_id_list = tmp_df1['influencer_id'].unique()

    # 下面提出来links
    links_id = tmp_df1.values.tolist()
    
    for line in links_id:
        if ((line[3]<=year)and(line[7]<=year)):
            links.append({"source": str(line[1]), "target": str(line[5]), "label_opts": opts.LabelOpts(color='#FFFAFA')})
            #print(1)
    # 在这里计算当年累积的link数量，再计算其中不重复的node数，append到总的list里（for循环外定义空list） 
    # 还要看genre
    '''
    # 只对source的人进行分析
    links1 = []
    for lin in tqdm(links):
        tmp_source = lin['source']
        tmp_genre = get_genre_by_name(tmp_source)
        if tmp_genre == genre_increase:
            links1.append(lin)

    links_num = len(links1)
    source_list = []
    target_list = []
    for link in links1:
        source = link['source']
        target = link['target']
        source_list.append(source)
        target_list.append(target)
    # 其实nodes_tmp也可以作为整体的节点写入
    nodes_tmp = list(set(source_list) | (set(target_list)))
    nodes_num = len(nodes_tmp)
    links_num_list.append([genre_increase, year, nodes_num, links_num])
    '''
    for j in tqdm(cat_list):
        categories.append({'name': j, 'label_opts': opts.LabelOpts(color=randomcolor())})
    
    filename = 'qzj/relation_year/Low_symbolCumulative' + chosen_genre + str(year) + '.html'
    graph= (
            Graph(init_opts=opts.InitOpts(width="3000px", height="1500px"))
            .add("", 
                 nodes=nodes_list, 
                 links=links,
                 categories=categories,
                 #layout="force"
                 repulsion=8000,
                 edge_symbol= ['circle', 'arrow'],
                 layout="force",
                 gravity=0.1,
                 label_opts=opts.LabelOpts(is_show=True)
                 )
            .set_global_opts(title_opts=opts.TitleOpts(title="title"))
            .render(filename)
        )
        
# 非累加结果
#out = pd.DataFrame(columns=['genre', 'year', 'nodes_num', 'links_num'], data=links_num_list)
#filepath = 'qzj/relation_year/' + genre_increase.replace('/', ' ') +'.csv'
#out.to_csv(filepath)

time_end=time.time()
print('time cost',time_end-time_start,'s')