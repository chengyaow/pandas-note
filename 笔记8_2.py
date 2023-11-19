import numpy as np
import pandas as pd
import re

re.findall(r'aaa|bbb', 'aaaabbbb') # ['aaa', 'bbb']
re.findall(r'a\\?|a\*', 'aa?a*a') # ['a', 'a', 'a', 'a']
re.findall(r'a?.', 'abaacadaae') # ['ab', 'aa', 'c', 'ad', 'aa', 'e']

# 简写字符集
'''
\w 匹配字母数字及下划线:[A-Za-z0-9_]
\W 匹配非字母数字及下划线:[^\w]
\d 匹配数字: [0-9]
\D 匹配非数字: [^\d]
\s 匹配任意空白字符，等价于 [\t\n\r\f\p{Z}].
\S 匹配任意非空字符: [^\s]
\B 匹配不是单词开头或结束的位置:匹配"othere"中的"the",但不能匹配"there"中的"the"
'''
re.findall(r'.s', 'Apple! This Is an Apple!') # ['is', 'Is']
re.findall(r'\w{2}', '09 8? 7w c_ 9q p@') # ['09', '7w', 'c_', '9q']
re.findall(r'\w\W\B', '09 8? 7w c_ 9q p@') # ['8?', 'p@']
re.findall(r'.\s.', 'Constant dropping wears the stone.') # ['t d', 'g w', 's t' 'e s']
re.findall(r'上海市(.{2,3}区)(.{2,3}路)(\d+号)', '上海市黄浦区方浜中路249号 上海市宝山区密山路5号')
'''[('黄浦区', '方浜中路', '249'), ('宝山区', '密山路', '5')]
(.{2,3}区)表示2到3个任何字符后面跟着`'区'`。`.`表示任何字符，`{2,3}`表示前面的字符可以出现2次或3次。
()表示一个捕获组，`re.findall`会返回每个捕获组匹配的内容。
(.{2,3}路)表示2到3个任何字符后面跟着`'路'`。
(\d+号)表示一个或多个数字后面跟着`'号'`。`\d`表示数字，`+`表示前面的字符可以出现一次或多次。
'''
#文本拆分
s = pd.Series(['上海市黄浦区方浜中路249号', '上海市宝山区密山路5号'])
s.str.split('[市区路]') # 0  [上海, 黄浦, 方浜中, 249号] 1  [上海, 宝山, 密山, 5号]
s.str.split('[市区路]', n=2, expand=True) #最大拆分次数为2，expand=True展开为多列
'''
    0   1     2
0  上海  黄浦  方浜中路249号
1  上海  宝山     密山路5号
'''
s.str.rsplit('[市区路]', n=2, expand=True) #从右向左拆分，有bug

# 文本合并
s = pd.Series([['a','b'], [1, 'a'], [['a', 'b'], 'c']])
s.str.join('-') 
''' 出现非字符串元素,返回NaN
0    a-b
1    NaN
2    NaN
dtype: object'''
'''`str.cat`用于合并两个序列，主要参数为连接符`sep`、连接形式`join`以及缺失值替代符号`na_rep`，
其中连接形式默认为以索引为键的左连接。'''
s1 = pd.Series(['a','b'])
s2 = pd.Series(['cat','dog'])
s1.str.cat(s2,sep='-')
'''0    a-cat
   1    b-dog'''
s2.index = [1, 2]
s1.str.cat(s2, sep='-', na_rep='?', join='outer')
'''0      a-?
   1      b-cat
   2      ?-dog'''
s = pd.Series(['my cat', 'he is fat', 'railway station'])
s.str.contains(r'\s\wat') #判断是否包含空格+任意数字字母+at
'''0    True
   1    True
   2    False'''
s.str.startswith('my') #判断是否以my开头
s.str.endswith('t') #判断是否以t结尾
s.str.match('m|h') #判断是否以m或h开头
s.str[::-1].str.match('ta[fg]|n') #判断反转后是否以taf或tag或n结尾 
s.str.contains('^[mh]') #判断是否以m或h开头
s.str.contains('[fg]at|n$') #判断是否以fat或gat或n结尾

'''贪婪匹配：在满足匹配条件的情况下，尽可能多地匹配字符。也就是说，贪婪匹配会尽可能长地匹配字符串。
例如，对于正则表达式`a.*b`和字符串`'acbdb'`，贪婪匹配会匹配整个字符串`'acbdb'`。
   非贪婪匹配：在满足匹配条件的情况下，尽可能少地匹配字符。也就是说，非贪婪匹配会尽可能短地匹配字符串。
非贪婪匹配可以通过在量词后面添加`?`来实现。例如，对于正则表达式`a.*?b`和字符串`'acbdb'`，非贪婪匹配会匹配`'acb'`。
贪婪匹配和非贪婪匹配的区别在于匹配的长度。贪婪匹配尽可能多地匹配字符，而非贪婪匹配尽可能少地匹配字符。'''

