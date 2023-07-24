from matplotlib import pyplot as plt
import pandas as pd
import operator
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

# 统计每个地区有多少房源信息
neighbourhood_count = listings_df['区域'].value_counts()
# 总体上:
# 户型总数分布:
room_type_count = listings_df['户型'].value_counts()
# 房屋朝向的分布:
arc_count = listings_df['朝向'].value_counts()
# 装修的分布：
renovation_count = listings_df['装修'].value_counts()
print(neighbourhood_count)
print(room_type_count)
print(arc_count)
print(renovation_count)


# 绘制房源分布区域占比图(饼)
# neighbourhood_label = neighbourhood_count.index
# neighbourhood_max = neighbourhood_count.idxmax()
# explode = {}
# for i in neighbourhood_label:
#     if i in neighbourhood_max:
#         explode[i] = 0.1
#     else:
#         explode[i] = 0
#
#
# plt.figure(figsize=(8,10),dpi=80)
# plt.pie(neighbourhood_count,explode=explode.values(),labels=neighbourhood_label,autopct='%.2f%%',startangle=90,counterclock=False,colors=sns.color_palette('hls',n_colors=16))
# plt.title('房源分布区域占比图')
# plt.savefig('房源分布区域占比图.png')
#plt.show()

# 绘制房源分布区域占比图(条形)
neighbourhood_label = neighbourhood_count.index.tolist()
neighbourhood_value = neighbourhood_count.values.tolist()
total = 0
for ele in range(0,len(neighbourhood_value)):
    total = total + neighbourhood_value[ele]
for ele in range(0,len(neighbourhood_value)):
    neighbourhood_value[ele] = round(neighbourhood_value[ele]/total,4)
_neighbourhood_label = list(range(len(neighbourhood_label)))
plt.figure(figsize=(20,8),dpi=80)
width = 0.2
plt.bar(_neighbourhood_label,neighbourhood_value,width=width)
for i, y in enumerate(neighbourhood_value):
    plt.text(i, y + 0.001, str(y), ha='center', va='bottom',rotation=45)
plt.xticks(rotation=90)
plt.xticks(_neighbourhood_label,neighbourhood_label)
plt.xlabel('区域名')
plt.ylabel('房源数量占比')
plt.title('房源分布区域占比图')
plt.legend()
plt.savefig('房源分布区域占比图.png')

#绘制户型分布区域占比图(饼图)
# room_type_label = room_type_count.index
# room_type_max = room_type_count.idxmax()
# explode = {}
# for i in room_type_label:
#     if i in room_type_max:
#         explode[i] = 0.1
#     else:
#         explode[i] = 0
# plt.figure(figsize=(8,10),dpi=80)
# plt.pie(room_type_count,explode=explode.values(),labels=room_type_label,autopct='%.2f%%',startangle=90,counterclock=False,colors=sns.color_palette('hls',n_colors=16))
# plt.title('天津市户型占比图')
# plt.savefig('天津市户型占比图.png')
# plt.show()

# 绘制户型分布区域占比图(条形图)
room_type_label = room_type_count.index.tolist()
room_type_value = room_type_count.values.tolist()
total = 0
for ele in range(0,len(room_type_value)):
    total = total + room_type_value[ele]
for ele in range(0,len(room_type_value)):
    room_type_value[ele] = round(room_type_value[ele]/total,4)
_room_type_label = list(range(len(room_type_label)))
plt.figure(figsize=(20,8),dpi=80)
width = 0.2
plt.bar(_room_type_label,room_type_value,width=width)
for i, y in enumerate(room_type_value):
    plt.text(i, y + 0.001, str(y), ha='center', va='bottom')
plt.xticks(rotation=45)
plt.xticks(_room_type_label,room_type_label)
plt.xlabel('户型名')
plt.ylabel('户型数量占比')
plt.title('天津市户型占比图')
plt.legend()
plt.savefig('天津市户型占比图.png')

