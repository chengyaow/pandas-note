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