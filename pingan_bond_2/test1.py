# -*- coding: utf-8 -*-
"""

-------------------------------------------------
   File Name：        test1
   Description :
   Author :           何友鑫
   Create date：      2018-10-10
   Latest version:    v1.0.0
-------------------------------------------------
   Change Log:
#-----------------------------------------------#
    v1.0.0            hyx        2018-10-10
    1.
#-----------------------------------------------#
-------------------------------------------------

"""
from multiprocessing import Pool
import time

def Foo(t):
    #time.sleep(2)
    #t = 0
    for i in range(1000000):
        t += i
    return t

def Bar(arg):
    return arg

if __name__ == '__main__':
    res_list=[]
    t_start=time.time()
    pool = Pool(4)

    #for i in range(10):
    i=0
    res = pool.apply_async(func=Foo, args=(i,), callback=Bar)

    res_list.append(res)

    pool.close()
    pool.join()
    for res in res_list:
        print (res.get())
    #print(res.get())
    t_end=time.time()
    t=t_end-t_start
    print ('the program time is :%s' %t)

