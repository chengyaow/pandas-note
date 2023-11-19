import numpy as np
import pandas as pd
''' 
概念            单元素类型      数组类型            pandas数据类型
Date times      Timestamp      DatetimeIndex       datetime64[ns]
Time deltas     Timedelta      TimedeltaIndex      timedelta64[ns]
Time spans      Period         PeriodIndex         period[freq]
Date offsets    DateOffset     None                None
'''
ts = pd.Timestamp('2020/1/1') # 时间戳,Timestamp('2020-01-01 00:00:00')
ts = pd.Timestamp('2020-1-1 08:10:30')
ts.year # 2020
ts.month # 1
ts.day # 1
ts.hour # 8
ts.minute # 10
ts.second # 30
pd.Timestamp.max # Timestamp('2262-04-11 23:47:16.854775807') 585年
pd.Timestamp.min # Timestamp('1677-09-21 00:12:43.145224193')
pd.to_datetime(['2020-1-1', '2020-1-3', '2020-1-6'])
df = pd.read_csv('../data/learn_pandas.csv')
s = pd.to_datetime(df.Test_Date) # 转换为时间戳
s.head()
temp = pd.to_datetime(['2020\\1\\1','2020\\1\\3'],format='%Y\\%m\\%d') # 使用format指定格式
#注意上面由于传入的是列表，而非`pandas`内部的`Series`，因此返回的是`DatetimeIndex`，
# 如果想要转为`datetime64[ns]`的序列，需要显式用`Series`转化：
pd.Series(temp)
df_date_cols = pd.DataFrame({'year': [2020, 2020],
                             'month': [1, 1],
                             'day': [1, 2],
                             'hour': [10, 20],
                             'minute': [30, 50],
                             'second': [20, 40]})
pd.to_datetime(df_date_cols) #注意列名必须是year,month,day,hour,minute,second

pd.date_range('2020-1-1','2020-1-21', freq='10D') # 生成时间序列，freq指定间隔
pd.date_range('2020-1-1','2020-2-28', freq='10D') # 不含28号，最后一个是20号
pd.date_range('2020-1-1', '2020-2-28', periods=6) # 28号结尾，freq>10天

s = pd.Series(np.random.rand(5), index=pd.to_datetime(['2020-1-%d'%i for i in range(1,10,2)]))
'''
2020-01-01    0.364130
2020-01-03    0.189897
2020-01-05    0.074438
2020-01-07    0.479496
2020-01-09    0.785153
dtype: float64
'''
s.asfreq('D').head() # 以天为间隔，补全缺失值
'''
2020-01-01    0.364130
2020-01-02         NaN
2020-01-03    0.189897
2020-01-04         NaN
2020-01-05    0.074438
Freq: D, dtype: float64
'''
s.asfreq('12H').head()
'''
2020-01-01 00:00:00    0.364130
2020-01-01 12:00:00         NaN
2020-01-02 00:00:00         NaN
2020-01-02 12:00:00         NaN
2020-01-03 00:00:00    0.189897
Freq: 12H, dtype: float64
'''
'''
    如同`category, string`的序列上定义了`cat, str`来完成分类数据和文本数据的操作，在时序类型的序列上
定义了`dt`对象来完成许多时间序列的相关操作。这里对于`datetime64[ns]`类型而言，可以大致分为三类操作：
取出时间相关的属性、判断时间戳是否满足条件、取整操作。
    第一类操作的常用属性包括：`date, time, year, month, day, hour, minute, second, microsecond, 
nanosecond, dayofweek, dayofyear, weekofyear, daysinmonth, quarter`，其中`daysinmonth, quarter`
分别表示该月一共有几天和季度。
'''
s = pd.Series(pd.date_range('2020-1-1','2020-1-3', freq='D'))
s.dt.date # 取出日期, 含年月日
s.dt.time # 取出时间，含时分秒
s.dt.day # 取出日
s.dt.daysinmonth # 取出每月天数
s.dt.dayofweek # 取出星期几，周一为0，周日为6
s.dt.month_name() # 取出月份名称
s.dt.day_name() # 取出星期名称，周一为Monday
s.dt.is_year_start # 还可选 is_quarter/month_start
s.dt.is_year_end # 还可选 is_quarter/month_end

#取整操作包含`round, ceil, floor`，它们的公共参数为`freq`，常用的包括`H, min, S`（小时、分钟、秒）
s = pd.Series(pd.date_range('2020-1-1 20:35:00', '2020-1-1 22:35:00', freq='45min'))
s.dt.round('1H') # 以1小时为间隔取整
s.dt.ceil('1H') # 向上取整
s.dt.floor('1H') # 向下取整

'''
时间戳序列作为索引使用。如果想要选出某个子时间戳序列，第一类方法是利用`dt`对象和布尔条件联合使用，
另一种方式是利用切片，后者常用于连续时间戳
'''
s = pd.Series(np.random.randint(2,size=366), index=pd.date_range('2020-01-01','2020-12-31'))
idx = pd.Series(s.index).dt
s.head()
'''
2020-01-01    0
2020-01-02    0
2020-01-03    1
2020-01-04    1
2020-01-05    1
Freq: D, dtype: int32
'''
s[(idx.is_month_start|idx.is_month_end).values].head() # 选出每月月初和月末的数据
'''
2020-01-01    0
2020-01-31    1
2020-02-01    1
2020-02-29    0
2020-03-01    0
dtype: int32
'''
s[idx.dayofweek.isin([5,6]).values].head() # 选出周六和周日的数据
s['2020-01-01'] # 选出某一天的数据
s['20200101'] # 自动转换标准格式
s['2020-07'].head() # 选出某一月的数据
s['2020-05':'2020-7-15'].head() # 选出某一段时间的数据,5月1日到7月15日
s['2020-05':'2020-7-15'].tail()

# 时间差
pd.Timestamp('20200102 08:00:00')-pd.Timestamp('20200101 07:35:00')
pd.Timedelta(days=1, minutes=25) # 需要注意加s
pd.Timedelta('1 days 25 minutes') # 字符串生成
s = pd.to_timedelta(df.Time_Record) # 生成时间差序列的主要方法
# 下面这个 TimedeltaIndex(['0 days 00:00:00', '0 days 00:06:00', '0 days 00:12:00'], 
# dtype='timedelta64[ns]', freq='6T')
pd.timedelta_range('0s', '1000s', freq='6min') # 生成时间差序列
# 下面这个 TimedeltaIndex(['0 days 00:00:00', '0 days 00:08:20', '0 days 00:16:40'],
#  dtype='timedelta64[ns]', freq=None)
pd.timedelta_range('0s', '1000s', periods=3) 
s.dt.seconds.head() # 取出秒数，对天数取余，从0到86399 .second从0到59
s.dt.total_seconds().head() # 取出总秒数
pd.to_timedelta(df.Time_Record).dt.round('min').head() # 取整操作



