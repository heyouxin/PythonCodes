# -*- coding: utf-8 -*-
"""
Created on Thu Jul 12 15:14:23 2018

@author: 何友鑫
"""
from __future__ import division
from collections import Counter
from imblearn.over_sampling import ADASYN 
import pandas as pd
import seaborn

import sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn import datasets
import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model
from sklearn.model_selection import StratifiedKFold
from sklearn.cross_validation import cross_val_score
from woe import Woefordf



df_bond_institu.describe()
data=data.reset_index()
data['default']=data['default'].astype(int)

#计算IV值
def CalcIV(Xvar, Yvar): 
   N_0  = np.sum(Yvar==0)
   N_1 = np.sum(Yvar==1)
   N_0_group = np.zeros(np.unique(Xvar).shape)
   N_1_group = np.zeros(np.unique(Xvar).shape)
   for i in range(len(np.unique(Xvar))):
       N_0_group[i] = Yvar[(Xvar == np.unique(Xvar)[i]) & (Yvar == 0)].count()
       N_1_group[i] = Yvar[(Xvar == np.unique(Xvar)[i]) & (Yvar == 1)].count()
   iv = np.sum((N_0_group/N_0 - N_1_group/N_1) * np.log((N_0_group/N_0)/(N_1_group/N_1)))
   return  iv   


def caliv_batch(df, Kvar, Yvar):
   df_Xvar = df.drop([Kvar, Yvar], axis=1)
   ivlist = []
   for col in df_Xvar.columns:
       iv = CalcIV(df[col], df[Yvar])
       ivlist.append(iv)
   names = list(df_Xvar.columns)
   iv_df = pd.DataFrame({'Var': names, 'Iv': ivlist}, columns=['Var', 'Iv'])

   return iv_df

def calIV(df,var,target):
    eps=0.0000001
    gbi=pd.crosstab(df[var],df[target])+eps
    gb=df[target].value_counts()+eps
    gbri=gbi/gb
    gbri['woe']=np.log(gbri[1]/gbri[0])
    gbri['iv']=(gbri[1]-gbri[0])*gbri['woe']
    return gbri['iv'].sum

data.to_csv("test_data.csv")


IV=calIV(data,'industry_name','default')

#1.计算定性指标IV值
factor_IV=pd.DataFrame()
factor_name=['industry_name']
IV=[]

for fac_var in factor_name:
    
data[0,:]