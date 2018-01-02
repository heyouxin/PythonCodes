# -*- coding: utf-8 -*-
#coding:utf-8

import re
import tkinter.filedialog
fn=tkinter.filedialog.askopenfilename(title='选择一个文件', filetypes=[('所有文件','.*'),('文本文件','.txt')])


f = open(fn, 'r',encoding='utf-8', errors='ignore')
###测试文件用gbk
#f = open(fn, 'r',encoding='gbk')

###2.7版本的python codecs.open 或 io.open
#import codecs
#f=codecs.open(fn,'r','utf-8')

print("open success!")
L=f.readlines()
print("read success!")
f.close()
#print(L[0:40])


records=[]
l1=[]
SQGGH=''
SQH=''
FLZTGGR=''
FLZT=''
FLZTXX=''
#for line in f:
    #line=f.readline()
for line in L:
    line=line.rstrip('\n')
    if (re.search('<REC>',line)):
    #if (line=='<REC>'):
        l1.append(SQGGH)
        l1.append(SQH)
        l1.append(FLZTGGR)
        l1.append(FLZT)
        l1.append(FLZTXX)
        records.append(l1)


        
        l1=[]
        SQGGH=''
        SQH=''
        FLZTGGR=''
        FLZT=''
        FLZTXX=''

    elif (re.search('<授权公告号>',line)):
        s1=line.split('>=')
        #s2=s1[1].split('\n')
        #print(s2[0])
        SQGGH=s1[1]
    elif (re.search('<申请号>',line)):
        s1=line.split('>=')
        #s2=s1[1].split('\n')
        #print(s2[0])
        SQH=s1[1]
    elif (re.search('<法律状态公告日>',line)):
        s1=line.split('>=')
        #s2=s1[1].split('\n')
        #print(s2[0])
        FLZTGGR=s1[1]
    elif (re.search('<法律状态>',line)):
        s1=line.split('>=')
        #s2=s1[1].split('\n')
        #print(s2[0])
        FLZT=s1[1]
    elif (re.search('<法律状态信息>',line)):
        s1=line.split('>=')
        #s2=s1[1].split('\n')
        #print(s2[0])
        FLZTXX=s1[1]
    #elif (line=='\n'):
l1.append(SQGGH)
l1.append(SQH)
l1.append(FLZTGGR)
l1.append(FLZT)
l1.append(FLZTXX)
records.append(l1)
#print(records)
del records[0]
print(len(records))       

      



import csv
with open("csv_FLZT2.csv","w",newline="") as datacsv:
     #dialect为打开csv文件的方式，默认是excel，delimiter="\t"参数指写入的时候的分隔符
     csvwriter = csv.writer(datacsv,dialect = ("excel"))
     #csv文件插入一行数据，把下面列表中的每一项放入一个单元格（可以用循环插入多行）
     csvwriter.writerow(["授权公告号","申请号","法律状态公告日","法律状态","法律状态信息"])
     csvwriter.writerows(records)






