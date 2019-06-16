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
import multiprocessing
import datetime
def calc():
    t = 0
    for i in range(1000000):
        t += i
    return t

if __name__ == '__main__':
    t_start = datetime.datetime.now()
    t = calc()
    t_end = datetime.datetime.now()
    print(t)
    print(t_end-t_start)

