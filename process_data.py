import pandas as pd
from sklearn import preprocessing
import numpy as np

#pd.pandas.set_option('display.max_colwidth',500)
# 初始化读取数据
full_music_data = pd.read_csv('./data/full_music_data.csv')
data_by_artist = pd.read_csv('./data/data_by_artist.csv')
top_id = pd.read_csv('./data/Top_100_ID.csv')
PCA = pd.read_csv('./data/PCA.csv')
music_data = pd.read_csv('./data/music_data_top100.csv')

def get_name_by_id(artist_id):
    artist_id_df = data_by_artist[data_by_artist['artist_id'] == artist_id]
    artist_name = artist_id_df['artist_name']
    return artist_name.values[0]

def get_music_by_id():
    for ID in top_id['artist_id']:
        full_music_data.loc[full_music_data['artists_id'].str.contains(str(ID)),'contains'] = True 
    music_data = full_music_data.loc[full_music_data['contains'] == True]
    #music_data.to_csv('./data/music_data_top100.csv', index=False, encoding='utf-8')
    return music_data

def process_pca(music_data):
    features = PCA['Unnamed: 0'][0:11].tolist()
    PCA_list = ['PC1','PC2','PC3','PC4','PC5','PC6','PC7']
    PCA7 = PCA[PCA_list].values
    # PCA转换前的feature_data
    features_data = music_data[features]

    # min-max标准化
    min_max = preprocessing.MinMaxScaler()
    # 归一化后的feature_data
    features_data_minmax = min_max.fit_transform(features_data.values)

    # 矩阵相乘
    pca_data = np.dot(features_data_minmax, PCA7) 

    # 格式转换与合并
    pca_df = pd.DataFrame(pca_data, columns=PCA_list)
    music_top100_nolabel=pd.concat([music_data[['artist_names','artists_id']],pca_df],axis=1)

    music_top100_nolabel.to_csv('./data/music_top100_nolabel.csv', index=False, encoding='utf-8')
    return music_top100_nolabel



#print(get_name_by_id(792507))
#music_data = get_music_by_id()
process_pca(music_data)
print(0)