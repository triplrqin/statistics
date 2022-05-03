import pandas as pd
import numpy as np
from sklearn import preprocessing
import matplotlib.pyplot as plt
import os

df1 = pd.read_csv('data_task3.csv')

file_list=os.listdir('revolutionary')

final_array = np.zeros([100,5])

def commute(a,b):
    a_norm = np.linalg.norm(a)
    b_norm = np.linalg.norm(b)
    cos = np.dot(a, b) / (a_norm * b_norm)
    return cos

#for i in range(len(file_list)):
def tuiduan(i):
    df_2 = pd.read_csv('revolutionary/' + file_list[i])

    BYX_people = df_2.iloc[:, 1]  # 取出follwer
    YX_people = df_2.iloc[:, 2]  # 取出influncer
    BYX_people = BYX_people[~np.isnan(BYX_people)]
    YX_people = YX_people[~np.isnan(YX_people)]
    A = df1[df1['artist_id'].isin([df_2.iloc[0, 3]])].iloc[0, [2,3,4,5,8,10]]  # 取出中间人A,并只取出2：13行12个变量

    YX_total = 0
    BYX_total = 0
    for j1 in range(len(BYX_people)):
        if(df1[df1['artist_id'].isin([BYX_people[j1]])].shape[0] == 0):
            continue
        else:
            BYX_tmp = df1[df1['artist_id'].isin([BYX_people[j1]])].iloc[0,[2,3,4,5,8,10]]

            BYX_total += commute(BYX_tmp,A)
    BYX_averange = BYX_total/(len(BYX_people)+1)
    for j2 in range(len(YX_people)):
        if(df1[df1['artist_id'].isin([YX_people[j2]])].shape[0] == 0):
            continue
        else:
            YX_tmp = df1[df1['artist_id'].isin([YX_people[j2]])].iloc[0,[2,3,4,5,8,10]]

            YX_total += commute(YX_tmp,A)

    YX_averange = YX_total/(len(YX_people)+1)
    final_array[i, 0] = df_2.iloc[0, 3]
    final_array[i, 1] = BYX_averange
    final_array[i, 2] = YX_averange
    final_array[i, 3] = len(BYX_people)
    final_array[i, 4] = len(YX_people)
    return final_array[i]
for i in range(100):
    tuiduan(i)

final_data = pd.DataFrame()
final_data['himself_id'] = final_array[:, 0]
final_data['follower_score'] = final_array[:, 1]
final_data['influencer_score'] = final_array[:, 2]
final_data['follower_num'] = final_array[:, 3]
final_data['influencer_num'] = final_array[:, 4]

print('end')
final_data.to_csv('100_atrist.csv',index=False)