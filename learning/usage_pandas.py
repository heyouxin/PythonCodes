# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 16:28:05 2017

@author: 何友鑫
"""

import pandas as pd
data=pd.read_csv("data_tail.csv")
data2=pd.read_excel("file:///C:/Users/heyouxin/Desktop/高级微观经济学2助教office hour安排表(王老师班).xlsx")
data2.to_excel("./files/bb.xlsx")
print (data2)
s=pd.Series([1,2,3,4,5])
print (s)
t=pd.Series([2,4,6,8,10])
t.plot()
#data.to_csv("aa.csv")

#pd.DataFrame.to_csv()
import math as m
m.exp(0.5*m.log(7000)+0.5*m.log(3000))
5000-4582.58
