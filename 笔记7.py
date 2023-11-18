import numpy as np
import pandas as pd
df = pd.read_csv('../data/learn_pandas.csv', usecols = ['Grade', 'Name', 'Gender', 'Height', 'Weight', 'Transfer'])
df.isna().head() # 查看每个单元格是否缺失
df.isna().sum() # 查看缺失的数量
df.isna().mean() # 查看缺失的比例
df[df.Height.isna()].head() # 查看身高缺失的行
sub_set = df[['Height', 'Weight', 'Transfer']]
df[sub_set.isna().all(1)] # 全部缺失 
df[sub_set.isna().any(axis=1)].head() # 至少有一个缺失
res = df.dropna(how = 'any', subset = ['Height', 'Weight']) # 丢弃身高或者体重缺失的行
res.shape # (174, 6)
# 删除超过15个缺失的列
res = df.dropna(thresh = df.shape[0]-15, axis = 1)
# 删除超过15个缺失的列
res = df.loc[df[['Height', 'Weight']].notna().all(1)]
res = df.loc[:, ~(df.isna().sum()>15)]
# 缺失值的填充与插值
# 1. 利用fillna方法填充,value可以是标量，也可以是索引到元素的字典映射,method参数有ffill和bfill两种
# limit参数限制填充的连续数量
s = pd.Series([np.nan, 1, np.nan, np.nan, 2, np.nan], list('aaabcd')) # nan, 1, nan, nan, 2, nan
s.fillna(method='ffill') # 用前面的值向后填充 nan, 1, 1, 1, 2, 2
s.fillna(method='ffill', limit=1) # 连续出现的缺失，最多填充一次 nan, 1, 1, nan, 2, 2
s.fillna(s.mean()) # value为标量 1.5 1.0 1.5 1.5 2.0 1.5
s.fillna({'a': 100, 'd': 200}) # 通过索引映射填充的值 100.0 1.0 100.0 nan 2.0 200.0
df.groupby('Grade')['Height'].transform(lambda x: x.fillna(x.mean())).head() # 按照年级进行分组，用身高的均值填充

# 2. interpolate方法进行线性插值，limit_direction参数有向前填充和向后填充两种,limit参数限制填充的连续数量
s = pd.Series([np.nan, np.nan, 1, np.nan, np.nan, np.nan, 2, np.nan, np.nan]) 
#array([nan, nan,  1., nan, nan, nan,  2., nan, nan])
res = s.interpolate(limit_direction='backward', limit=1) 
#array([ nan, 1.  , 1.  ,  nan,  nan, 1.75, 2.  ,  nan,  nan])
res = s.interpolate(limit_direction='both', limit=1)
#array([ nan, 1.  , 1.  , 1.25,  nan, 1.75, 2.  , 2.  ,  nan])
s.interpolate('nearest').values # 用最近的非缺失值填充
#array([nan, nan,  1.,  1.,  1.,  2.,  2.,  nan, nan])
s = pd.Series([0,np.nan,10],index=[0,1,10]) # 0.0 nan 10.0
s.interpolate() # 0.0 5.0 10.0
s.interpolate(method='index') # 和索引有关的线性插值，计算相应索引大小对应的值, 0.0 1.0 10.0
s = pd.Series([0,np.nan,10], index=pd.to_datetime(['20200101', '20200102', '20200111']))
s.interpolate() # 0.0 5.0 10.0
s.interpolate(method='index') # 0.0 1.0 10.0

# 3. nullable类型
# python中的缺失值是None，只等于自身,而在pandas中，对于整数类型而言，其缺失值是np.nan，这种缺失值是float类型的
s1 = pd.Series([1, np.nan])
s2 = pd.Series([1, 2])
s3 = pd.Series([1, np.nan])
s1 == 1 #返回布尔类型的Series，True和False
s1.equals(s2) # False
s1.equals(s3) # True
pd.to_timedelta(['30s', np.nan]) # Timedelta中的NaT
pd.to_datetime(['20200101', np.nan]) # Datetime中的NaT
pd.Series([1, np.nan]).dtype # float64
pd.Series([True, False, np.nan]).dtype # object而不是bool
pd.Series([np.nan, 1], dtype = 'Int64') # Int64类型的缺失值
pd.Series([np.nan, True], dtype = 'boolean') # boolean类型的缺失值
pd.Series([np.nan, 'my_str'], dtype = 'string') # string类型的缺失值

s = pd.Series(['a', 'b'])
s_bool = pd.Series([True, np.nan])
# 带有缺失的布尔列表无法进行索引器中的选择，而`boolean`会把缺失值看作`False`：
s_boolean = pd.Series([True, np.nan]).astype('boolean') 
# s[s_bool] # 报错
s[s_boolean] # 0    a
'''进行逻辑运算时，`bool`类型在缺失处返回的永远是`False`，而`boolean`会根据逻辑运算
是否能确定唯一结果来返回相应的值。那什么叫能否确定唯一结果呢？举个简单例子：
`True | pd.NA`中无论缺失值为什么值，必然返回`True`;`False | pd.NA`中的结果会根据缺
失值取值的不同而变化，此时返回`pd.NA`;`False & pd.NA`中无论缺失值为什么值，必然返回`False`。'''
s_boolean & True # 0    True, 1    <NA>
s_boolean | True # 0    True, 1    True
df = pd.read_csv('../data/learn_pandas.csv')
df = df.convert_dtypes() # 转换为nullable的类型

# 4. Nullable类型的算术运算
# 4.1 加法运算
s = pd.Series([2,3,np.nan,4,5])
s.sum() # 14.0, 会自动跳过缺失值
s.prod() # 120.0, 会自动跳过缺失值
s.cumsum() # 0     2.0, 1     5.0, 2     NaN, 3     9.0, 4    14.0
# 标量运算，除pd.NA ** 0 = 1，1 ** np.nan = 1外，其余全为缺失，pd.NA 也是，pd.NA + 1 = pd.NA,
s.diff() # 0    NaN, 1    1.0, 2    NaN, 3    NaN, 4    1.0
s.pct_change() # 0    NaN, 1    0.500000, 2    0.00000, 3    0.333333, 4    0.250000
df_nan = pd.DataFrame({'category':['a','a','b',np.nan,np.nan], 'value':[1,3,5,7,9]})
df_nan.groupby('category', dropna=False).mean() # 统计均值，包括缺失值
pd.get_dummies(df_nan.category, dummy_na=True) #返回三列，有一列为缺失值的列，值为True或False


