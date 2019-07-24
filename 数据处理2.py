import pandas as pd
import numpy as np
import csv
import json
import math



df = pd.read_csv("thiers_2012.csv",header = None)
df.columns =['total']
#print(df)
#print(df['total'])
df = df['total'].str.split('\t',expand =True)
df.columns = ['time','id0','id1','class0','class1']
#print(df)
dic = {}
for index,row in df.iterrows():
    dic[row['id0']] = row['class0']
    dic[row['id1']] = row['class1']
l = []
for key in dic.keys():
    l.append([key,dic[key]])
#print(len(dic))
df1 = pd.DataFrame(l)
df1.columns = ['id','class']
#print(len(df1['class'].unique())) #5个不同班级
#print(df1)
df1.to_csv("id_class.csv", index = None)