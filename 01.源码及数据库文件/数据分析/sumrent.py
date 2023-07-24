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
rentmoney = listings_df['租金']
d = 500
num_bins = (max(rentmoney)-min(rentmoney))//d
print('租金最大值: ',max(rentmoney))
print('租金最小值: ',min(rentmoney))
print('租金设置组别数: ',num_bins)
#设置图片大小
plt.figure(figsize=(20,8),dpi=80)
plt.hist(rentmoney,num_bins)
for rect in plt.gca().patches:
    height = rect.get_height()
    plt.gca().annotate(f'{height}', (rect.get_x() + rect.get_width() / 2, height), ha='center', va='bottom', rotation=45)
#刻度设置
plt.xticks(range(min(rentmoney),max(rentmoney)+d,d),rotation=90)
# x,y标签设置
plt.xlabel('租金/元')
plt.ylabel('频数/个')
plt.title('天津市租金分布图')
#画网格
plt.grid()
plt.savefig('天津市租金分布图.png')
plt.show()
