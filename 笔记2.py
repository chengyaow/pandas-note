import pandas as pd
s = pd.Series(data = [100, 'a', {'dic1':5}],
              index = pd.Index(['id1', 20, 'third'], name='my_idx'),
              dtype = 'object',
              name = 'my_name')
print(s)

pd.__version__ #查看版本
df_csv = pd.read_csv('../data/my_csv.csv')
df_txt = pd.read_table('../data/my_table.txt')
df_excel = pd.read_excel('../data/my_excel.xlsx')
pd.read_table('../data/my_table.txt', header=None) #不要第一行作为列名
pd.read_csv('../data/my_csv.csv', index_col=['col1', 'col2']) #将col1和col2两列作为索引
pd.read_table('../data/my_table.txt', usecols=['col1', 'col2']) #只读取col1和col2两列
pd.read_csv('../data/my_csv.csv', parse_dates=['col5']) #将col5列的数据转换为时间格式
pd.read_excel('../data/my_excel.xlsx', nrows=2) #只读取前两行
pd.read_table('../data/my_table_special_sep.txt', sep=' \|\|\|\| ', engine='python') #指定分隔符为多个|
df_csv.to_csv('../data/my_csv_saved.csv', index=False) #保存为csv文件，不保存索引
df_csv.to_excel('../data/my_excel_saved.xlsx', sheet_name='new_sheet') #保存为excel文件
df_txt.to_csv('../data/my_txt_saved.txt', sep='\t', index=False)
print(df_csv.to_markdown())
print(df_csv.to_latex())
s.values #查看数据
s.index #查看索引
s.dtype #查看数据类型
s.name #查看Series名称
s.shape #查看Series形状

data = [[1, 'a', 1.2], [2, 'b', 2.2], [3, 'c', 3.2]]
df = pd.DataFrame(data = data,
                  index = ['row_%d'%i for i in range(3)],
                  columns=['col_0', 'col_1', 'col_2'])

df = pd.DataFrame(data = {'col_0': [1,2,3],
                          'col_1':list('abc'),
                          'col_2': [1.2, 2.2, 3.2]},
                  index = ['row_%d'%i for i in range(3)])
'''
      col_0 col_1  col_2
row_0     1     a    1.2
row_1     2     b    2.2
row_2     3     c    3.2
'''

df['col_0']
df[['col_0', 'col_1']]
df.values
df.index
df.columns
df.dtypes # 返回的是值为相应列数据类型的Series
df.shape #(3,3)
df.T #转置后index不变

df = pd.read_csv('../data/learn_pandas.csv')
df = df[df.columns[:7]]
df.head(2) #不填数字默认为5
df.tail(3) #不填数字默认为5
df.info() #信息概况
df.describe() #数值列的描述性统计
df_demo = df[['Height', 'Weight']]
df_demo.mean()
df_demo.max()
df_demo.quantile(0.75) #四分位数
df_demo.count() #非缺失值元素个数
df_demo.idxmax() #最大值的索引
df_demo.mean(axis=1).head() # 在这个数据集上体重和身高的均值并没有意义,逐行计算
df['School'].unique() #查看唯一值
df['School'].drop_duplicates() #去重
df['School'].nunique() #查看唯一值个数
df['School'].value_counts() #查看唯一值及其出现次数

df_demo = df[['Gender','Transfer']]
df_demo.drop_duplicates(['Gender', 'Transfer']) #去重
df_demo.drop_duplicates(['Gender', 'Transfer'], keep='last') #保留最后一个
df_demo = df[['Gender','Transfer','Name']]
df['Gender'].replace({'Female':0, 'Male':1}).head() #替换
df['Gender'].replace(['Female', 'Male'], [0, 1]).head() #替换

s = pd.Series([-1, 1.2345, 100, -50])
s.where(s<0) #小于0的保留，大于0的变为缺失值
s.where(s<0, 1) #小于0的保留，大于0的变为1
s.mask(s<0) #小于0的变为缺失值，大于0的保留
s.mask(s<0, -1) #小于0的变为-1，大于0的保留
s_condition= pd.Series([True,False,False,True],index=s.index) #布尔索引序列
s.mask(s_condition, -50)
s.round(2) #保留两位小数
s.abs() #取绝对值
s.clip(0, 1) #将小于0的变为0，大于1的变为1

df_demo = df[['Grade', 'Name', 'Height', 'Weight']].set_index(['Grade','Name']) #设置索引
df_demo.sort_values('Height', ascending=False) #按身高降序排列
df_demo.sort_values(['Weight','Height'],ascending=[True,False])
df_demo.sort_index(level=['Grade','Name'],ascending=[True,False])

df_demo = df[['Height', 'Weight']]
def my_mean(x):
     res = x.mean()
     return res
df_demo.apply(my_mean) #逐列计算均值，apply默认逐列计算
df_demo.apply(lambda x:x.mean()) #逐列计算均值
df_demo.apply(lambda x:x.mean(), axis=1).head() #逐行计算均值
df_demo.apply(lambda x:(x-x.mean()).abs().mean())

s = pd.Series([1,2,3,4,5])
s.rolling(3) 
roller = s.rolling(window = 3) #创建一个Rolling对象，window表示窗口大小
roller.mean()
'''如果你设置window = 3,window可缺省,那么rolling函数会创建一个新的Series,
   其中的每个元素都是原Series中对应位置及其前两个元素(总共3个元素)的某种计算结果(如平均值、总和等)
0    NaN
1    NaN
2    2.0
3    3.0
4    4.0
dtype: float64
'''
s2 = pd.Series([1,2,6,16,30])
roller.cov(s2)
roller.corr(s2)
roller.apply(lambda x:x.mean())

s = pd.Series([1,3,6,10,15])
s.shift(2) #向下移动两个位置,原来的前两个位置变为缺失值
s.diff(3) #当前位置的值减去前三个位置的值,原来的前三个位置变为缺失值
s.pct_change() #当前位置的值减去前一个位置的值除以前一个位置的值,原来的第一个位置变为缺失值
s.shift(-1) #向上移动一个位置,原来的最后一个位置变为缺失值
s.diff(-2) #当前位置的值减去后两个位置的值,原来的最后两个位置变为缺失值
s.rolling(3).apply(lambda x:list(x)[0]) # s.shift(2)的另一种实现方式
#向后滑窗
s = s[::-1]
result = s.rolling(window=2).sum()[::-1]

s = pd.Series([1, 3, 6, 10])
s.expanding().mean() 
'''扩张窗口又称累计窗口，可以理解为一个动态长度的窗口，其窗口的大小就是从序列开始处到具体操作的对应位置，
其使用的聚合函数会作用于这些逐步扩张的窗口上。具体地说,设序列为a1, a2, a3, a4,
则其每个位置对应的窗口即\[a1\]、\[a1, a2\]、\[a1, a2, a3\]、\[a1, a2, a3, a4\]。
'''
