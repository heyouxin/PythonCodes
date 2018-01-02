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
GKH=''
GKR=''
SQH=''
SQR=''
ZLH=''
MC=''
ZFLH=''
FLH=''
SQZLR=''
FMR=''
ZY=''

ZQX=''
YXQ=''



GSDM=''
DZ=''
ZLDLJG=
DLR=''

SCY=''

FBLJ=''
YS=''
SQGDM=''
ZLLX=''
SQLY=''

CKWX=''
#for line in f:
    #line=f.readline()
for line in L:
    line=line.rstrip('\n')
    if (re.search('<REC>',line)):
    #if (line=='<REC>'):
        l1.append(GKH)
        l1.append(GKR)
        l1.append(SQH)
        l1.append(SQR)
        l1.append(ZLH)

        
        l1.append(MC)
        l1.append(ZFLH)
        l1.append(FLH)
        l1.append(SQZLR)
        l1.append(FMR)
        l1.append(ZY)

        l1.append(ZQX)
        l1.append(YXQ)

        l1.append(GSDM)
        l1.append(DZ)
        l1.append(ZLDLJG)
        l1.append(DLR)

        l1.append(SCY)

        l1.append(FBLJ)
        l1.append(YS)
        l1.append(SQGDM)
        l1.append(ZLLX)
        l1.append(SQLY)

        l1.append(CKWX)
        records.append(l1)


        
        l1=[]
        GKH=''
        GKR=''
        SQH=''
        SQR=''
        ZLH=''
        MC=''
        ZFLH=''
        FLH=''
        SQZLR=''
        FMR=''
        ZY=''

        ZQX=''
        YXQ=''



        GSDM=''
        DZ=''
        ZLDLJG=
        DLR=''

        SCY=''

        FBLJ=''
        YS=''
        SQGDM=''
        ZLLX=''
        SQLY=''

        CKWX=''

    elif (re.search('<公开（公告）号>',line)):
        s1=line.split('>=')
        #s2=s1[1].split('\n')
        #print(s2[0])
        GKH=s1[1]
    elif (re.search('<公开（公告）日>',line)):
        s1=line.split('>=')
        GKR=s1[1]
    elif (re.search('<申请号>',line)):
        s1=line.split('>=')
        SQH=s1[1]
    elif (re.search('<申请日>',line)):
        s1=line.split('>=')
        SQR=s1[1]
    elif (re.search('<专利号>',line)):
        s1=line.split('>=')
        ZLH=s1[1]
    elif (re.search('<名称>',line)):
        s1=line.split('>=')
        MC=s1[1]
    elif (re.search('<主分类号>',line)):
        s1=line.split('>=')
        ZFLH=s1[1]
    elif (re.search('<分类号>',line)):
        s1=line.split('>=')
        FLH=s1[1]   
    elif (re.search('<申请（专利权）人>',line)):
        s1=line.split('>=')
        SQZLR=s1[1]
    elif (re.search('<发明（设计）人>',line)):
        s1=line.split('>=')
        FMR=s1[1]

       
    elif (re.search('<摘要>',line)):
        s1=line.split('>=')
        ZY=s1[1]

    elif (re.search('<主权项>',line)):
        s1=line.split('>=')
        #s2=s1[1].split('\n')
        #print(s2[0])
        ZQX=s1[1]
    elif (re.search('<优先权>',line)):
        s1=line.split('>=')
        YXQ=s1[1]
        
    elif (re.search('<国省代码>',line)):
        s1=line.split('>=')
        GSDM=s1[1]
    elif (re.search('<地址>',line)):
        s1=line.split('>=')
        DZ=s1[1]
    elif (re.search('<专利代理机构>',line)):
        s1=line.split('>=')
        ZLDLJG=s1[1]
    elif (re.search('<代理人>',line)):
        s1=line.split('>=')
        #s2=s1[1].split('\n')
        #print(s2[0])
        DLR=s1[1]
        
    elif (re.search('<审查员>',line)):
        s1=line.split('>=')
        #s2=s1[1].split('\n')
        #print(s2[0])
        SCY=s1[1]

    elif (re.search('<发布路径>',line)):
        s1=line.split('>=')
        #s2=s1[1].split('\n')
        #print(s2[0])
        FBLJ=s1[1]
    elif (re.search('<页数>',line)):
        s1=line.split('>=')
        YS=s1[1]
    elif (re.search('<申请国代码>',line)):
        s1=line.split('>=')
        SQGDM=s1[1]
    elif (re.search('<专利类型>',line)):
        s1=line.split('>=')
        ZLLX=s1[1]
    elif (re.search('<申请来源>',line)):
        s1=line.split('>=')
        SQLY=s1[1]

    elif (re.search('<参考文献>',line)):
        s1=line.split('>=')
        CKWX=s1[1]
        
    #elif (line=='\n'):
    
l1.append(GKH)
l1.append(GKR)
l1.append(SQH)
l1.append(SQR)
l1.append(ZLH)


l1.append(MC)
l1.append(ZFLH)
l1.append(FLH)
l1.append(SQZLR)
l1.append(FMR)
l1.append(ZY)

l1.append(ZQX)
l1.append(YXQ)

l1.append(GSDM)
l1.append(DZ)
l1.append(ZLDLJG)
l1.append(DLR)

l1.append(SCY)

l1.append(FBLJ)
l1.append(YS)
l1.append(SQGDM)
l1.append(ZLLX)
l1.append(SQLY)

l1.append(CKWX)

records.append(l1)
#print(records)
del records[0]
print(len(records))       

      



import csv
with open("csv_SG2.csv","w",newline="") as datacsv:
     #dialect为打开csv文件的方式，默认是excel，delimiter="\t"参数指写入的时候的分隔符
     csvwriter = csv.writer(datacsv,dialect = ("excel"))
     #csv文件插入一行数据，把下面列表中的每一项放入一个单元格（可以用循环插入多行）
     csvwriter.writerow(["公开（公告）号","公开（公告）日","申请号","申请日","专利号","名称","主分类号","分类号","申请（专利权）人","发明（设计）人","摘要","主权项","优先权","国省代码","地址","专利代理机构","代理人","审查员","发布路径","页数","申请国代码","专利类型","申请来源","参考文献"])
     csvwriter.writerows(records)






