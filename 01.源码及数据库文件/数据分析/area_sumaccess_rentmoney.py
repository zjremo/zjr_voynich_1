import re
import csv
import pandas as pd
import matplotlib.pyplot as plt
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

# 为dataframe添加一列: 综合得分
# 轨道交通 高铁，(公交)站 公路 地铁 机场 高速    一项得分加10
# 小区设施 地上车位 地下车库 (公共活动)中心 花园 运动器材 小孩玩的东西 游乐场 广场 (商)业 一项得分加4
# 生活配套 超市 饭店 商业 广场 菜市场 (购物)中心  花园   地上车位 地下车库 一项得分加3
# 不足之处 出现一处减去三分 bad_words列表
# 附近学校 出现一栏加5分
get_score = []
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

traffic = ['.*高铁.*','.*公路.*','.*地铁.*','.*机场.*','.*高速.*','.*站.*']
facilities = ['.*地上车位.*','.*地下车库.*','.*中心.*','.*运动器材.*','.*小孩.*','.*游乐场.*','.*广场','.*业.*']
life = ['.*超市.*','.*饭店.*','.*商业.*','.*广场.*','.*菜市场.*','.*中心.*','.*花园.*','.*地上车位.*','.*地下车库.*']
school = ['小学','.*中.*','.*大学.*','.*幼儿园.*']
for ele in range(len(question)):
    score_temp = 0
    if question[ele]=='不足之处':
        temp = score_temp
        for n in bad_words:
            if re.match(n,ans[ele]):
                score_temp = score_temp - 9
        if temp == score_temp:
            score_temp = score_temp - 9
    if question[ele]=='轨道交通':
        for n in traffic:
            if re.match(n,ans[ele]):
                score_temp = score_temp + 15
    if question[ele]=='房屋品质':
        score_temp = score_temp + 10
    if question[ele]=='小区设施':
        for n in facilities:
            if re.match(n,ans[ele]):
                score_temp = score_temp + 4
    if question[ele]=='生活配套':
        for n in life:
            if re.match(n,ans[ele]):
                score_temp = score_temp + 3
    if question[ele]=='附近学校':
        for n in school:
            if re.match(n,ans[ele]):
                score_temp = score_temp + 15
    get_score.append(score_temp)
print(get_score)
listings_df['得分'] = get_score
print(listings_df)

# 重新建立list,用new_smallarea表示小区,好评数量为new_get_score
smallarea_temp = list(listings_df['小区'])
print(smallarea_temp)
score_get_temp = list(listings_df['得分'])
def remove_duplicates(input_list):
    new_list = []
    for ele in input_list:
        if ele not in new_list:
            new_list.append(ele)
    return new_list

new_smallarea = remove_duplicates(smallarea_temp)  #按顺序去掉重复的小区
print(new_smallarea)
new_get_score = []

for ele in range(len(new_smallarea)):
    sum = 0
    for n in range(len(smallarea_temp)):
        if smallarea_temp[n] == new_smallarea[ele]:
            sum = sum + score_get_temp[n]
    new_get_score.append(sum)
print(new_get_score)


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

listings_p_1 = pd.DataFrame(listings_df_1,columns=['小区','区域','租金'])
delete_areas = ['开发区', '其他区', '商住楼区', '三期区', '滨海区', '西区',  '南区',  '和平时光区',  '北区', '汉沽区', '二期区', '天成轩区','AC区', '东区', '一二期区', '蓟县区', '大港区', '塘沽区']
for del_area in delete_areas:
    listings_p_1 = listings_p_1.drop(listings_p_1[listings_p_1['区域']==del_area].index)
#去重
listings_p_1 = listings_p_1.drop_duplicates(subset=['小区'])
print(listings_p_1)

# 提取小区list和区域list
x = list(listings_p_1['小区'])
y = list(listings_p_1['区域'])
rent_money_av = round(listings_p_1.groupby(['区域'])['租金'].mean(),4)
print(rent_money_av)
_x = rent_money_av.index.tolist()
_y = rent_money_av.values.tolist()  #_x与x匹配

dic = ['河西区', '武清区', '蓟州区', '宁河区', '河北区', '静海区', '宝坻区', '北辰区', '南开区', '津南区', '滨海新区', '河东区', '东丽区', '西青区', '红桥区', '和平区']
# 和平区 320
#河西，河北，河东，红桥 南开 240
#北辰 东丽 西青 津南 160
# 武清 宝坻 宁河 滨海新区 静海 80
# 蓟州 0
addition_score = [240,80,0,80,240,80,80,160,240,160,80,240,160,160,240,320]
print(dic)
_y_last = []
for ele in range(len(dic)):
    if dic[ele] in _x:
        i = _x.index(dic[ele])
        _y_last.append(_y[i])

print(_y_last)  #构造出由dic，_y_last的租金体制

new_sum_score = []
for ele in range(len(dic)):
    new_sum_score.append(0)

for ele in range(len(new_smallarea)):
    if new_smallarea[ele] in x:
        i = x.index(new_smallarea[ele])
        # 获取对应的区的索引
        j = dic.index(y[i])
        new_sum_score[j] = new_sum_score[j] + new_get_score[ele]

for ele in range(len(new_sum_score)):
    new_sum_score[ele] = new_sum_score[ele] + addition_score[ele]
print(new_sum_score)

#dic ,new_sum_score , _y_last
list_1 = [dic,dic]
list_2 = [new_sum_score,_y_last]
label_get = ['综合得分','租金均价']
_x = [list(range(len(dic))),list(range(len(dic)))]
_x_begin = _x[0]
print(label_get)
point = 0
plt.figure(figsize=(20,20),dpi=80)
for x_1,y_1,_x_1,label_get in zip(list_1,list_2,_x,label_get):
    width = 0.2
    _x_1 = [i+point*width for i in _x_begin]
    plt.bar(_x_1,y_1,width=width,label=label_get)
    for i, y in enumerate(y_1):
        plt.text(i+point*width, y + 10, str(y), ha='center',rotation=45)
    point = point + 1
plt.xticks(_x_begin,list_1[0])
plt.xlabel('区域')
plt.ylabel('综合得分(分)/租金均价')
plt.title('天津市各区域住房舒适度综合得分与租金均价')
plt.legend()
plt.savefig('天津市各区域住房舒适度综合得分与租金均价.png')
# print(list_1)
# print(list_2)
