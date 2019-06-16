# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 11:08:14 2018

@author: 何友鑫
"""

import os
import re
import pandas as pd

year='2016'
path = "./2016_txt" #文件夹目录  
files= os.listdir(path) #得到文件夹下的所有文件名称  
reports = []
for file in files: #遍历文件夹  
    if(re.search('已取消',file)):
        pass
    else:
        f = open(path+"/"+file,"r",encoding='utf8',errors='ignore') #打开文件  
        lines = f.readlines()#读取全部内容  
        n=0
        flag=0
        for line in lines: #遍历文件，一行行遍历，读取文本 
            n=n+1
            if(re.search('募投',line) or re.search('募集资金投资',line)):
                for i in range(n,len(lines)):
    
                    if(re.search('项目延期',lines[i]) or re.search('项目延迟',lines[i])):
                        #s.insert(2,company)
                        flag=1
                        print(file)
                        break
            if(flag==1):
                break
        #print(file)
        #2014的格式
        #file='2014-000001-平安银行：2014年年度报告'
        code_name=re.split('：',file)
        code_name=code_name[0]
        code=code_name[5:11]
        name=code_name[12:len(code_name)]
        l=[]
        l.append(code)
        l.append(name)
        l.append(year)
        l.append(flag)     
        #s.append(company)
        reports.append(l)




reports=pd.DataFrame(reports)
reports.columns=['公司代码','公司名称','年份','募投项目是否延期']
reports.to_excel('2016年报募投项目.xlsx')
  

     
     
     
     
     
