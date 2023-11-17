import numpy as np
import pandas as pd

# 1. 读取数据集
df = pd.read_csv('../data/learn_pandas.csv', usecols = ['School', 'Grade', 'Name', 'Gender', 'Weight', 'Transfer'])
df['Name'].head()
df[['Gender', 'Name']].head() # 选取多列
df.Name.head() # 选取一列

#序列的行索引
s = pd.Series([1, 2, 3, 4, 5, 6], index=['a', 'b', 'a', 'a', 'a', 'c'])
s['a'] # 会返回多个值，为一个Series
s[['c', 'b']] # 会返回多个值，为一个Series
s['c': 'b': -2] # 取出c到b的值，步长为2，包含c和b
s['a': 'b'] #前后端点值重复出现，需经排序才能切片，报错
s.sort_index()['a': 'b']
#如果使用`[int]`或`[int_list]`，则可以取出对应索引**元素**的值
s = pd.Series(['a', 'b', 'c', 'd', 'e', 'f'], index=[1, 3, 1, 2, 5, 4])
s[1] 
s[[2,3]]
s[1:-1:2] #如果使用整数切片，则会取出对应索引**位置**的值，注意这里的整数切片同`Python`中的切片一样不包含右端点：

'''
`loc`索引器的一般形式是`loc[*, *]`，其中第一个`*`代表行的选择，第二个`*`代表列的选择，
如果省略第二个位置写作`loc[*]`，这个`*`是指行的筛选。其中，`*`的位置一共有五类合法对象，
分别是：单个元素、元素列表、元素切片、布尔列表以及函数
'''
df_demo = df.set_index('Name')
df_demo.loc['Qiang Sun'] 
df_demo.loc['Qiang Sun', 'School'] #同时选择行和列
df_demo.loc[['Qiang Sun','Quan Zhao'], ['School','Gender']] #同时选择多行和多列
df_demo.loc['Gaojuan You':'Gaoqiang Qian', 'School':'Gender'] #切片
df_demo.loc[df_demo.Weight>70].head() #布尔列表
df_demo.loc[df_demo.Grade.isin(['Freshman', 'Senior'])].head() #布尔列表
 # 与& 或| 非~ 
#索引为函数
def condition(x):
    return x.Weight > 70
df_demo.loc[condition].head() #函数
# lambda函数
df_demo.loc[lambda x:x.Weight>70].head() #lambda函数
# 函数返回切片需要用到`slice`对象
df_demo.loc[lambda x:slice('Zhang Yang', 'Xiaochen Sun')].head() #函数返回切片
df_chain = pd.DataFrame([[0,0],[1,0],[-1,0]], columns=list('AB'))
df_chain[df_chain.A!=0].B = 1 # 使用方括号列索引后，再使用点的列索引，会出现链式索引，报错
df_chain.loc[df_chain.A!=0,'B'] = 1 # 使用loc可以避免链式索引

# 3. iloc索引器
'''
`iloc`索引器与`loc`索引器一样，一般也是`iloc[*, *]`的形式，其中的`*`代表的是位置，
包含单个位置、位置列表、位置切片、位置布尔列表以及位置函数，与`loc`索引器不同的是，
这里的位置只能用整数或整数列表，而不能使用元素值或元素值列表。
'''
df_demo.iloc[0, 0] # 选择第一行第一列
df_demo.iloc[[0, 2], [0, 2]] # 同时选择多行多列
df_demo.iloc[0:2, 0:2] # 切片，不包含右端点
df_demo.iloc[(df_demo.Weight>70).values].head() # 布尔列表,values将Series转换为ndarray,否则会报错
df_demo.iloc[lambda x: slice(0, 2)].head() # 函数返回切片

# 4. query方法
'''
`query`方法的一般形式为`df.query(expr, inplace=False)`，其中`expr`是查询表达式，
字符串类型，`inplace`表示是否在原地进行赋值，默认为`False`。
'''
df.query('Weight > Weight.mean()').head()
# 对于含空格列名的处理，需要用到反引号，如：
df.query('School == "S_1"').head()
# query支持：or, and, not, in, not in, <, <=, >, >=, ==, !=, &, |, ~
# 引用外部变量
school_name = 'S_1'
df.query('School == @school_name').head()

# 5. 随机抽样
'''
`sample`方法的一般形式为`df.sample(n=None, frac=None, replace=False, weights=None, random_state=None, axis=None)`,
其中`n`是抽样的数量，`frac`是抽样占比（二者只能设置一个），`replace`表示是否放回，
`weights`是权重，`random_state`是随机种子，`axis`是抽取的维度，默认为行维度。
'''
df_sample = pd.DataFrame({'id': list('abcde'), 'value': [1, 2, 3, 4, 90]})
df_sample.sample(3, replace = True, weights = df_sample.value)

