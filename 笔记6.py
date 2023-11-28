import numpy as np
import pandas as pd
'''左连接即以左表的键为准，如果右表中的键于左表存在，那么就添加到左表，否则则处理为缺失值，
右连接类似处理。内连接只负责合并两边同时出现的键，而外连接则会在内连接的基础上包含只在左边出
现以及只在右边出现的值，因此外连接又叫全连接。'''
df1 = pd.DataFrame({'Name':['San Zhang','Si Li'], 'Age':[20,30]})
df2 = pd.DataFrame({'Name':['Si Li','Wu Wang'], 'Gender':['F','M']})
df1.merge(df2, on='Name', how='left') # 左连接,不会出现Wu Wang
df1 = pd.DataFrame({'df1_name':['San Zhang','Si Li'], 'Age':[20,30]})
df2 = pd.DataFrame({'df2_name':['Si Li','Wu Wang'], 'Gender':['F','M']})
df1.merge(df2, left_on='df1_name', right_on='df2_name', how='left') # 指定列名
df1 = pd.DataFrame({'Name':['San Zhang'],'Grade':[70]})
df2 = pd.DataFrame({'Name':['San Zhang'],'Grade':[80]})
df1.merge(df2, on='Name', how='left', suffixes=['_Chinese','_Math']) # 指定列名后缀
df1 = pd.DataFrame({'Name':['San Zhang', 'San Zhang'],
                    'Age':[20, 21],
                    'Class':['one', 'two']})
df2 = pd.DataFrame({'Name':['San Zhang', 'San Zhang'],
                    'Gender':['F', 'M'],
                    'Class':['two', 'one']})
df1.merge(df2, on=['Name', 'Class'], how='left') # 多列连接，只连接则Name错了

from datetime import timedelta
nowcoder = pd.read_csv('nowcoder.csv')
df = pd.merge(nowcoder,nowcoder,on='user_id',suffixes=['_a','_b'])
df.date_a = pd.to_datetime(df.date_a).dt.date
df.date_b = pd.to_datetime(df.date_b).dt.date
df = df[(df.date_a+timedelta(days=1))==df.date_b]
all_num = nowcoder.user_id.count()
again_num = df.user_id.count()
print(round(again_num/all_num,2))

#索引连接
df1 = pd.DataFrame({'Grade':[70]}, index=pd.Series(['San Zhang'], name='Name'))
df2 = pd.DataFrame({'Grade':[80]}, index=pd.Series(['San Zhang'], name='Name'))
df1.join(df2, how='left', lsuffix='_Chinese', rsuffix='_Math') # 指定列名后缀
df1 = pd.DataFrame({'Age':[20,21]}, index=pd.MultiIndex.from_arrays([['San Zhang', 'San Zhang'],['one', 'two']], names=('Name','Class')))
df2 = pd.DataFrame({'Gender':['F', 'M']}, index=pd.MultiIndex.from_arrays([['San Zhang', 'San Zhang'],['two', 'one']], names=('Name','Class')))
df1.join(df2) # 多列连接

#方向连接
df1 = pd.DataFrame({'Name':['San Zhang','Si Li'], 'Age':[20,30]})
df2 = pd.DataFrame({'Name':['Wu Wang'], 'Age':[40]})
pd.concat([df1, df2])
df2 = pd.DataFrame({'Grade':[80, 90]})
df3 = pd.DataFrame({'Gender':['M', 'F']})
pd.concat([df1, df2,df3],axis=1) # 列方向连接，axis=0为行方向连接,即纵向连接，默认为0
# contact 的 join 参数默认为 outer，即保留所有行和列，如果想要保留公共部分，可以设置为 inner
pd.concat([df1, df2], join='inner')
df2 = pd.DataFrame({'Grade':[80, 90]}, index=[1, 2]) #给第2,3人加上成绩
pd.concat([df1, df2], axis=1)
'''当确认要使用多表直接的方向合并时，尤其是横向的合并，可以先用`reset_index`方法恢复默认整数索引再进行合并，
防止出现由索引的误对齐和重复索引的笛卡尔积带来的错误结果。`keys`参数的使用场景在于多个表合并后，
用户仍然想要知道新表中的数据来自于哪个原表，这时可以通过`keys`参数产生多级索引进行标记。'''
pd.concat([df1, df2], keys=['one', 'two'])
s = pd.Series(['Wu Wang', 21], index = df1.columns)
df1._append(s, ignore_index=True) # ignore_index=True表示忽略原来的索引,自动添加索引
s = pd.Series([80, 90])
df1.assign(Grade=s) #返回新表，不改变原表
df1['Grade'] = s #在原表上修改
df1.compare(df2) # 比较两个表的差异，返回一个新表，如果相同则为NaN，完整显示用keep_shape=True

def choose_min(s1, s2):
    s2 = s2.reindex_like(s1) # 用s1的索引对s2进行重排，没有的用NaN填充
    res = s1.where(s1<s2, s2) # where表示如果s1<s2则保留s1，否则保留s2
    res = res.mask(s1.isna()) # isna表示是否为缺失值，返回布尔序列
    return res
df1 = pd.DataFrame({'A':[1,2], 'B':[3,4], 'C':[5,6]})
df2 = pd.DataFrame({'B':[5,6], 'C':[7,8], 'D':[9,10]}, index=[1,2])
df1.combine(df2, choose_min) # 用自定义函数进行合并
df1.combine(df2, choose_min, overwrite=False) # 保留被调用表未被调用的部分，即df1中的A列

df1 = pd.DataFrame({'A':[1,2], 'B':[3,np.nan]})
df2 = pd.DataFrame({'A':[5,6], 'B':[7,8]}, index=[1,2])
df1.combine_first(df2) # 用df2填充df1中的缺失值
