import pandas as pd
def mergeit():
    df1 = pd.read_csv("./text_result.csv")
    df2 = pd.read_csv("./image_result.csv")
    new = df1.merge(df2)
    tmp = []
    for item in new.values:
        if int(item[4]) == 1:
            if int(item[5]) == 1:
                tmp.append(1)
            else:
                tmp.append(0.5)
        else:
            tmp.append(0)
    new.insert(6,"pred_combined",tmp)
    print(new)
    new.to_csv("combined_result.csv",index=None)
def cal():
    new = pd.read_csv("./combined_result.csv")
    pos = 0
    we_get = 0
    precision = 0
    recall = 0
    for item in new.values:
        if int(item[1]) ==1:
            pos+=1
            if int(item[-1])==1:
                recall+=1
        if int(item[-1])==1:
            we_get+=1
            if int(item[1])==1:
                precision+=1
    print(pos,recall,we_get,precision)
    print(recall/pos)
    print(precision/we_get)

# mergeit()
cal()