# 6. 多级索引
'''
多级索引的创建可以通过`set_index`方法来实现，它的`keys`参数表示需要设置为索引的列名，
`append`参数表示是否在原索引基础上添加索引，`drop`表示是否将`keys`列从数据中删除。
'''
np.random.seed(0)
multi_index = pd.MultiIndex.from_product([list('ABCD'), df.Gender.unique()], names=('School', 'Gender'))
multi_column = pd.MultiIndex.from_product([['Height', 'Weight'], df.Grade.unique()], names=('Indicator', 'Grade'))
df_multi = pd.DataFrame(np.c_[(np.random.randn(8,4)*5 + 163).tolist(), (np.random.randn(8,4)*5 + 65).tolist()],
                        index = multi_index, columns = multi_column).round(1)
df_multi.index.names # 查看索引名
df_multi.columns.names # 查看列名
df_multi.index.values # 查看索引值，返回一个元组组成的列表，每个元组对应一行，如('A', 'Female')
df_multi.columns.values # 查看列值，返回一个元组组成的列表，每个元组对应一列，如('Height', 'Freshman')
df_multi.index.get_level_values(0) # 查看某一层的索引值，返回一个列表，如['A', 'A', 'B', 'B', 'C', 'C', 'D', 'D']
df_multi = df.set_index(['School', 'Grade'])
# 当传入元组列表或单个元组或返回前二者的函数时，需要先进行索引排序以避免性能警告
df_sorted = df_multi.sort_index() # 排序后的多级索引
df_sorted.loc[('Fudan University', 'Junior')].head() # 一个Fudan匹配多个Junior，返回一个DataFrame
df_sorted.loc[df_sorted.Weight > 70].head() # 布尔列表也是可用的
df_sorted.loc[lambda x:('Fudan University','Junior')].head()
df_sorted.loc[('Fudan University', 'Senior'):].head() # 必须排序后才能使用切片
df_unique = df.drop_duplicates(subset=['School','Grade']).set_index(['School', 'Grade']) # 去重后设置索引
df_unique.sort_index().loc[('Fudan University', 'Senior'):].head() # 排序后的索引可以使用切片
#到所有北大和复旦的大二大三学生
res = df_multi.loc[(['Peking University', 'Fudan University'], ['Sophomore', 'Junior']), :] 
#选出北大的大三学生和复旦的大二学生
res = df_multi.loc[[('Peking University', 'Junior'), ('Fudan University', 'Sophomore')]]

# IndexSlice对象
'''
`IndexSlice`对象是在`pd`模块中定义的，可以使用`pd.IndexSlice`来获取。
`IndexSlice`对象可以接受三种形式的元组，分别是`:`、`单个元素`、`列表或数组`,
其中的`:`表示选取该维度的全部数据，单个元素表示选取对应的单个数据，列表或数组表示选取对应的多个数据。
'''
np.random.seed(0)
L1,L2 = ['A','B','C'],['a','b','c']
mul_index1 = pd.MultiIndex.from_product([L1,L2],names=('Upper', 'Lower'))
L3,L4 = ['D','E','F'],['d','e','f']
mul_index2 = pd.MultiIndex.from_product([L3,L4],names=('Big', 'Small'))
df_ex = pd.DataFrame(np.random.randint(-9,10,(9,9)), index=mul_index1, columns=mul_index2)
idx = pd.IndexSlice # 获取IndexSlice对象
df_ex.loc[idx['C':, ('D', 'f'):]] # 选取C到最后一行，Df到最后列的数据
df_ex.loc[idx[:'A', lambda x:x.sum()>0]] # 列和大于0
#行取A之前，b之后，列取E之后，e之后的数据,不支持函数
df_ex.loc[idx[:'A', 'b':], idx['E':, 'e':]] #前一个`idx`指代的是行索引，后一个是列索引。

# 7. 多级索引的构造
my_tuple = [('a','cat'),('a','dog'),('b','cat'),('b','dog')]
pd.MultiIndex.from_tuples(my_tuple, names=['First','Second'])# 从元组构建
my_array = [list('aabb'), ['cat', 'dog']*2]
pd.MultiIndex.from_arrays(my_array, names=['First','Second'])# 从数组构建
my_list1 = ['a','b']
my_list2 = ['cat','dog']
pd.MultiIndex.from_product([my_list1, my_list2], names=['First','Second'])# 从笛卡尔积构建

