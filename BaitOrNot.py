from tkinter import Tk, filedialog
import csv
import tkinter.messagebox
import pandas as pd
import matplotlib.pyplot as plt

def input():
    Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
    filename = filedialog.askopenfilename()  # show an "Open" dialog box and return the path to the selected file
    data = []
    with open(filename, 'r', encoding='UTF-8') as f:
        csvFile = csv.reader((line.replace('\0','') for line in f), delimiter=';')  # replace the NULL byte
        flag = True #skip first line
        for row in csvFile:
            if flag==True:
                flag=False
                continue
            else:  # view_num, reply, favorite, coin, avid
                data.append([int(row[11]), int(row[13]), int(row[14]), int(row[15]), int(row[1])])
    return data

def preprocess(raw):
    tmp = []
    for line in raw:
        if line[0] <50000:
            continue
        else:
            tmp.append(line)

    new = []
    for a in tmp:  # view_num, reply, favorite, coin, avid
        A = min((200000 + a[0]) / (2 * a[0]), 1)
        B = min((a[2] * 20 + a[3] * 10)/(a[0] + a[3] * 10 + a[1] * 50), 1)
        new.append([a[0] * A, a[1] * B * 50, a[2] * 20, a[3] * B * 10, a[4]])

    return new

def hof(lof):
    hof = []
    for a in lof:  # (view_num + reply + favorite) / coin, avid
        hof.append([(a[1]+a[2]+a[3])/a[0], a[4]])
    return hof

def takeFirst(elem):
    return elem[0]

def classify(feature):
    feature.sort(key = takeFirst)  # 按照比例来排序
    return feature[int(len(feature)/5)][0]  # 输出后20%的比例分界线

def train():
    tkinter.messagebox.showinfo('提示', '您现在在训练模式下，请选择样本集！')
    raw_data = input()
    new_data = preprocess(raw_data[1:])
    hof_data = hof(new_data)
    boundary = classify(hof_data)
    f = open('boundary.txt', 'w')
    f.write(str(boundary))
    f.close()

def label(bou, hof):
    la = []
    for i in range(len(hof)):
        if bou < hof[i][0]:
            la.append([hof[i][1], 0])  # [avid, not bait]
        else:
            la.append([hof[i][1], 1])  # [avid, is bait]
    df = pd.DataFrame(la,columns=["aid","label"])
    df.to_csv("label_result.csv",index=None)



def give_label():
    f = open('boundary.txt')
    boundary = float(f.read())
    f.close()
    tkinter.messagebox.showinfo('提示', '您现在在标记模式下，请输入待标记的数据！')
    raw_data = input()
    new_data = preprocess(raw_data)
    hof_data = hof(new_data)
    label(boundary, hof_data)
    # print(la)

def main():
    # train()#generate boundary.txt
    give_label()

if __name__ ==  '__main__':
    main()
    # cnt =0
    # df = pd.read_csv("./label_result.csv")
    # for item in df.values:
    #     if item[1]=='1' or item[1]== 1 :
    #         cnt+=1
    # print(cnt)
