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

# 1. 小区评论热度
rate_count = listings_df.groupby(['小区']).count()
# print(rate_count)
smallarea = rate_count.index.tolist()
print(smallarea)
num_temp = rate_count.values.tolist()
num = []
for ele in num_temp:
    num.append(ele[0])
print(num)


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
# print(listings_df_1)

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
area = []
new_smallarea = []
new_num = []
for ele in range(len(smallarea)):
    if smallarea[ele] in x:
        i = x.index(smallarea[ele])
        new_smallarea.append(smallarea[ele])
        new_num.append(num[ele])
        area.append(y[i])

myownlist = set(y)
myownlist = list(myownlist)
print(myownlist)
myownlist_num = []
for ele in myownlist:
    temp = 0
    for n in range(len(area)):
        if area[n] == ele:
            temp = temp + new_num[n]
    myownlist_num.append(temp)
print(myownlist_num)

data_pair = []
for ele in range(len(myownlist)):
    data_pair.append((myownlist[ele],int(myownlist_num[ele])))
print(data_pair)
#开始绘图
def hot_map(data):
    print(data)
    mapp = (
        Map(init_opts=opts.InitOpts(width='1200px', height='1200px'))
        .add("天津市各区域房源评价热度热力图", data, "天津", itemstyle_opts=opts.ItemStyleOpts(color='red'))
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(visualmap_opts=opts.VisualMapOpts(min_=0, max_=250, is_inverse=True,
                                                           range_color=['#FFD6D6', '#FF9B9B', '#FF6666', '#FF4040',
                                                                        '#FF0000'],
                                                           range_text=['High', 'Low']),
                         title_opts=opts.TitleOpts(title='天津市各区域房源评价热度热力图'),
                         toolbox_opts=opts.ToolboxOpts(is_show=True))
    )
    return mapp
c = hot_map(data_pair)
c.render(path = '天津市各区域房源评价热度热力图.html')