# 绘制房屋朝向分布区域占比图(饼图)
# arc_count_label = arc_count.index
# arc_count_max = arc_count.idxmax()
# explode = {}
# for i in arc_count_label:
#     if i in arc_count_max:
#         explode[i] = 0.1
#     else:
#         explode[i] = 0
# plt.figure(figsize=(8,10),dpi=80)
# plt.pie(arc_count,explode=explode.values(),labels=arc_count_label,autopct='%.2f%%',startangle=90,counterclock=False,colors=sns.color_palette('hls',n_colors=16))
# plt.title('天津市房屋朝向占比图')
# plt.savefig('天津市房屋朝向占比图.png')
# plt.show()

# 绘制房屋朝向分布区域占比图(条形图)
arc_count_label = arc_count.index.tolist()
arc_count_value = arc_count.values.tolist()
total = 0
for ele in range(0,len(arc_count_value)):
    total = total + arc_count_value[ele]
for ele in range(0,len(arc_count_value)):
    arc_count_value[ele] = round(arc_count_value[ele]/total,4)
_arc_count_label = list(range(len(arc_count_label)))
plt.figure(figsize=(20,8),dpi=80)
width = 0.2
plt.bar(_arc_count_label,arc_count_value,width=width)
for i, y in enumerate(arc_count_value):
    plt.text(i, y + 0.001, str(y), ha='center', va='bottom')
plt.xticks(rotation=90)
plt.xticks(_arc_count_label,arc_count_label)
plt.xlabel('房屋朝向')
plt.ylabel('房屋朝向占比')
plt.title('天津市房屋朝向占比图')
plt.legend()
plt.savefig('天津市房屋朝向占比图.png')

# 绘制装修分布区域图(饼图)
# renovation_label = renovation_count.index
# renovation_count_max = renovation_count.idxmax()
# explode = {}
# for i in renovation_label:
#     if i in renovation_count_max:
#         explode[i] = 0.1
#     else:
#         explode[i] = 0
# plt.figure(figsize=(8,10),dpi=80)
# plt.pie(renovation_count,explode=explode.values(),labels=renovation_label,autopct='%.2f%%',startangle=90,counterclock=False,colors=sns.color_palette('hls',n_colors=16))
# plt.title('天津市装修类型占比图')
# plt.savefig('天津市装修类型占比图.png')
# plt.show()

# 绘制装修分布区域图(条形图)
renovation_count_label = renovation_count.index.tolist()
renovation_count_label[len(renovation_count_label)-1]='其他'
renovation_count_value = renovation_count.values.tolist()
total = 0
for ele in range(0,len(renovation_count_value)):
    total = total + renovation_count_value[ele]
for ele in range(0,len(renovation_count_value)):
    renovation_count_value[ele] = round(renovation_count_value[ele]/total,4)
_renovation_count_label = list(range(len(renovation_count_label)))
plt.figure(figsize=(20,8),dpi=80)
width = 0.2
plt.bar(_renovation_count_label,renovation_count_value,width=width)
for i, y in enumerate(renovation_count_value):
    plt.text(i, y + 0.001, str(y), ha='center', va='bottom')
plt.xticks(rotation=90)
plt.xticks(_renovation_count_label,renovation_count_label)
plt.xlabel('装修类型')
plt.ylabel('装修类型占比')
plt.title('天津市装修类型占比图')
plt.legend()
plt.savefig('天津市装修类型占比图.png')
# 天津市各个区域的租金均价整理，并进行统计分析
# 按标签索引整理不同区域的租金均值
rent_money_av = round(listings_df.groupby(['区域'])['租金'].mean(),2)
width = 0.5
x_1 = rent_money_av.index.tolist()
y_1 = rent_money_av.values.tolist()
_x = list(range(len(x_1)))
plt.figure(figsize=(20,8),dpi=80)
plt.bar(_x,y_1,width=width)
for i, y in enumerate(y_1):
    plt.text(i, y + 100, str(y), ha='center', va='bottom',rotation=75)
plt.xticks(rotation=90)
plt.xticks(_x,x_1)
plt.xlabel('区域名')
plt.ylabel('租金均价/(元)')
plt.title('天津市各区域租金均价分布图')
plt.legend()
plt.savefig('天津市各区域租金均价分布图.png')




