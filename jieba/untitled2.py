
import jieba
import pandas as pd
import re


file=open("aa.txt",'r',encoding='gbk')
data=file.readlines()
data=(str(data)).strip()
 
data2=re.split('[；、。]',data)
#data2=data

data3=[]
for word in data2:
     if(re.search('生产的',word)):
         data3.append(word)
 
 
 data4='/' .join(jieba.cut(str(data3), cut_all=False)) 
 