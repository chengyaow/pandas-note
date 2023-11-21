import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import pandas as pd
import re
import matplotlib
from matplotlib.lines import Line2D   
from matplotlib.patches import Circle, Wedge
from matplotlib.collections import PatchCollection

fig, ax = plt.subplots()  # 创建一个包含一个axes的figure
ax.plot([1, 2, 3, 4], [1, 4, 2, 3]);  # 绘制图像
line =plt.plot([1, 2, 3, 4], [1, 4, 2, 3])  # 绘制图像

x = np.linspace(0, 2, 100)
fig, ax = plt.subplots()  # 创建一个包含一个axes的figure
ax.plot(x, x, label='linear')  
ax.plot(x, x**2, label='quadratic')  
ax.plot(x, x**3, label='cubic')  
ax.set_xlabel('x label') 
ax.set_ylabel('y label') 
ax.set_title("Simple Plot")  
ax.legend() # 显示图例
plt.show() # 显示图像

# 也可以使用plt的函数
plt.plot(x, x, label='linear') 
plt.plot(x, x**2, label='quadratic')  
plt.plot(x, x**3, label='cubic')
plt.xlabel('x label')
plt.ylabel('y label')
plt.title("Simple Plot")
plt.legend()
plt.show()

'''惯用套路'''
# step1 准备数据
x = np.linspace(0, 2, 100)
y = x**2

# step2 设置绘图样式，这一模块的扩展参考第五章进一步学习，这一步不是必须的，样式也可以在绘制图像是进行设置
mpl.rc('lines', linewidth=4, linestyle='-.') # 设置线宽，线型

# step3 定义布局， 这一模块的扩展参考第三章进一步学习
fig, ax = plt.subplots()  # 创建一个包含一个axes的figure

# step4 绘制图像， 这一模块的扩展参考第二章进一步学习
ax.plot(x, y, label='linear')  

# step5 添加标签，文字和图例，这一模块的扩展参考第四章进一步学习
ax.set_xlabel('x label') 
ax.set_ylabel('y label') 
ax.set_title("Simple Plot")  
ax.legend() 

'''
线的常用属性
属性	     说明
alpha	     透明度
color	     颜色
linestyle	 线型
linewidth	 线宽
marker	     标记
markersize	 标记大小
xdata	     线的x数据,默认为range(1,len(y)+1)
ydata	     线的y数据
'''
x = range(0,5)
y = [2,5,7,8,10]

plt.plot(x,y, linewidth=10); # 设置线的粗细参数为10

line, = plt.plot(x, y, '-') # 这里等号坐标的line,是一个列表解包的操作，目的是获取plt.plot返回列表中的Line2D对象
# plt.plot()函数返回的是一个线对象的列表，即使只绘制了一条线。所以，我们需要使用,来进行解包，获取列表中的第一个元素
line.set_antialiased(False); # 关闭抗锯齿功能

lines = plt.plot(x, y)
plt.setp(lines, color='r', linewidth=10)

x = range(0,5)
y1 = [2,5,7,8,10]
y2= [3,6,8,9,11]
fig,ax= plt.subplots()
ax.plot(x,y1)
ax.plot(x,y2)
print(ax.lines); # 通过直接使用辅助方法画线，打印ax.lines后可以看到在matplotlib在底层创建了两个Line2D对象

x = range(0,5)
y1 = [2,5,7,8,10]
y2= [3,6,8,9,11]
fig,ax= plt.subplots()
lines = [Line2D(x, y1), Line2D(x, y2,color='orange')]  # 显式创建Line2D对象
for line in lines:
    ax.add_line(line) # 使用add_line方法将创建的Line2D添加到子图中
ax.set_xlim(0,4)
ax.set_ylim(2, 11)