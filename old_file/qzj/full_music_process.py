import pandas as pd

FullMusicData = pd.read_csv('qzj/data/full_music_data.csv')
ArtistGenre = pd.read_csv('cyz/data/data_by_artist_with_genre.csv')


def getGenre(artistid):
    genre_df = ArtistGenre[ArtistGenre['artist_id'] == int(artistid)]
    return genre_df['genre'].values[0]


data_by_artist1 = pd.read_csv('qzj/data/data_by_artist.csv')


def get_id_by_name(artist_name):
    artist_name_df = data_by_artist1[data_by_artist1['artist_name'] == artist_name]
    artist_id = artist_name_df['artist_id']
    try:
        a = artist_id.values[0]
    except:
        a = 'none'
    return a


FullMusicData['artists_id'] = FullMusicData['artists_id'].apply(
    lambda x: x.replace('[', '').replace(']', ''))

df_split_row = FullMusicData.drop('artists_id', axis=1).join(FullMusicData['artists_id'].str.split(
    ',', expand=True).stack().reset_index(level=1, drop=True).rename('artists_id'))

#df_split_row['artists_id'] = df_split_row['artists_id'].apply(lambda x:x[1:-1])
df_split_row['year'] = df_split_row['year'].apply(
    lambda x: 10*(int(int(x)/10)))
df_split_row['artists_id'] = df_split_row['artists_id'].apply(lambda x: int(x))
# 下面这步巨慢无比
#df_split_row['genre'] = df_split_row['artists_id'].apply(lambda x:getGenre(x))

popularityDf = df_split_row.groupby(['artists_id', 'year'])[
    'popularity'].mean()

countDf = df_split_row.groupby(['artists_id', 'year'])['popularity'].count()

artistDf = pd.concat(
    [pd.DataFrame(popularityDf), pd.DataFrame(countDf)], axis=1)
artistDf.columns = ['popularity', 'count']
artistDf.to_csv('qzj/data/artistDf.csv')

influence_data = pd.read_csv('qzj/data/influence_data.csv')

# 注意每个人的影响年份从其active start的年份开始的。
# 按照follower的年份来划分什么时候受影响（放在假设中）
followerNum = influence_data.groupby(['influencer_id', 'follower_active_start'])[
    'follower_id'].count()
followerNum.to_csv('qzj/data/followerNum.csv')

select_genre = 'Pop/Rock'
artistDf2 = pd.read_csv('qzj/data/artistDf.csv')

idList = artistDf2['artists_id'].tolist()
# artistDf2.drop( ,inplace=True)
select_id = ArtistGenre.groupby(['genre']).get_group(
    'Pop/Rock')['artist_id'].tolist()
artistDf3 = artistDf2[artistDf2['artists_id'].isin(select_id)]

# 下面只针对选取的流派进行分析
filename = 'qzj/relation_year/' + select_genre.replace('/', ' ') + '_sum.csv'
genre_year_follower = pd.read_csv(filename)
artistDf4 = artistDf3[['year', 'popularity', 'count']]
genre_popul = artistDf4.groupby(['year'])['popularity'].sum()
genre_count = artistDf4.groupby(['year'])['count'].sum()
popul_list = genre_popul.tolist()[1:-1]
count_list = genre_count.tolist()[1:-1]
nodes_num = genre_year_follower['nodes_num'].tolist()
links_num = genre_year_follower['links_num'].tolist()

tmp = pd.concat([pd.DataFrame(popul_list), pd.DataFrame(
    count_list), pd.DataFrame(nodes_num), pd.DataFrame(links_num)], axis=1)
tmp.columns = ['popularity', 'count', 'nodes', 'links']
filename2 = 'qzj/data/' + select_genre.replace('/', ' ') + '.csv'
tmp.to_csv(filename2)

# weight:
# 0.2637    0.1979    0.2351    0.3033

chosen_artist = 'The Who'
artistID = get_id_by_name(chosen_artist)
chosenDF = artistDf3[artistDf3['artists_id'] == artistID]
followerNum1 = pd.read_csv('qzj/data/followerNum.csv')
follower_num_year = followerNum1[followerNum1['influencer_id'] == artistID]
chosenDF = chosenDF.reset_index(drop=True)
year_list = chosenDF['year'].tolist()
start_year = min(year_list)
reallen = len(year_list)
follower_year = follower_num_year['follower_active_start'].tolist()
addnum = 0
flaselen = len(follower_year)
for year in follower_year:
    if year < start_year:
        tmpnum = follower_num_year[follower_num_year['follower_active_start'] == year]['follower_id'].values[0]
        addnum = addnum + tmpnum
follower_num_year = follower_num_year.set_index('follower_active_start')
try:
    follower_num_year.loc[start_year,'follower_id'] = follower_num_year.loc[start_year,'follower_id'] + addnum
except:
    print(2)
ttt = follower_num_year['follower_id'].tolist()
diff = flaselen - reallen
follower_num_increase = ttt[diff:]
outdf = pd.concat([chosenDF, pd.DataFrame(follower_num_increase)], axis=1)
outdf = outdf.rename(columns={0:'follower_num'})
# 最后一列是影响的人数
filename3 = 'qzj/data/' + chosen_artist + '.csv'
outdf.to_csv(filename3)
# 0.2637    0.1979    0.2351    0.3033
print(1)
