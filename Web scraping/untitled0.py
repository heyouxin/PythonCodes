# -*- coding: utf-8 -*-
"""
Created on Mon Jan  8 11:20:49 2018

@author: 何友鑫
"""

import pandas as pd

data=pd.read_excel('副本开学初问卷.xls',sheetname='Sheet2')
data.strip()


data['姓名.1']=data['姓名.1'].str.strip(' ')
data.to_excel('test.xls')

