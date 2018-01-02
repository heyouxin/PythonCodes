# -*- coding: utf-8 -*-
"""
Created on Sun Jun 25 17:15:23 2017

@author: 何友鑫
"""

from a.Time1 import Time 
import a.Time1 as T
T.muPri()
#from a import Time1
#print (T.minute)
time1=Time()
print (time1.hour)
#print (time1.printMilitary())
#choice = input()
#print (type(choice))
#print (int(choice)+1)

list1=[1,0,3,4,5]

for i in range(5):
    try:
        num1=1/list1[i]
        print (num1)
    except  ZeroDivisionError:
        print ("do error")
 