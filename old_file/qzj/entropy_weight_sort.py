import pandas as pd

datapath1 = 'qzj/data/entropy_weight_matlab.csv'
influence_data = pd.read_csv(datapath1, header=None)
influence_data = influence_data[[1,2,3,4,5]]
influence_data.columns =['artist_id','popularity','count','follower_num','entropy_weight']
sort_df = influence_data.sort_values(by=['entropy_weight'], ascending=False)
sort_df = sort_df.reset_index(drop=True)
sort_df.to_csv('qzj/data/entropy_weight_sort.csv')
print(1)