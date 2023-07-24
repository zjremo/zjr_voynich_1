import re
import csv
import pandas as pd
import matplotlib.pyplot as plt
from pyecharts import options as opts
from pyecharts.charts import Map
import operator

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

# 为dataframe添加一列: 好坏,好为1，坏为0
rate_bad = []
question = list(listings_df['问题'])
ans = list(listings_df['答案'])
bad_words = [
    '.*不适合.*',
    '不.*好',
    '.*欠缺',
    '.*不.*齐全',
    '.*嘈杂',
    '.*略差',
    '没有.*地下车库',
    '.*未能.*',
    '.*紧张',
    '.*接受不了.*',
    '.*比较贵.*',
    '.*乱停乱放',
    '.*不足.*'
    '没有.*车位',
    '无.*车位',
    '.*差',
    '.*老旧',
    '.*拥堵',
    '没有.*绿化.*',
    '车位.*不足',
    '位置.*偏远',
    '交通.*不便',
    '物业费.*高',
    '.*不太好',
    '绿化率.*较低'
]
for ele in range(len(question)):
    if question[ele]=='不足之处':
        rate_bad.append(0)
    else:
        flag = True
        for pattern in bad_words:
            if re.match(pattern, ans[ele]):
                flag = False
        if flag:
            rate_bad.append(1)
        else:
            rate_bad.append(0)
print(rate_bad)
listings_df['好坏'] = rate_bad
print(listings_df)

# 重新建立list,用new_smallarea表示小区,好评数量为new_good_rate,总评价数量为new_rate_total
smallarea_temp = list(listings_df['小区'])
print(smallarea_temp)
rate_temp = list(listings_df['好坏'])
def remove_duplicates(input_list):
    new_list = []
    for ele in input_list:
        if ele not in new_list:
            new_list.append(ele)
    return new_list

new_smallarea = remove_duplicates(smallarea_temp)
print(new_smallarea)
new_good_rate = []
new_rate_total = []

for ele in range(len(new_smallarea)):
    sum = 0
    total = 0
    for n in range(len(smallarea_temp)):
        if smallarea_temp[n] == new_smallarea[ele]:
            total = total + 1
            sum = sum + rate_temp[n]
    new_good_rate.append(sum)
    new_rate_total.append(total)
print(new_good_rate)
print(new_rate_total)



# 联立另外的一个表，house_info
# 导入数据
data = pd.read_csv('D:/venvs/temp/Scripts/datades/house_info.csv')
# DataFrame化
listings_df_1 = pd.DataFrame(data)

streets = listings_df_1['街道']
mylist = []
for street in streets:
    s = str(street).split(" ")
    if(s[0]):
        if(1-operator.contains(s[0],'区')):
            s[0]+='区'
    else:
        s[0] += '其他区'
    mylist.append(s[0])
listings_df_1['区域'] = mylist
print(listings_df_1)

listings_p_1 = pd.DataFrame(listings_df_1,columns=['小区','区域'])
delete_areas = ['开发区', '其他区', '商住楼区', '三期区', '滨海区', '西区',  '南区',  '和平时光区',  '北区', '汉沽区', '二期区', '天成轩区','AC区', '东区', '一二期区', '蓟县区', '大港区', '塘沽区']
for del_area in delete_areas:
    listings_p_1 = listings_p_1.drop(listings_p_1[listings_p_1['区域']==del_area].index)
#去重
listings_p_1 = listings_p_1.drop_duplicates(subset=['小区'])
print(listings_p_1)

# 提取小区list和区域list
x = list(listings_p_1['小区'])
y = list(listings_p_1['区域'])
print(x)
print(y)
dic = list(set(y))
print(dic)
new_sum = []
new_total = []
for ele in range(len(dic)):
    new_sum.append(0)
    new_total.append(0)

for ele in range(len(new_smallarea)):
    if new_smallarea[ele] in x:
        i = x.index(new_smallarea[ele])
        # 获取对应的区的索引
        j = dic.index(y[i])
        new_sum[j] = new_sum[j] + new_good_rate[ele]
        new_total[j] = new_total[j] + new_rate_total[ele]
# 用new_sum存放好评率,最终dic存的是区域
for ele in range(len(new_sum)):
    if new_total[ele] == 0:
        new_sum[ele] = 0.0000
    else:
        new_sum[ele] = round(new_sum[ele]/new_total[ele],4)
print(new_sum)

data_pair = []
for ele in range(len(dic)):
    data_pair.append((dic[ele],float(new_sum[ele])))
print(data_pair)
#开始绘图
#数据分段
stages = [
        {'max': 0.7000, 'label': '0.7000以下', 'color': '#FFF0D6'},
        {'min': 0.7001, 'max': 0.7200, 'label': '0.7000-0.7200', 'color': '#FFD6D6'},
        {'min': 0.7201, 'max': 0.7400, 'label': '0.7200-0.7400', 'color': '#FF9B9B'},
        {'min': 0.7401, 'max': 0.7600, 'label': '0.7400-0.7600', 'color': '#FF6666'},
        {'min': 0.7601, 'max': 0.7800, 'label': '0.7600-0.7800', 'color': '#FF4040'},
        {'min': 0.7801, 'max': 0.8000, 'label': '0.7800-0.8000', 'color': '#FF0000'},
        {'min': 0.8000, 'label': '0.8000以上', 'color': '#8B0000'}
    ]

def hot_map(data):
    mapp = (
        Map(init_opts=opts.InitOpts(width='1200px', height='1200px'))
        .add("天津市各区域房源好评率热力图", data, "天津", itemstyle_opts=opts.ItemStyleOpts(color='red'))
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(visualmap_opts=opts.VisualMapOpts(is_piecewise=True,pieces=stages),
                         title_opts=opts.TitleOpts(title='天津市各区域房源好评率热力图'),
                         toolbox_opts=opts.ToolboxOpts(is_show=True))
    )
    return mapp
c = hot_map(data_pair)
c.render(path = '天津市各区域房源好评率热力图.html')
