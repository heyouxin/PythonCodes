# -*- coding: utf-8 -*-
"""
Created on Fri May 19 21:56:55 2017

@author: 何友鑫
"""
import math as m
l1=[0.07,0.07,0.07,0.07,0.07];
l2=[0.05,0.06,0.07,0.08,0.09];
l3=[0.09,0.08,0.07,0.06,0.05]

def count_discount(l):
    l_temp=[]
    for T in range(len(l)):
        q_T=1/m.pow(1+l[T],T+1)
        print (q_T)
        l_temp.append(q_T)
    return l_temp        
    
print (count_discount(l1))
print (" ---")
count_discount(l2)
print (" ---")
count_discount(l3)
print (" ---")    


print (1/m.pow(1+0.1,2))
print (20*0.952+100*0.826)