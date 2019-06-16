# -*- coding: utf-8 -*-
"""

-------------------------------------------------
   File Name：        test_multi
   Description :
   Author :           何友鑫
   Create date：      2018-10-26
   Latest version:    v1.0.0
-------------------------------------------------
   Change Log:
#-----------------------------------------------#
    v1.0.0            hyx        2018-10-26
    1.
#-----------------------------------------------#
-------------------------------------------------

"""
import time
from multiprocessing.pool import ThreadPool
from multiprocessing import Pool
import multiprocessing
import datetime
def calc():
    t = 0
    for i in range(1000000000):
        t += i
    return t

def thread_pool(num=4):
    p = ThreadPool(num)
    start_time = time.time()
    ret = p.map(calc)
    p.close()
    p.join()
    print("thread_pool  %d, costTime: %fs ret.size: %d" % (num, (time.time() - start_time), len(ret)))
    print(ret)

if __name__ == '__main__':
    #multiprocessing.cpu_count()
    t_start = datetime.datetime.now()
    #pool = Pool(4)                # 创建进程池对象，进程数与multiprocessing.cpu_count()相同
    #tofs = pool.apply_async(calc)
    #pool.close()
    #pool.join()
    #print(tofs.get())
    #t = calc()
    #print(t)
    #thread_pool()
    thread_pool()
    t_end = datetime.datetime.now()
    print(t_end-t_start)