s = pd.Series(['This is an apple. That is not an apple.'])
s.str.find('apple') #返回第一个apple的起始位置,没有返回-1.11
s.str.rfind('apple') #返回最后一个apple的起始位置. 33
s = pd.Series(['a_1_b','c_?'])
s.str.replace(r'\d|\?', 'new', regex=True) #将数字和?替换为new,regex=True表示正则表达式

s = pd.Series(['上海市黄浦区方浜中路249号',
                '上海市宝山区密山路5号',
                '北京市昌平区北农路2号'])
pat = r'(\w+市)(\w+区)(\w+路)(\d+号)'
city = {'上海市': 'Shanghai', '北京市': 'Beijing'}
district = {'昌平区': 'CP District',
            '黄浦区': 'HP District',
            '宝山区': 'BS District'}
road = {'方浜中路': 'Mid Fangbin Road',
        '密山路': 'Mishan Road',
        '北农路': 'Beinong Road'}
def my_func(m):
    str_city = city[m.group(1)] #group(1)表示第一个括号内的内容
    str_district = district[m.group(2)]
    str_road = road[m.group(3)]
    str_no = 'No. ' + m.group(4)[:-1] #去掉最后一个字，即去掉号
    return ' '.join([str_city, str_district, str_road, str_no])
s.str.replace(pat, my_func, regex=True)

#命名捕获组
pat = r'(?P<市名>\w+市)(?P<区名>\w+区)(?P<路名>\w+路)(?P<编号>\d+号)'
def my_func2(m):
    str_city = city[m.group('市名')]
    str_district = district[m.group('区名')]
    str_road = road[m.group('路名')]
    str_no = 'No. ' + m.group('编号')[:-1]
    return ' '.join([str_city, str_district, str_road, str_no])
s.str.replace(pat, my_func2, regex=True)

pat = r'(\w+市)(\w+区)(\w+路)(\d+号)'
s.str.extract(pat) #提取匹配的内容,返回一个DataFrame
pat = r'(?P<市名>\w+市)(?P<区名>\w+区)(?P<路名>\w+路)(?P<编号>\d+号)'
s.str.extract(pat) #提取匹配的内容,返回一个DataFrame,列名为命名捕获组的名称

s = pd.Series(['A135T15,A26S5','B674S2,B25T6'], index = ['my_A','my_B'])
pat = r'[A|B](\d+)[T|S](\d+)' #括号内的内容为捕获组，不需要提取的内容不要加括号
s.str.extractall(pat) #提取所有匹配的捕获组,返回一个多级索引的DataFrame,列名为0,1,2,3
pat_with_name = r'[A|B](?P<name1>\d+)[T|S](?P<name2>\d+)' #命名捕获组，列名为name1,name2
s.str.extractall(pat_with_name)
s.str.findall(pat) #返回所有匹配的列表，列表中的元素为元组，而不是返回一个多级索引的DataFrame

# 常用字符串函数
s = pd.Series(['lower', 'CAPITALS', 'this is a sentence', 'SwApCaSe'])
s.str.upper() #全部大写
s.str.lower() #全部小写
s.str.title() #首字母大写
s.str.capitalize() #首字母大写
s.str.swapcase() #大小写互换
s.str.len() #字符串长度

s = pd.Series(['1', '2.2', '2e', '??', '-2.1', '0'])
pd.to_numeric(s, errors='ignore') #忽略错误，保持原来的字符串
pd.to_numeric(s, errors='coerce') #转换为缺失值
pd.to_numeric(s, errors='raise') #报错
s[pd.to_numeric(s, errors='coerce').isna()] #返回非数值行
s = pd.Series(['cat rat fat at', 'get feed sheet heat'])
s.str.count('[r|f]at|ee') #返回匹配的次数

my_index = pd.Index([' col1', 'col2 ', ' col3 '])
my_index.str.strip().str.len() #去除两边空格后求长度
my_index.str.rstrip() #去除右边空格
my_index.str.lstrip() #去除左边空格
s = pd.Series(['a','b','c'])
s.str.pad(5,'left','*') # 填充在左边，****a,****b,****c
s.str.pad(5,'right','*') # 填充在右边，a****,b****,c****
s.str.pad(5,'both','*') # 填充在两边，**a**,**b**,**c**

s = pd.Series([7, 155, 303000]).astype('string')
s.str.pad(6,'left','0') # 000007,000155,303000
s.str.rjust(6,'0') # 000007,000155,303000，
s.str.zfill(6) # 000007,000155,303000,只能在左边填充0
