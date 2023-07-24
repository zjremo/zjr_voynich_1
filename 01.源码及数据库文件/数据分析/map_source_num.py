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
myownlist = set(mylist)
print(myownlist)
listings_p = pd.DataFrame(listings_df,columns=['区域'])
delete_areas = ['开发区', '其他区', '商住楼区', '三期区', '滨海区', '西区',  '南区',  '和平时光区',  '北区', '汉沽区', '二期区', '天成轩区','AC区', '东区', '一二期区', '蓟县区', '大港区', '塘沽区']
for del_area in delete_areas:
    listings_p = listings_p.drop(listings_p[listings_p['区域']==del_area].index)
print(listings_p)

rent_sourcenum = listings_p['区域'].value_counts()
print(rent_sourcenum)

# 将series转为list
data_pair = []
area = rent_sourcenum.index.tolist()
rent_num = rent_sourcenum.values.tolist()
for ele in range(len(rent_sourcenum)):
    data_pair.append((area[ele],int(rent_num[ele])))
print(data_pair)

#开始绘图
def hot_map(data):
    print(data)
    mapp = (
        Map(init_opts=opts.InitOpts(width='1200px', height='1200px'))
        .add("天津市房源分布热力图", data, "天津", itemstyle_opts=opts.ItemStyleOpts(color='red'))
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(visualmap_opts=opts.VisualMapOpts(min_=0, max_=110, is_inverse=True,
                                                           range_color=['#FFD6D6', '#FF9B9B', '#FF6666', '#FF4040',
                                                                        '#FF0000'],
                                                           range_text=['High', 'Low']),
                         title_opts=opts.TitleOpts(title='天津市各区域房源分布图'),
                         toolbox_opts=opts.ToolboxOpts(is_show=True))
    )
    return mapp
c = hot_map(data_pair)
c.render(path = '天津市各区域房源分布图.html')