# 8. 索引的常用方式
np.random.seed(0)
L1,L2,L3 = ['A','B'],['a','b'],['alpha','beta']
mul_index1 = pd.MultiIndex.from_product([L1,L2,L3], names=('Upper', 'Lower','Extra'))
L4,L5,L6 = ['C','D'],['c','d'],['cat','dog']
mul_index2 = pd.MultiIndex.from_product([L4,L5,L6], names=('Big', 'Small', 'Other'))
df_ex = pd.DataFrame(np.random.randint(-9,10,(8,8)), index=mul_index1,  columns=mul_index2)
df_ex.swaplevel(0,2,axis=1).head() # 列索引的第一层和第三层交换，表头一三行
df_ex.reorder_levels([2,0,1],axis=0).head() # 列表数字指代原来索引中的层，原来1,2,3列的顺序
df_ex.droplevel(1,axis=1) # 删除第二层索引
df_ex.droplevel([0,1],axis=0) # 删除第一层和第二层索引
df_ex.rename_axis(index={'Upper':'Changed_row'}, columns={'Other':'Changed_Col'}).head()
df_ex.rename(columns={'cat':'not_cat'}, level=2).head() # 多级索引需指定level
df_ex.rename(index=lambda x:str.upper(x), level=2).head()
new_values = iter(list('abcdefgh'))
df_ex.rename(index=lambda x:next(new_values), level=2) # 用迭代器生成新的索引值
'''
若想要对某个位置的元素进行修改，在单层索引时容易实现，即先取出索引的`values`属性，
再给对得到的列表进行修改，最后再对`index`对象重新赋值。但是如果是多级索引的话就有些麻烦，
一个解决的方案是先把某一层索引临时转为表的元素，然后再进行修改，最后重新设定为索引，下面一节将介绍这些操作。
另外一个需要介绍的函数是`map`，它是定义在`Index`上的方法，与前面`rename`方法中层的函数式用法是类似的，
只不过它传入的不是层的标量值，而是直接传入索引的元组，这为用户进行跨层的修改提供了遍历。
例如，可以等价地写出上面的字符串转大写的操作：
'''
# 等价于df_ex.rename(index=lambda x:str.upper(x), level=2).head()
df_temp = df_ex.copy()
new_idx = df_temp.index.map(lambda x: (x[0], x[1], str.upper(x[2])))
df_temp.index = new_idx
# 多级索引压缩成单级索引，拼接
df_temp = df_ex.copy()
new_idx = df_temp.index.map(lambda x: (x[0]+'-'+x[1]+'-'+x[2]))
df_temp.index = new_idx
# 展开
new_idx = df_temp.index.map(lambda x:tuple(x.split('-')))
df_temp.index = new_idx

# 9. 索引的设置与重置
df_new = pd.DataFrame({'A':list('aacd'), 'B':list('PQRT'), 'C':[1,2,3,4]})
df_new.set_index('A') # 设置单索引
df_new.set_index('A', append=True) # 保留原索引0,1,2,3
df_new.set_index(['A', 'B'])
my_index = pd.Series(list('WXYZ'), name='D')
df_new = df_new.set_index(['A', my_index]) # 用Series设置索引
df_new.reset_index(['D']) # 重置索引
df_new.reset_index(['D'], drop=True) # 重置索引并删除列
df_new.reset_index() # 重置所有索引,会生成一个默认的整数索引

# 10. 索引的变形
df_reindex = pd.DataFrame({"Weight":[60,70,80], "Height":[176,180,179]}, index=['1001','1003','1002'])
df_reindex.reindex(index=['1001','1002','1003','1004'], columns=['Weight','Gender'])
'''
这种需求常出现在时间序列索引的时间点填充以及`ID`编号的扩充。
另外，需要注意的是原来表中的数据和新表中会根据索引自动对齐，
例如原先的1002号位置在1003号之后,而新表中相反,那么`reindex`中会根据元素对齐，与位置无关。
还有一个与`reindex`功能类似的函数是`reindex_like`，其功能是仿照传入的表索引来进行被调用
表索引的变形。例如，现在已经存在一张表具备了目标索引的条件，那么上述功能可采用下述代码得到：
'''
df_existed = pd.DataFrame(index=['1001','1002','1003','1004'], columns=['Weight','Gender'])
df_reindex.reindex_like(df_existed)

# 11. 索引的运算
df_set_1 = pd.DataFrame([[0,1],[1,2],[3,4]], index = pd.Index(['a','b','a'],name='id1'))
df_set_2 = pd.DataFrame([[4,5],[2,6],[7,1]], index = pd.Index(['b','b','c'],name='id2'))
id1, id2 = df_set_1.index.unique(), df_set_2.index.unique()
id1.intersection(id2) # 交集
id1.union(id2) # 并集
id1.difference(id2) # 差集，id1有id2没有
id1.symmetric_difference(id2) # 对称差，id1和id2中不同的元素
# 若两张表需要做集合运算的列并没有被设置索引，一种办法是先转成索引，运算后再恢复，
# 另一种方法是利用`isin`函数，例如在重置索引的第一张表中选出id列交集的所在行：
df_set_in_col_1 = df_set_1.reset_index()
df_set_in_col_2 = df_set_2.reset_index()
df_set_in_col_1[df_set_in_col_1.id1.isin(df_set_in_col_2.id2)]