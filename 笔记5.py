import numpy as np
import pandas as pd
pd.DataFrame({'Gender':['F','F','M','M'], 'Height':[163, 160, 175, 180]}) #性别的长表
pd.DataFrame({'Height: F':[163, 160], 'Height: M':[175, 180]}) #性别的宽表
df = pd.DataFrame({'Class':[1,1,2,2],
                   'Name':['San Zhang','San Zhang','Si Li','Si Li'],
                   'Subject':['Chinese','Math','Chinese','Math'],
                   'Grade':[80,75,90,85]})
# index: 新表的行索引，columns: 新表的列索引，values: 新表的值
# 利用`pivot`进行变形操作需要满足唯一性的要求，即由于在新表中的行列索引对应了唯一的`value`，
# 因此原表中的`index`和`columns`对应两个列的行组合必须唯一
df.pivot(index='Name', columns='Subject', values='Grade')
pivot_multi = df.pivot(index = ['Class', 'Name'],
                       columns = ['Subject','Examination'],
                       values = ['Grade','rank'])
# aggfunc: 聚合函数，如果出现多个值对应的情况，需要进行聚合操作,也可以ggfunc = lambda x:x.mean()
df.pivot_table(index = 'Name',
               columns = 'Subject',
               values = 'Grade',
               aggfunc = 'mean',
               margins=True) # margins: 是否进行边际汇总
df = pd.DataFrame({'Class':[1,2],
                   'Name':['San Zhang', 'Si Li'],
                   'Chinese':[80, 90],
                   'Math':[80, 75]})
# melt: 宽表变长表
# id_vars: 保持原来的列，将其他列变成行索引和值
df_melted = df.melt(id_vars = ['Class', 'Name'],
                    value_vars = ['Chinese', 'Math'],
                    var_name = 'Subject',
                    value_name = 'Grade')
# pivot: 长表变宽表
df_unmelted = df_melted.pivot(index = ['Class', 'Name'],
                              columns='Subject',
                              values='Grade')
# reset_index: 重置索引, rename_axis: 重命名索引
df_unmelted = df_unmelted.reset_index().rename_axis(columns={'Subject':''})
# equals: 判断两个表是否相等
df_unmelted.equals(df)
# wide_to_long: 宽表变长表, stubnames: 需要变成长表的列的前缀, i: 保持不变的列, j: 变成长表的列的后缀
# sep: 分隔符, suffix: 后缀
df = pd.DataFrame({'Class':[1,2],'Name':['San Zhang', 'Si Li'],
                   'Chinese_Mid':[80, 75], 'Math_Mid':[90, 85],
                   'Chinese_Final':[80, 75], 'Math_Final':[90, 85]})
pd.wide_to_long(df,
                stubnames=['Chinese', 'Math'],
                i = ['Class', 'Name'],
                j='Examination',
                sep='_',
                suffix='.+')
df = pd.DataFrame(np.ones((4,2)),
                  index = pd.Index([('A', 'cat', 'big'),
                                    ('A', 'dog', 'small'),
                                    ('B', 'cat', 'big'),
                                    ('B', 'dog', 'small')]),
                  columns=['col_1', 'col_2'])
df.unstack() # unstack: 将行索引变成列索引，默认转化最内层的行索引，big, small
df.unstack(2) # 将第二层的行索引变成列索引，big, small
df.unstack([0,2]) # 将第一层和第三层的行索引变成列索引，A, B, big, small
# 使用unstack需保证行索引的层级关系是唯一的，如果不唯一，需要先进行变形操作

df = pd.DataFrame(np.ones((4,2)),
                  index = pd.Index([('A', 'cat', 'big'),
                                    ('A', 'dog', 'small'),
                                    ('B', 'cat', 'big'),
                                    ('B', 'dog', 'small')]),
                  columns=['index_1', 'index_2']).T
df.stack() # stack: 将列索引变成行索引，默认转化最内层的列索引，big, small
df.stack([1, 2]) # 将第二层和第三层的列索引变成行索引，cat, dog, big, small
df = pd.read_csv('../data/learn_pandas.csv')
# crosstab可以看作是pivot_table的特殊情况，用于计算分组频率
pd.crosstab(index = df.School, columns = df.Transfer) 
# values: 用于聚合的列,此处无意义， aggfunc: 聚合函数
pd.crosstab(index = df.School, columns = df.Transfer, values = [0]*df.shape[0], aggfunc = 'count')
# 可以用pivot_table实现crosstab的功能
df.pivot_table(index = 'School',
               columns = 'Transfer',
               values = 'Name',
               aggfunc = 'count')
'''从上面可以看出这两个函数的区别在于，`crosstab`的对应位置传入的是具体的序列，
而`pivot_table`传入的是被调用表对应的名字，若传入序列对应的值则会报错。
除了默认状态下的`count`统计，所有的聚合字符串和返回标量的自定义函数都是可用的'''
'''`explode`参数能够对某一列的元素进行纵向的展开，被展开的单元格必须存储`list, tuple, Series, np.ndarray`中的一种类型。'''
df_ex = pd.DataFrame({'A': [[1, 2], 'my_str', {1, 2}, pd.Series([3, 4])],'B': 1})
df_ex.explode('A') # 对A列进行展开
'''`get_dummies`是用于特征构建的重要函数之一，其作用是把类别特征转为指示变量。
例如,对年级一列转为指示变量,属于某一个年级的对应列标记为1,否则为0:'''
pd.get_dummies(df.Grade).head()