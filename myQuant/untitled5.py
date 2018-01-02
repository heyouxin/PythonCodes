# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 14:50:06 2017

@author: 何友鑫
"""

import tushare as ts
import pandas as pd

HS300_data=ts.get_k_data('000300', index=True)


test=HS300_data.ix[:,0:2]
#HS300_data.to_excel("HS300.xlsx")
HS300_data[HS300_data.p_change<=-1]['token']=0
  HS300_data[HS300_data.p_change>=1]['token']=2       
     
          
HS300_data['token']=0


HS300_data.to_csv("HS300_2.csv")




l=[0,3,5]
for i in l:

    try:
        a=0
        b=1
        c=b/i
        try:
            c=b/a
        except:
            #d=4
            pass
        '''
        try:
            c=a/b
        except:
            pass
            #print("error2")
        d=2
        '''
    except:
        print(i)
        #print("error")
    finally:
        e=a+i
        print(e)
    f=a+i
    print(f)



a=0
b=1
i=0
try:
    b=2
    c=b/i
except:
    pass
    #print(i)
    #print("error")
else:
    try:
    else:
finally:
    e=b+i
    print(e)
f=b+i
print(f)




try:
    d[1]@E#
except:
    print(2)
else:
    print(1)
    try:
        pass
    except:
        pass
    else:
        

        
        
        
        
        
import threading
import time





exitFlag = 0

class myThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        print ("开始线程：" + self.name)
        print_time(self.name, self.counter, 5)
        print ("退出线程：" + self.name)

def print_time(threadName, delay, counter):
    while counter:
        if exitFlag:
            threadName.exit()
        time.sleep(delay)
        print ("%s: %s" % (threadName, time.ctime(time.time())))
        counter -= 1

# 创建新线程
thread1 = threading.Thread(1, "Thread-1", 1)
thread2 = threading.Thread(2, "Thread-2", 2)
thread3 = myThread(3, "Thread-3", 3)
thread4 = myThread(4, "Thread-4", 4)

# 开启新线程
thread1.start()
thread2.start()
thread3.start()
thread4.start()
thread1.join()
thread2.join()
thread3.join()
thread4.join()
print ("退出主线程")



