# -*- coding: utf-8 -*-
"""
Created on Thu Sep 20 22:28:39 2018

@author: JessicaGAO
"""
import pandas as pd
import numpy as np
import statsmodels.api as sm
X=pd.read_excel('0_X.xlsx')

y=pd.read_excel('0_y.xlsx')

LR = sm.Logit(y, X).fit()

#data = pd.concat([y,X],axis=1)
#train_cols = data.columns[1:]

#data1=data.iloc[:1000,]
logit = sm.Logit(y,X)


#拟合参数
result = logit.fit()
