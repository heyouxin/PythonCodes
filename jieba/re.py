# -*- coding: utf-8 -*-
"""
Created on Fri Dec 29 17:34:45 2017

@author: 何友鑫
"""

import jieba
import pandas as pd
import re

file=open("aa.txt",'r',encoding='gbk')
data=file.readlines()
data=(str(data)).strip()
#print(data)
data2=re.split('[；，。、]',data)
data3=[]
for word in data2:
    if(re.search('生产的',word)):  
         data3.append(word)
fac=[]
product=[]
fac_wt=[]
for word in data3:
    if(re.search('公司生产的',word) or (re.search('）生产的',word) )):
        if(re.search('（委托方：',word)):
            temp=re.split('生产的',word)
            product.append(temp[1]) 
            fac_all=re.split('（委托方：',temp[0])
            fac.append(fac_all[0])
            fac_wt.append( str(fac_all[1]).replace('）',''))
           
        else:
            temp=re.split('生产的',word)
            fac.append(temp[0])
            product.append(temp[1])
            fac_wt.append('')

data4=[fac,fac_wt,product]
dict={'公司':fac,'委托方':fac_wt,'产品':product}
data4=pd.DataFrame(dict)   
data4.to_csv("cc.csv")


