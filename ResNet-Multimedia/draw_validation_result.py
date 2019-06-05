import re
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

with open('./train_resnet_101_20W_ans/ans-1000-to-40000.txt', 'r') as f:
    readstr0 = str(f.read())
    val_acc0 = re.findall(r'val_acc:[0-9.]*', readstr0)
    for i in range(len(val_acc0)):
        val_acc0[i] = float(val_acc0[i].split(':')[1])

with open('./train_resnet_101_20W_ans/ans-5000-stride.txt', 'r') as f:
    readstr = str(f.read())
    val_acc = re.findall(r'val_acc:[0-9.]*', readstr)
    for i in range(len(val_acc)):
        val_acc[i] = float(val_acc[i].split(':')[1])
val_acc = val_acc[8:]
val_acc = val_acc0 + val_acc
maxindex = val_acc.index(max(val_acc))
leg = ['Validation accuracy']

x = list(range(1000, 40000, 1000)) + list(range(40000, 155000, 5000))
plt.plot(x, val_acc)
plt.legend(leg, loc=4, fontsize=12)
plt.plot(x[maxindex], max(val_acc), marker='o', markersize=7.5, color='red')
plt.xlabel('Number of steps')
plt.ylabel('Validation accuracy')
plt.annotate('({}, {})'.format(int(x[maxindex]), round(max(val_acc), 4)),
             xy=(x[maxindex], max(val_acc)), xytext=(x[maxindex] + 2000, max(val_acc)),
             fontsize=14)

plt.show()
