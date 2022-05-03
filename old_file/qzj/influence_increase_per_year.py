import pandas as pd
import numpy as np
import os
import pyecharts.options as opts
from pyecharts.charts import Line
import matplotlib.pyplot as plt

#创建一个空列表，存储当前目录下的CSV文件全称
file_name = []
  
#获取当前目录下的CSV文件名
#将当前目录下的所有文件名称读取进来
a = os.listdir('qzj/relation_year/')
dict_list = []
for j in a:
    #判断是否为CSV文件，如果是则存储到列表中
    if os.path.splitext(j)[1] == '.csv':
        file_name.append(j)
for filename in file_name:
    filepath = 'qzj/relation_year/' + filename
    tmpdf = pd.read_csv(filepath)
    genre = tmpdf['genre'].values[0]
    year_list = tmpdf['year'].tolist()
    tmpdf['nodes_sum'] = 0
    tmpdf['links_sum'] = 0
    count = 0
    for year in year_list:
        new_year_list = [year-10*x for x in range(0 , 11) if (year-10*x)>1929]
        tmp_df1 = pd.DataFrame()
        for i in new_year_list:
            tmp_df0 = tmpdf.groupby(['year']).get_group(i)
            tmp_df1 = pd.concat([tmp_df0, tmp_df1])
        # tmp_df1 就是当年之前所有的dataframe
        nodes_sum = tmp_df1['nodes_num'].sum()
        links_sum = tmp_df1['links_num'].sum()
        tmpdf.loc[count, 'nodes_sum'] = nodes_sum
        tmpdf.loc[count, 'links_sum'] = links_sum
        count = count + 1
        #print(2)
    outname = 'qzj/relation_year/' + genre.replace('/', ' ') + '_sum.csv'
    tmpdf = tmpdf.sort_values(by='year')
    tmpdf.to_csv(outname)
    n_list = tmpdf['nodes_sum'].tolist()
    l_list = tmpdf['links_sum'].tolist()
    y_list = tmpdf['year'].tolist()
    dict_list.append({'genre':genre, 'nodes_sum':n_list, 'links_sum':l_list, 'x_data':y_list})

    #print(1)


# 针对每个流派可视化
for genre_dict in dict_list:
    x_data = genre_dict['x_data']
    genre = genre_dict['genre']
    nodes_data = genre_dict['nodes_sum']
    links_data = genre_dict['links_sum']
    plt.title(genre)
    plt.plot(x_data, nodes_data, color='green', label='nodes_sum')
    plt.plot(x_data, links_data, color='blue', label='links_sum')
    plt.legend()
    plt.xlabel('year')
    plt.ylabel('num')
    pltpath = 'qzj/relation_year/' + genre.replace('/', ' ') + '_sum.png'
    plt.savefig(pltpath)
    plt.close()
    #plt.show()
    #print(2)
    '''
    figure_name = 'qzj/relation_year/' + genre.replace('/', ' ') + '_sum.html'
    (
        Line(init_opts=opts.InitOpts(width="1600px", height="800px"))
        
        .add_xaxis(xaxis_data=x_data)
        .add_yaxis(
            series_name="nodes",
            y_axis=nodes_data,
            symbol="emptyCircle",
            is_symbol_show=True,
            #label_opts=opts.LabelOpts(is_show=False),
        )
        .add_yaxis(
            series_name="links",
            y_axis=links_data,
            symbol="emptyCircle",
            is_symbol_show=True,
            #label_opts=opts.LabelOpts(is_show=False),
        )
        .set_global_opts(
            tooltip_opts=opts.TooltipOpts(is_show=False),
            xaxis_opts=opts.AxisOpts(type_="category"),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
        )
        .render(figure_name)
    )
    '''

print(1)