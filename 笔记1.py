list(map(lambda x: print(x), range(1, 4)))
pairs = [(1, 'a'), (2, 'b'), (3, 'c'), (4, 'd')]
numbers, letters = zip(*pairs)
print(numbers, letters)
import numpy as np

np.linspace(1,5,11) # 起始、终止（包含）、样本个数
np.arange(1,5,2) # 起始、终止（不包含）、步长
np.full((2,3), 10) # 元组传入大小，10表示填充数值
np.zeros((2,3)) # 生成全0数组
np.ones((2,3)) # 生成全1数组
np.full((2,3), [1,2,3]) # 每行填入相同的列表
np.random.uniform(5, 15, 3) # 生成3个5到15的随机数,均匀分布
np.random.randn(2, 2) # 生成2*2的标准正态分布随机数


# 生成一个3*3的单位矩阵，偏移量为-1
np.eye(3,k=-1)
print(np.eye(3,k=-1))

#标准正态分布
np.random.randn(3,3)

#方差为2，均值为1的正态分布
np.random.normal(1,2,(3,3))

# 生成5到14的随机整数
low, high, size = 5, 15, (2,2) 
np.random.randint(low, high, size)

# 生成一个随机序列，从['a', 'b', 'c', 'd']中随机抽取2个数，不放回
my_list = ['a', 'b', 'c', 'd']
np.random.choice(my_list, 2, replace=False, p=[0.1, 0.7, 0.1 ,0.1])
np.random.choice(my_list, (3,3))

#打散my_list
np.random.shuffle(my_list)
np.random.permutation(my_list)

#设置随机种子,使得每次生成的随机数相同
np.random.seed(0)
print(np.random.rand())
np.random.seed(None)

np.zeros((2,3)).T # 转置
np.r_[np.zeros((2,3)),np.zeros((2,3))] # 按行合并
np.c_[np.zeros((2,3)),np.zeros((2,3))] # 按列合并
np.hsplit(np.zeros((2,6)),3) # 按列分割
np.vsplit(np.zeros((4,6)),2) # 按行分割

#注意，一维数组视为列向量
np.r_[np.array([0,0]),np.zeros(2)]
# array([0., 0., 0., 0.])

np.c_[np.array([0,0]),np.zeros((2,3))]
# array([[0., 0., 0., 0.],
#        [0., 0., 0., 0.]])

target = np.arange(8).reshape(2,4)
target.reshape((4,2), order='C') # 按照行读取和填充
target.reshape((4,2), order='F') # 按照列读取和填充
target.reshape((4,-1)) # -1表示自动计算行数或列数
target.flatten() # 展平为一维数组，按照行读取
target.flatten(order='F') # 按照列读取
target = np.ones((3,1))
target.reshape(-1) # 一维数组

target = np.arange(9).reshape(3,3)
target[:-1, [0,2]] # 前两行，第一列和第三列
target[np.ix_([1,2], [True, False, True])] # 第二行和第三行，第一列和第三列

a = np.array([-1,1,-1,0])
np.where(a>0, a, 5) # 对应位置为True时填充a对应元素，否则填充5
a.nonzero() # 返回非零元素的索引
a.argmax() # 返回最大值的索引
a.argmin() # 返回最小值的索引
a.argsort() # 返回排序后的索引
a.clip(0,1) # 小于0的数变为0，大于1的数变为1
a.any() # 有一个为True则返回True
a.all() # 全为True则返回True
a.cumsum() # 累加 [1,2,3] -> [1,3,6]
a.cumprod() # 累乘 [1,2,3] -> [1,2,6]
np.diff(a) # 一阶差分 [1,2,5] -> [1,3]
a.mean() # 均值
a.std() # 标准差
a.var() # 方差
a.max() # 最大值
a.min() # 最小值
np.median(a) # 中位数
np.percentile(a, 25) # 25%分位数
np.quantile(a, 0.25) # 25%分位数
a.sum() # 求和
a.prod() # 求积
a =np.array([1,2,np.nan]) # nan表示缺失值
np.isnan(a) # 判断是否为缺失值
np.nanmax(a) # 忽略缺失值后的最大值
np.nanquantile(target, 0.5) # 忽略缺失值后的中位数

target1 = np.array([1,3,5,9])
target2 = np.array([1,5,3,-9])
np.cov(target1, target2) # 协方差矩阵
np.corrcoef(target1, target2) # 相关系数矩阵

target = np.arange(1,10).reshape(3,-1)
'''
array([[1, 2, 3],
       [4, 5, 6],
       [7, 8, 9]])
'''
target.sum(0) # 按列求和, [12, 15, 18]
target.sum(1) # 按行求和, [6, 15, 24]

a = np.array([1,2,3])
b = np.array([1,3,5])
a.dot(b) # 点积

matrix_target =  np.arange(4).reshape(-1,2)
'''
array([[0, 1],
       [2, 3]])
'''
np.linalg.norm(matrix_target, 'fro') # Frobenius范数，所有元素平方和的平方根
np.linalg.norm(matrix_target, np.inf) # L1范数，所有元素绝对值的最大值
np.linalg.norm(matrix_target, 1) # L1范数，max(sum(abs(x), axis=0))
np.linalg.norm(matrix_target, 2) # L2范数，所有元素绝对值的平方和的平方根

vector_target =  np.arange(4) # array([0, 1, 2, 3])
np.linalg.norm(vector_target, np.inf) # max(abs(x))
np.linalg.norm(vector_target, 1) # sum(abs(x))
np.linalg.norm(vector_target, 2) # sqrt(sum(x**2))
np.linalg.norm(vector_target, 3) # sum(abs(x)**3)**(1./3)

#矩阵乘法
a = np.arange(4).reshape(2,2)
b = np.arange(4).reshape(2,2)
a@b

res = np.ones((3,2))
'''
array([[1., 1.],
       [1., 1.],
       [1., 1.]])
'''
print(np.array([[2],[3],[4]]) * res == res * np.array([[2],[3],[4]]) )