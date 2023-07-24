from matplotlib import pyplot as plt
import pandas as pd
import operator

# 以roomtype为基准，统计租金分布
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
# 添加区域一栏
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


rent_money_house = round(listings_df.groupby(['户型'])['租金'].mean(),2)
width = 0.5
x_1 = rent_money_house.index.tolist()
y_1 = rent_money_house.values.tolist()
_x = list(range(len(x_1)))
plt.figure(figsize=(20,8),dpi=80)
plt.bar(_x,y_1,width=width)
for i, y in enumerate(y_1):
    plt.text(i, y + 100, str(y), ha='center', va='bottom')
plt.xticks(rotation=45)
plt.xticks(_x,x_1)
plt.xlabel('户型名')
plt.ylabel('租金均价/(元)')
plt.title('天津市各户型租金均价分布图')
plt.legend()
plt.savefig('天津市各户型租金均价分布图.png')