# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 18:59:32 2017

@author: 何友鑫
"""

f = open("foo.txt")             # 返回一个文件对象  
line = f.readline()             # 调用文件的 readline()方法  
while line:                   # 后面跟 ',' 将忽略换行符  
    # print(line, end = '')　　　# 在 Python 3中使用  
    line = f.readline()  

f.close() 