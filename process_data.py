import pandas as pd

# 初始化读取数据
full_music_data = pd.read_csv('./data/full_music_data.csv')
data_by_artist = pd.read_csv('./data/data_by_artist.csv')


def get_name_by_id(artist_id):
    artist_id_df = data_by_artist[data_by_artist['artist_id'] == artist_id]
    artist_name = artist_id_df['artist_name']
    return artist_name.values[0]



print(get_name_by_id(792507))