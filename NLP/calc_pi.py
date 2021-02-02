# -*- coding: utf-8 -*-
"""

-------------------------------------------------
   File Name：        calc_pi
   Description :
   Author :           何友鑫
   Create date：      2021-02-02
   Latest version:    v1.0.0
-------------------------------------------------
   Change Log:
#-----------------------------------------------#
    v1.0.0            hyx        2021-02-02
    1.
#-----------------------------------------------#
-------------------------------------------------

"""
import random
import time

def timethis(func):
    def inner():
        start = time.time()
        print('start timer:')
        result = func()
        end = time.time()
        print('end timer:%fs.'%(end-start))
        return result
    return inner

@timethis
def calc_pi():
    n = 1000000
    cnt = 0
    for i in range(n):
        x = random.uniform(-1,1)
        y = random.uniform(-1, 1)
        if x**2 + y**2 <=1:
            cnt += 1

    return 4*cnt/n

if __name__ == '__main__':

    calc_pi()