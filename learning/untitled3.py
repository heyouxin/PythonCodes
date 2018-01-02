# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 10:14:24 2017

@author: 何友鑫
"""

import pandas as pd
import numpy as np
file = pd.read_csv('./files/xm.csv',skiprows = 100)
print (file)


### 索引
dates = pd.date_range('1/1/2000', periods=8)
df = pd.DataFrame(np.random.randn(8, 4), index=dates, columns=['A', 'B', 'C', 'D'])
print (df)
print (df['B']['2000-01-02'])

###
print (df['A'].iloc[0:2])

print (df.loc["2000-01-01",'A'])

