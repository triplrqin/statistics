import pandas as pd

data_by_artist = pd.read_csv('data/data_by_artist.csv')
influence_data = pd.read_csv('data/influence_data.csv')

def get_name_by_id(artist_id):
    artist_id_df = data_by_artist[data_by_artist['artist_id'] == artist_id]
    artist_name = artist_id_df['artist_name']
    return artist_name.values[0]
# print(get_name_by_id(792507))

# follower
def get_year_by_follower_id(follower_id):
    follower_id_df = influence_data[influence_data['follower_id'] == follower_id]
    follower_active_start = follower_id_df['follower_active_start']
    year = follower_active_start.values[0]
    return year
# print(get_year_by_follower_id(759491))
# print(1)