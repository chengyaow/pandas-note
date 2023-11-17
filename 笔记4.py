import numpy as np
import pandas as pd
df = pd.read_csv('../data/learn_pandas.csv')
df.groupby('Gender')['Height'].median() # 按性别分组，计算身高的中位数
df.groupby(['School', 'Gender'])['Height'].mean() # 按学校和性别分组，计算身高的均值
condition = df.Weight > df.Weight.mean()
df.groupby(condition)['Height'].mean()
# 计算体重的上下四分位数
q1 = df['Weight'].quantile(0.25)
q3 = df['Weight'].quantile(0.75)

# 根据四分位数将体重分为'high'、'normal'和'low'三组
conditions = [
    df['Weight'] <= q1,
    (df['Weight'] > q1) & (df['Weight'] < q3),
    df['Weight'] >= q3
]
choices = ['low', 'normal', 'high']
df['Weight_group'] = np.select(conditions, choices)

# 按照体重组别分组，计算身高的均值
result = df.groupby('Weight_group')['Height'].mean()

item = np.random.choice(list('abc'), df.shape[0]) #从a,b,c中随机选取df.shape[0]个元素
df.groupby(item)['Height'].mean()
df[['School', 'Gender']].drop_duplicates() # 去重
#传入列名只是一种简便的记号，事实上等价于传入的是一个或多个列，最后分组的依据来自于数据来源组合的unique值
df.groupby([df['School'], df['Gender']])['Height'].mean() 
gb = df.groupby(['School', 'Grade'])
gb.ngroups # 分组的数量
res = gb.groups
res.keys() # 字典的值由于是索引，元素个数过多，此处只展示字典的键
#使用group实现drop_duplicates的功能,fist()返回第一个值
df_grouped = df.groupby(['School', 'Gender']).first().reset_index()
gb.size() # 每个分组的元素个数
gb.get_group(('Fudan University', 'Freshman')) # 获取某个特定的分组
'''内置聚合函数包括:max/min/mean/median/count/all/any/idxmax/idxmin/
mad/nunique/skew/quantile/sum/std/var/sem/size/prod'''
gb = df.groupby('Gender')['Height']
gb.idxmin() # 最小值对应的索引
gb.quantile(0.95) # 计算分位数
# mad: 平均绝对偏差，公式为E(|X-E(X)|)
# skew: 偏度, 表示分布的不对称程度，公式为E[((X-u)/delta)^3]
# sem: 标准误差，表示均值估计的精确程度，公式为std/sqrt(n)
# prod: 乘积，所有元素的乘积

gb.agg(['sum', 'idxmax', 'skew']) # 一次性使用多个聚合函数
gb.agg({'Height':['mean', 'max'], 'Weight':'count'}) # 对不同的列使用不同的聚合函数
gb.agg(lambda x: x.mean()-x.min())
def my_func(s): # 自定义聚合函数，传入的参数是Series，返回值是标量，判断组的均值与整体均值的大小
    res = 'High'
    if s.mean() <= df[s.name].mean():
        res = 'Low'
    return res
gb.agg(my_func)
# 使用两个聚合函数，名字分别为range和my_sum
gb.agg([('range', lambda x: x.max()-x.min()), ('my_sum', 'sum')])
# 使用字典实现上述功能,Hight下有两个函数，一个是自定义的my_func，一个是sum
gb.agg({'Height': [('my_func', my_func), 'sum'], 'Weight': lambda x:x.max()}) 
gb.agg([('my_sum', 'sum')]) # 传入的是一个元组，元组的第一个元素是函数名，第二个元素是函数

#变换函数与transform方法
gb.cummax().head() # 累计最大值
#现对身高和体重进行分组标准化，即减去组均值后除以组的标准差
gb.transform(lambda x: (x-x.mean())/x.std()).head()  
'''transform方法的参数是一个函数,该函数只接受Series,返回值是DataFrame、Series'''
gb.transform('mean').head() # 传入返回标量的函数也是可以的
gb.filter(lambda x: x.shape[0] > 100).head() # 选择组大小超过100的组
'''返回的均值是标量而不是序列，因此`transform`不符合要求；似乎使用`agg`函数能够处理，
但是聚合函数是逐列处理的，而不能够多列数据同时处理。由此，引出了`apply`函数来解决这一问题。'''
def BMI(x):
    Height = x['Height']/100
    Weight = x['Weight']
    BMI_value = Weight/Height**2
    return BMI_value.mean()
gb.apply(BMI)
gb = df.groupby(['Gender','Test_Number'])[['Height','Weight']]
gb.apply(lambda x: 0) # 返回标量,与agg结果一致
gb.apply(lambda x: [0, 0]) # 虽然是列表，但是作为返回值仍然看作标量
# 得到的是`DataFrame`，行索引与标量情况一致，列索引为`Series`的索引
gb.apply(lambda x: pd.Series([0,0],index=['a','b'])) 
'''如果在apply传入的自定义函数中,根据组的某些特征返回相同长度但索引不同的Series,
那么Pandas会尝试对这些Series进行对齐,以便将它们合并到一个DataFrame中。如果无法对齐,
Pandas会抛出一个ValueError。'''
def custom_func(x):
    if x['Gender'].iloc[0] == 'Male':
        return pd.Series([0, 0], index=['a', 'b'])
    else:
        return pd.Series([0, 0], index=['c', 'd'])

try:
    gb.apply(custom_func)
except ValueError as e:
    print(f"Error: {e}")