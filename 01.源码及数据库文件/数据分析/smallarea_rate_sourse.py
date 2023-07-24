import csv
from matplotlib import pyplot as plt
import pandas as pd
import plotly.graph_objects as go
import plotly as py
font = {
    'family':'SimHei',
    'weight':'bold',
    'size':'14'
}
plt.rc('font',**font)
plt.rc('axes',unicode_minus=False)
# 数据初始化
data_init = []
# 导入数据
with open('assistant_info.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        data_init.append(row)
data_init_temp = []
num = [3,4,5,6]
for data in data_init:
    for n in num:
        if data[n] == '':
            data[2] = data[2]+''
        else:
            data[2] = data[2]+'\n'+data[n]
    data_init_temp.append([data[0],data[1],data[2]])
del data_init_temp[0]

listings_df = pd.DataFrame(data_init_temp,columns=['小区','问题','答案'])
print(listings_df)

# 感兴趣的问题都有哪些
# 首先进行第一次清洗,去重
question_set  = set(list(listings_df['问题']))
# print(question_set)
question_temp = list(question_set)
question = []
# 去空
for que in question_temp:
    if que != '':
        question.append(que)
print(question)

# 1. 小区评论热度
rate_count = listings_df.groupby(['小区']).count()
# print(rate_count)
smallarea = rate_count.index.tolist()
num_temp = rate_count.values.tolist()
num = []
for ele in num_temp:
    num.append(ele[0])
# print(num)
# 来一个降序排列，制作网页表格
data_need = []
for ele in range(len(num)):
    data_need.append([smallarea[ele],num[ele]])
# print(data_need)
data_need.sort(key=lambda x:x[1],reverse=True)
print(data_need)

data_x = []
data_y = []
for ele in data_need:
    data_x.append(ele[0])
    data_y.append(ele[1])
trace=go.Table(header=dict(values=['小区名','评论数'],
                           line_color="black", # 表头线条颜色
                           fill_color="#44cef6",  # 表头填充色
                           align="center"),             # 文本居中
               cells=dict(values=[data_x,    # 第1列数据
                                  data_y],     # 第2列数据
                          line_color = "black", # 表格线条颜色
                          fill_color = "#228B22",  # 表格填充色
                          align = "center"))            # 文本居中
# 将图轨转换为列表
data=[trace]
layout=go.Layout(width=500,height=20000)
# 将图轨和图层合并
fig = go.Figure(data=data, layout=layout)
py.offline.plot(fig)
