# -*- coding: utf-8 -*-
"""
Created on Fri May 26 13:45:06 2017

@author: 何友鑫
"""

import math as m


NPV=-20+10*(1-m.pow(1/1.26,9))/0.26+20/m.pow(1.26,10)
print (NPV)


import sympy as s
from sympy import isympy
r1=s.solve((1-m.pow(1/(1+r),9))/r+2/m.pow(1/(1+r),10)-2,r)
0.1*0.25*0.45+0.3*0.05*0.15+0.4*0.05*0.05+0.2*0.1*0.35