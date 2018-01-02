# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 09:07:28 2017

@author: 何友鑫
"""
from __future__ import division
#list链表 下标和c++一致 0下标表示第一个元素
b=[7,8,9]
a=[1,b,3,4,5,6]
l=len(a)

print (l)
print (a[0])
print (a[5])

# range(0,5) #代表从0到5(不包含5)
for i in range(0,l) :
    print (a[i])

print (a[1][0])


#字典
c={'a':1,'b':2}
d={'c':3,'d':4}
print (c['a'])
print (c)
print (c.values())
    
import pandas as pd
print (pd.Series(c))
##key是行名，value是dataframe 的值
print (pd.DataFrame({'c':c,'d':d}))



##用List一次性生成字典
print (list(zip(('x','y','z'),(1,2,3))))
my_zip=list(zip(('x','y','z'),(1,2,3)))
my_map=dict(my_zip)
print (my_map)    


#函数式编程 map 和r 的 lapply
test_list=[(1,2),(3,4)]
print (test_list)


import pandas as pd
def f(x,y):
    return (x+y-0.5)/100
print (list(map(f,[1,2],[0.5,4])))
print (list(map(str,['0933',2,3,4,5])))


def is_odd(x):
    return x%2 == 1
print (list(filter(is_odd,[1,2,3,4,5,6,7,8,9])))





