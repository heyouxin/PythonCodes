
#names=['a','b','c']
#for name in names:
#    print(name)


#L=[('<rec>','123213213','fdfd'),('<REC>')]
#print(L)
#for i in L:
 #   print(i)

'''
iii
'''
'''
import datetime
begin = datetime.datetime.now()
n=0
for i in (range(100000000)):
   n=i+n 
end = datetime.datetime.now()
print(end-begin)
print(n)
'''


import re
import tkinter.filedialog
fn=tkinter.filedialog.askopenfilename(title='选择一个文件', filetypes=[('所有文件','.*'),('文本文件','.txt')])


f = open(fn, 'r',encoding='gbk', errors='ignore')
#f = open(fn, 'r',encoding='gbk')
print("open success!")
L=f.readlines()
print("read success!")
f.close()
#print(L[0:100])
records=[]
l1=[]
GKR=''
GKH=''
for line in L:
    line=line.rstrip('\n')
    #print(line)
    if (line=='<REC>'):
        l1.append(GKR)
        l1.append(GKH)
        records.append(l1)
        
        l1=[]
        GKR=''
        GKH=''
    elif (re.search('<公开（公告）日>',line)):
        s1=line.split('>=')
        #s2=s1[1].split('\n')
        #print(s2)
        GKR=s1[1]
        #print(GKR)
    elif (re.search('<公开（公告）号>',line)):
        s1=line.split('>=')
        #s2=s1[1].split('\n')
        #print(s2[0])
        GKH=s1[1]
    #elif (line=='\n'):
l1.append(GKR)
l1.append(GKH)
records.append(l1)
#print(records)

            
del records[0]
print(len(records))       
print(records)

import csv
with open("csv_test.csv","w",newline="") as datacsv:
     #dialect为打开csv文件的方式，默认是excel，delimiter="\t"参数指写入的时候的分隔符
     csvwriter = csv.writer(datacsv,dialect = ("excel"))
     #csv文件插入一行数据，把下面列表中的每一项放入一个单元格（可以用循环插入多行）
     csvwriter.writerow(["公开日","公号号"])
     csvwriter.writerows(records)




'''
import re
l1=[]
GKR=''
s='<公开（公告）日>=1990.01.03\n'
#print(s)
if (re.search('<公开（公告）日>',s)):
    print('yes')
    s1=s.split('>=')
    s2=s1[1].split('\n')
    print(s2[0])
    GKR=s2[0]
l1.append(GKR)
print(l1)
  '''  



'''
L=[]
l1=['a','b','c']
l2=['22223','b','cccccc']
L.append(l1)
L.append(l2)
print(L[0][2])
'''




