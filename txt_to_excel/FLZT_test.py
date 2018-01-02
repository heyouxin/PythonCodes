# -*- coding: utf-8 -*-
#coding:utf-8
import csv
import re






'''
####PYTHON 2.7
def mycsv_reader(csv_reader): 
  while True: 
    try: 
      yield next(csv_reader) 
    except csv.Error: 
      # error handling what you want.
      pass
    continue 
  return
     
if __name__ == '__main__': 
    reader = mycsv_reader(csv.reader(open('FLZT_test2.csv', 'r')))
    #print(reader)
    for line in reader:
        #pass
        print(line[1])

reader.close()
'''

###存csv文件的时候，先新建一个excel，然后另存为CSV UTF-8   在CSV修改内容也要另存不然会乱码
###用csv模块读文件遇到编码错误，直接用UE打开原文件，另存为UTF-8的编码文件
'''
import tkinter.filedialog
fn=tkinter.filedialog.askopenfilename(title='选择一个文件', filetypes=[('所有文件','.*'),('文本文件','.txt')])
'''
'''
import pandas as pd
reader=pd.read_csv("FLZT20161228_ordered.csv")

'''
fn="FLZT20161228_ordered.csv"
with open(fn,'r',newline='',encoding='utf-8') as f:
    reader=csv.reader(f)
    L=[]
    l1=[]
    l2=['','','','','']
    #FL_sqh_cur=''
    #FL_sqh_pre=''
    for l1 in reader:
        #FL_sqh_cur=l1[2]
        #list第一个位置是0
        if(l1[1]!=l2[1]):
        #if (l1[0]!=''):
            ###上一条记录添加到list中，初始化l2
            L.append(l2)     
            l2=l1
        else:
            l2.append(l1[2])
            l2.append(l1[3])
            l2.append(l1[4])




    ###添加最后一条记录
    L.append(l2)  



    
    ###删除第一条空记录
    del L[0]
    ###删除抬头
    del L[0]
    print(len(L))
    #print(L)


#L.to_csv("FLZT20161228.csv")


import csv
with open('FLZT20161228.csv','w',newline='') as datacsv:
    csvwriter=csv.writer(datacsv)
    csvwriter.writerow(['授权公告号','申请号','法律状态公告日1','法律状态1','法律状态信息1','法律状态公告日2','法律状态2','法律状态信息2','法律状态公告日3','法律状态3','法律状态信息3','法律状态公告日4','法律状态4','法律状态信息4'])
    csvwriter.writerows(L)




'''
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
with open('csv_FLZT2.csv','w',newline='') as datacsv:
     csvwriter.writerow(["授权公告号","申请号","法律状态公告日","法律状态","法律状态信息"])
     csvwriter.writerows(records)

'''




