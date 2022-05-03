import json
import os
from pyecharts import options as opts
from pyecharts.charts import Graph, Page
import numpy as np
import pandas as pd
from tqdm import tqdm
import random

def randomcolor():
    colorArr = ['1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']
    color = ""
    for i in range(6):
        color += colorArr[random.randint(0,14)]
    return "#"+color

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

datapath = 'qzj/data/influence_data.csv'
dataset = pd.read_csv(datapath)  #读取数据
#get_weight('2 Brothers on the 4th Floor')
data_by_artist = pd.read_csv('cyz/data/data_by_artist_with_genre.csv') 
#data = dataset.values[:, :]
#influencer_id = dataset['influencer_id'].values.tolist()
#follower_id = dataset['follower_id'].values.tolist()
#links_id = dataset[['influencer_id', 'follower_id']].values.tolist()
links_id = dataset[['influencer_name', 'follower_name', 'influencer_id', 'influencer_main_genre', 'follower_main_genre']].values.tolist()
#id_list_df = pd.concat([dataset['influencer_id'], dataset['follower_id']])

# 选影响力前n位，画关系图
datapath2 = 'qzj/data/entropy_weight_sort.csv'
entropy_df = pd.read_csv(datapath2) 
entropy_id_list = entropy_df['artist_id'].to_list()
entropy_id_list = entropy_id_list[0:10]
#id_list = id_list_df.unique().tolist()
links = []
nodes = []
#nodes_list = []
for line in tqdm(links_id):
    if line[2] in entropy_id_list:
        links.append({"source": str(line[0]), "target": str(line[1]), "label_opts": opts.LabelOpts(color='#FFFAFA')})
        nodes.append(line[0])
        nodes.append(line[1])
        '''
        name_list = []
        for i in nodes:
            name_list.append(i['name'])
        if ~(line[0] in name_list):
            nodes.append({'name': str(line[0]), 'symbolSize':10, 'category': line[3]})
        if ~(line[1] in name_list):
            nodes.append({'name': str(line[1]), 'symbolSize':10, 'category': line[4]})
        '''


nodes_list = []
cat_list = []
nodes = data_by_artist['artist_name'].tolist()
nodes = np.unique(nodes)
for i in tqdm(nodes):
    cat_df = data_by_artist[data_by_artist['artist_name'] == i]
    try:
        cat = cat_df['genre'].values[0]
    except:
        cat = 'none'
    cat_list.append(cat)
    weight = get_weight(i)
    symbol = 13000*weight
    if symbol > 13:
        nodes_list.append({'name':str(i), 'symbolSize':symbol, 'category':cat})

categories = []
for j in tqdm(cat_list):
    categories.append({'name': j, 'label_opts': opts.LabelOpts(color=randomcolor())})

influencer_list_first = []
follower_list_first = []
for link in links:
    influencer_first = link['source']
    influencer_list_first.append(influencer_first)
    follower_first = link['target']
    follower_list_first.append(follower_first)
node_name = []
for node in nodes_list:
    node_name.append(node['name'])
# follower_list_first 与node取交集
follower_list_first = list(set(follower_list_first) & set(node_name)) 
influencer_list_second = [item for item in follower_list_first if item not in influencer_list_first]
# influencer second确定要有能影响的人，就是在influencer里面
total_influencer = dataset['influencer_name'].tolist()
influencer_list_second = list(set(influencer_list_second) & set(total_influencer))
links2 = []
nodes2 = []

for influencer2 in tqdm(influencer_list_second):
    second = dataset[dataset['influencer_name'] == influencer2]
    line2_list = second[['influencer_name', 'follower_name', 'influencer_id', 'influencer_main_genre', 'follower_main_genre']].values.tolist()
    for line2 in line2_list:
        links2.append({"source": line2[0], "target": line2[1], "label_opts": opts.LabelOpts(color='#FFFAFA')})
        weight = get_weight(line2[1])
        symbol = 15000*weight
        cat = line2[4]
        if symbol>5:   
            nodes2.append({'name':line2[1], 'symbolSize':symbol, 'category':cat})

#nodes_list.extend(nodes2)
links.extend(links2)

# 去重
def deleteDuplicate(li):
    temp_list = list(set([str(i) for i in li]))
    li=[eval(i) for i in temp_list]
    return li
#nodes_list = deleteDuplicate(nodes_list)
#links = deleteDuplicate(links)

filename = 'qzj/top10_weight_second.html'
graph= (
        Graph(init_opts=opts.InitOpts(width="3000px", height="1500px"))
        .add("", 
             nodes=nodes_list, 
             #nodes=nodes2, 
             links=links,
             #links=links2,
             categories=categories,
             #layout="force"
             repulsion=15000,
             edge_symbol= ['circle', 'arrow'],
             layout="force",
             is_draggable=True,
             gravity=0.1,
             label_opts=opts.LabelOpts(
                # is_show=True 是否显示标签
                is_show=True,
                
            
                # position 标签的位置 可选 'top'，'left'，'right'，'bottom'，'inside'，'insideLeft'，'insideRight'.....
                #position='bottom',
            
                # font_size 文字的字体大小
                #font_size=10,
            
                # color 文字的颜色
                #color= '#FF6633',
            
                # font_style 文字字体的风格，可选 'normal'，'italic'，'oblique'
                #font_style = 'italic' , #斜体
            
                # font_weight 文字字体的粗细  'normal'，'bold'，'bolder'，'lighter'
                #font_weight = None,
            
                # font_family 字体 'Arial', 'Courier New', 'Microsoft YaHei（微软雅黑）' ....
                #font_family = None,
            
                # rotate 标签旋转 从 -90 度到 90 度。正值是逆时针
                #rotate = '0',
            
                # margin 刻度标签与轴线之间的距离
                #margin = 20,
            
                # 坐标轴刻度标签的显示间隔，在类目轴中有效。Union[Numeric, str, None]
                # 默认会采用标签不重叠的策略间隔显示标签。
                # 可以设置成 0 强制显示所有标签。
                # 如果设置为 1，表示『隔一个标签显示一个标签』，如果值为 2，表示隔两个标签显示一个标签，以此类推。
                # 可以用数值表示间隔的数据，也可以通过回调函数控制。回调函数格式如下：
                # (index:number, value: string) => boolean
                # 第一个参数是类目的 index，第二个值是类目名称，如果跳过则返回 false。
                #interval = None,
            
                # horizontal_align 文字水平对齐方式，默认自动。可选：'left'，'center'，'right'
                #horizontal_align = 'center',
            
                # vertical_align 文字垂直对齐方式，默认自动。可选：'top'，'middle'，'bottom'
                #vertical_align = None,
            
                )
             )
        .set_global_opts(title_opts=opts.TitleOpts(title="title"))
        .render(filename)
        
    )

print(1)