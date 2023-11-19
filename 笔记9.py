import numpy as np
import pandas as pd

df = pd.read_csv('../data/learn_pandas.csv', usecols = ['Grade', 'Name', 'Gender', 'Height', 'Weight'])
s = df.Grade.astype('category') #转换为分类类型
s.head()
s.cat.categories #Index(['Freshman', 'Junior', 'Senior', 'Sophomore'], dtype='object')
s.cat.ordered #False，分类是否有序
s.cat.codes.head() #分类的编码
s = s.cat.add_categories('Graduate') # 增加一个毕业生类别
s = s.cat.remove_categories('Freshman') # 删除一类别
s = s.cat.set_categories(['Sophomore','PhD']) # 新类别为大二学生和博士，Index(['Sophomore', 'PhD'], dtype='object')
s = s.cat.remove_unused_categories() # 移除了未出现的博士生类别
s = s.cat.rename_categories({'Sophomore':'本科二年级学生'}) # 重命名类别

#有序分类
'''有序类别和无序类别可以通过`as_unordered`和`reorder_categories`互相转化，需要注意的是后者传入的参数
必须是由当前序列的无序类别构成的列表，不能够增加新的类别，也不能缺少原来的类别，并且必须指定参数
`ordered=True`，否则方法无效。例如，对年级高低进行相对大小的类别划分，然后再恢复无序状态：'''
s = df.Grade.astype('category')
s = s.cat.reorder_categories(['Freshman', 'Sophomore', 'Junior', 'Senior'],ordered=True)
s.cat.as_unordered().head() #无序化
'''如果不想指定`ordered=True`参数，那么可以先用`s.cat.as_ordered()`转化为有序类别，再利用
`reorder_categories`进行具体的相对大小调整。'''
df.Grade = df.Grade.astype('category')
df.Grade = df.Grade.cat.reorder_categories(['Freshman', 'Sophomore', 'Junior', 'Senior'],ordered=True)
df.sort_values('Grade').head() # 按照年级大小排序
df.set_index('Grade').sort_index().head() # 按照年级索引排序

res1 = df.Grade == 'Sophomore'
res1.head() 
res2 = df.Grade == ['PhD']*df.shape[0] 
res3 = df.Grade <= 'Sophomore' #判断是否小于等于本科二年级学生
res4 = df.Grade <= df.Grade.sample(frac=1).reset_index(drop=True) #随机打乱后判断是否小于等于自身

#区间类别
s = pd.Series([1,2])
pd.cut(s, bins=2) # 区间为(0.999, 1.5]和(1.5, 2.0]，默认左开右闭
pd.cut(s, bins=2, right=False) # 区间为[1.0, 1.5)和[1.5, 2.001)]
pd.cut(s, bins=[-np.infty, 1.2, 1.8, 2.2, np.infty]) # 区间为(-inf, 1.2]、(1.2, 1.8]、(1.8, 2.2]、(2.2, inf]
s = pd.Series([1,2])
res = pd.cut(s, bins=2, labels=['small', 'big'], retbins=True) # labels参数指定区间名字，retbins参数返回区间边界
res[0] #res是一个元组，包含两个元素，res[0]是一个序列,放的区间的标签
res[1] #res[1]是一个数组，放的是区间的边界，array([0.999, 1.5  , 2.   ])
'''qcut和cut几乎没有差别,只是把bins参数变成的q参数,qcut中的q是指quantile。
这里的q为整数n时指按照n等分位数把数据分箱,还可以传入浮点列表指代相应的分位数分割点。'''
s = df.Weight
pd.qcut(s, q=3).head() # 按照三等分位数进行分箱,返回一个序列，序列的值是区间。
pd.qcut(s, q=[0,0.2,0.8,1]).head() # 按照指定的分位数进行分箱,返回一个序列

my_interval = pd.Interval(0, 1, 'right') #生成一个左开右闭的区间，mid, length, right, left, closed
0.5 in my_interval #True
my_interval_2 = pd.Interval(0.5, 1.5, 'left')
my_interval.overlaps(my_interval_2) #True，两个区间是否有重叠

#IntervalIndex([[1, 3], [3, 6], [6, 10]], dtype='interval[int64, both]')
pd.IntervalIndex.from_breaks([1,3,6,10], closed='both')
#IntervalIndex([(1, 5), (3, 4), (6, 9), (10, 11)], dtype='interval[int64, neither]')
pd.IntervalIndex.from_arrays(left = [1,3,6,10], right = [5,4,9,11], closed = 'neither')
pd.IntervalIndex.from_tuples([(1,5),(3,4),(6,9),(10,11)], closed='neither')
pd.interval_range(start=1,end=5,periods=8) # 8个等距区间，左开右闭
pd.interval_range(end=5,periods=8,freq=0.5) # 8个等距区间，左开右闭

my_interval #Interval(0, 1, closed='right')
my_interval_2 #Interval(0.5, 1.5, closed='left')
# IntervalIndex([[0.0, 1.0), [0.5, 1.5)], dtype='interval[float64, left]')
pd.IntervalIndex([my_interval, my_interval_2], closed='left') 

df = pd.DataFrame({'Weight': [60, 70, 80, 90, 100]})
s = df['Weight']
id_interval = pd.IntervalIndex(pd.cut(s, 3))
id_interval[:3] #IntervalIndex([(59.96, 73.333], (59.96, 73.333], (73.333, 86.667]], dtype='interval[float64, right]', name='Weight')
id_demo = id_interval[:5] # 选出前5个展示
id_demo.left # 左边界，Index([ 59.96 ,  59.96 ,  73.333,  73.333,  86.667])
id_demo.right # 右边界，Index([ 73.333,  73.333,  86.667,  86.667, 100.   ])
id_demo.mid # 中间值，Index([66.6465, 66.6465, 80.0, 93.3335, 93.3335], dtype='float64')
id_demo.length # 长度，Index([13.373, 13.373, 13.334, 13.334, 13.333], dtype='float64')
id_demo.contains(4) # 判断是否包含4，array([False, False, False, False, False])
id_demo.overlaps(pd.Interval(40,60)) # 判断是否与区间[40,60]有重叠，array([False, False, False, False, False])
