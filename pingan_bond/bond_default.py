# -*- coding: utf-8 -*-
"""
Created on Tue Jul 10 17:49:16 2018

@author: 何友鑫
"""

import h2o

import pandas as pd

import numpy as np



default_bond=pd.read_excel("违约债券报表.xlsx")

default_bond=default_bond.loc[:182,:]

group_by_indu=default_bond.groupby('所属wind行业')

print(1+1)
print('a')
for indu,group in group_by_indu:
    print(indu)
    print(len(group)/183)