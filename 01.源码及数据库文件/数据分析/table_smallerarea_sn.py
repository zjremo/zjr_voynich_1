from matplotlib import pyplot as plt
import pandas as pd
import operator


import plotly.graph_objects as go
import plotly as py
font = {
    'family':'SimHei',
    'weight':'bold',
    'size':'14'
}
plt.rc('font',**font)
plt.rc('axes',unicode_minus=False)
# 导入数据
data = pd.read_csv('D:/venvs/temp/Scripts/datades/house_info.csv')
# DataFrame化
listings_df = pd.DataFrame(data)
# 打印初步信息
print('记录行数为：{}'.format(len(listings_df)))
print(listings_df.count())        # 统计每一行的非NA单元数
# 租金整体分析
streets = listings_df['街道']
mylist = []
for street in streets:
    s = str(street).split(" ")
    if(s[0]):
        if(1-operator.contains(s[0],'区')):
            s[0]+='区'
    else:
        s[0] += '其他区'
    mylist.append(s[0])
listings_df['区域'] = mylist


# 天津市各个区域的租金均价整理，并进行统计分析
# 按标签索引整理不同区域的租金均值
rent_money_av = round(listings_df.groupby(['小区'])['租金'].mean(),2)
print(rent_money_av)
x_1 = rent_money_av.index.tolist()
y_1 = rent_money_av.values.tolist()
# 创建表格数据
trace=go.Table(header=dict(values=['小区名','租金均价'],
                           line_color="black", # 表头线条颜色
                           fill_color="#44cef6",  # 表头填充色
                           align="center"),             # 文本居中
               cells=dict(values=[x_1,    # 第1列数据
                                  y_1],     # 第2列数据
                          line_color = "black", # 表格线条颜色
                          fill_color = "#228B22",  # 表格填充色
                          align = "center"))            # 文本居中
# 将图轨转换为列表
data=[trace]
layout=go.Layout(width=500,height=20000)
# 将图轨和图层合并
fig = go.Figure(data=data, layout=layout)
py.offline.plot(fig)