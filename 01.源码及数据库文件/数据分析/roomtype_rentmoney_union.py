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
# 添加区域一列
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
# 将重点关注的区域放入myownlist，这几个区域都是房源最多的几个区，并按照递减顺序排序
myownlist = ['南开区','北辰区','河西区','塘沽区','河北区','其他区']
# 将重点关注的户型放入list，这几个户型都是天津市占比最高的几个户型，并按照递减顺序排序
room_type_set = ['1室1厅1卫','2室1厅1卫','2室2厅1卫','3室2厅1卫']


# 各个区域不同户型租金均价
# 对dataFrame初次筛选，筛选出不同类型的
# 存放所有的dataframe
df_set = []
for room in room_type_set:
    tmp = listings_df[(listings_df['户型']==room)]
    tmp_copy = tmp.copy()
    for area in myownlist:
        if tmp_copy[tmp_copy['区域']==area].empty:
            tmp_copy.loc[len(tmp_copy)] = [0,' ',room,' ',' ',' ',' ',' ',' ',' ',0,' ',area]
            # tmp = tmp.append({'租金':0,'户型':room,'区域':area},ignore_index=True)
    df_set.append(tmp_copy)
# x的list存放，y的list存放，_x的list存放
x = []
y = []
_x = []
label_get = []
for df in df_set:
    room_type_get = list(df['户型'])
    label_get.append(room_type_get[0])
    df_rent_money_av = round(df.groupby(['区域'])['租金'].mean(),2).reindex(myownlist)

    print(df_rent_money_av)
    x_1 = df_rent_money_av.index.tolist()
    y_1 = df_rent_money_av.values.tolist()
    _x_1 = list(range(len(x_1)))
    x.append(x_1)
    y.append(y_1)
    _x.append(_x_1)

_x_begin = _x[0]
print(label_get)
point = 0
plt.figure(figsize=(20,20),dpi=80)
for x_1,y_1,_x_1,label_get in zip(x,y,_x,label_get):
    width = 0.2
    _x_1 = [i+point*width for i in _x_begin]
    plt.bar(_x_1,y_1,width=width,label=label_get)
    for i, y in enumerate(y_1):
        plt.text(i+point*width, y + 10, str(y), ha='center',rotation=45)
    point = point + 1
plt.xticks(_x_begin,x[0])
plt.xlabel('区域')
plt.ylabel('租金均价')
plt.title('天津市代表区域代表性户型租金均价')
plt.legend()
plt.savefig('天津市代表区域代表性户型租金均价.png')

# 各个区域不同户型数量占比
# 先得出所有的区域的房源总数量
neighbourhood_count = listings_df['区域'].value_counts().reindex(myownlist)
df_set = []
for room in room_type_set:
    tmp = listings_df[(listings_df['户型']==room)]
    df_set.append(tmp)
x = []
y = []
_x = []
label_get = []
for df in df_set:
    room_type_get = list(df['户型'])
    label_get.append(room_type_get[0])
    df_rent_count = df['区域'].value_counts()
    for ele in myownlist:
        if ele not in df_rent_count:
            df_rent_count[ele] = 0
    df_rent_count_sorted = df_rent_count.reindex(myownlist)
    for ele in myownlist:
        df_rent_count_sorted[ele] = round(df_rent_count_sorted[ele]/neighbourhood_count[ele],4)

    x_1 = df_rent_count_sorted.index.tolist()
    y_1 = df_rent_count_sorted.values.tolist()
    _x_1 = list(range(len(x_1)))
    x.append(x_1)
    y.append(y_1)
    _x.append(_x_1)

_x_begin = _x[0]
# print(label_get)
point = 0
plt.figure(figsize=(20,20),dpi=80)
for x_1,y_1,_x_1,label_get in zip(x,y,_x,label_get):
    width = 0.2
    _x_1 = [i+point*width for i in _x_begin]
    plt.bar(_x_1,y_1,width=width,label=label_get)
    for i, y in enumerate(y_1):
        plt.text(i+point*width, y + 0.01, str(y), ha='center',rotation=45)
    point = point + 1
plt.xticks(_x_begin,x[0])
plt.xlabel('区域')
plt.ylabel('房源占比')
plt.title('天津市代表区域代表性户型房源占比')
plt.legend()
plt.savefig('天津市代表区域代表性户型房源占比.png')