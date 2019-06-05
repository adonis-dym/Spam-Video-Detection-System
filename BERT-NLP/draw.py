import matplotlib.pyplot as plt
from pylab import *                                 #支持中文
mpl.rcParams['font.sans-serif'] = ['SimHei']

names = ['title_5', 'title_3', '+type_3', '+type+clicks_3', '+type+clicks_2']
x = range(len(names))
y = [0.605,0.629,0.618, 0.619, 0.641]#
y1 = [0.845,0.854,0.851, 0.853, 0.857]
y2 = [0.663,0.342,0.398, 0.376, 0.326]
y3 =[0.568,0.590,0.595,0.62,0.582]
#plt.plot(x, y, 'ro-')
#plt.plot(x, y1, 'bo-')
#pl.xlim(-1, 11)  # 限定横轴的范围
#pl.ylim(-1, 110)  # 限定纵轴的范围
plt.ylim(ymax=0.9)
plt.ylim(ymin=0.3)
plt.plot(x, y, marker='o', color='r',label=u'precision')
plt.plot(x, y1, marker='*', mec='b',label=u'y=accuracy')
plt.plot(x, y2, marker='x', mec='k',label=u'y=loss')
plt.plot(x, y3, marker='s', mec='g',label=u'y=recall')
plt.legend()  # 让图例生效
plt.xticks(x, names)
plt.margins(0)
plt.subplots_adjust(bottom=0.15)
plt.xlabel(u"Model Name") #X轴标签
plt.ylabel("rate") #Y轴标签
plt.title("EXP result") #标题
plt.show()