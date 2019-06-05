import pandas as pd
import math
import numpy as np
import os

def preprocess(csv_path1,csv_path2,separate_sign):
    ######## read data ############
    # origin_df = pd.read_csv(csv_path1,delimiter=",",encoding="utf-8")
    origin_df = pd.read_csv(csv_path1,delimiter=";",usecols=["aid","tname","title","view_num"],encoding="utf-8")#wait for score
    label_df = pd.read_csv(csv_path2)
    final_df = pd.merge(origin_df,label_df)

    ######### stop words ############
    def delete_stopwords(final_df):
        origin_title = final_df.pop("title")
        stopwords_file = open('./StopWords.txt', 'r', encoding='utf-8')
        stopwords_list = []
        for line in stopwords_file.readlines():
            stopwords_list.append(line[:-1])
        for i,sentence in enumerate(origin_title):
            sentence = list(sentence)
            for j,letter in enumerate(sentence):
                if letter in stopwords_list:
                    sentence[j] = " "
            # delete extra space
            origin_title[i] = "".join(sentence)# to str
            origin_title[i] = ' '.join(origin_title[i].split())
        final_df.insert(2,"title",origin_title)
    delete_stopwords(final_df)
    ######## data combined ###########
    tname = final_df.pop("tname")
    view = final_df.pop("view_num")
    overall = pd.Series(range(len(tname)))
    for i,item in enumerate(final_df.values):
        overall[i] = str(view[i])+ separate_sign+ tname[i]+separate_sign+item[1]
        view[i] = str(view[i])+separate_sign+item[1]
        tname[i] = tname[i]+separate_sign+item[1]

    final_df.insert(1,"tname",tname)
    final_df.insert(3,"view_num",view)
    final_df.insert(4,"overall",overall)
    print(final_df.head(5))
    final_df.to_csv("final_data2.csv",index=None,encoding="utf-8") # aid,tname,title,view_num,overall_label

def main():
    ######## hyperparams ##########
    csv_path1 = "./info_new12.csv"
    csv_path2 = "./label_result.csv"
    separate_sign = "."
    preprocess(csv_path1,csv_path2,separate_sign)
    df = pd.read_csv("./final_data2.csv")
    from sklearn.utils import shuffle
    df = shuffle(df)
    length = len(df)
    first = int(length*0.8)
    mid = int(length*0.9)
    df.iloc[:first,:].to_csv("./data2/train.csv", index=None,columns=None,encoding="utf-8")
    df.iloc[first:mid, :].to_csv("./data2/dev.csv", index=None, columns=None,encoding="utf-8")
    df.iloc[mid:, :].to_csv("./data2/test.csv", index=None,columns=None,encoding="utf-8")


if __name__=="__main__":
    main()