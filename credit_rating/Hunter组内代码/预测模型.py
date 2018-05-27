#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 13 00:04:24 2018

@author: macbook
"""
from __future__ import division
import pandas as pd
import numpy as np
import statsmodels.api as sm
data = pd.read_csv('/Users/macbook/Desktop/test-2.csv',encoding='gb2312')
test = data[data['industry_name']!=u'金融业']
test = test.replace(np.inf,np.nan).replace(-np.inf,np.nan)
del test['Unnamed: 0']
import statsmodels.api as sm
y = np.array(test['default'])
x = test.T[1:-1].T
from sklearn.preprocessing import Imputer
trans = Imputer(missing_values='NaN', strategy='mean', axis=0)
xs = trans.fit_transform(x)

from sklearn.preprocessing import StandardScaler
import sklearn
scaler = StandardScaler()
#x = scaler.fit_transform(x)
from sklearn import linear_model
model = linear_model.LogisticRegression(C=0.2, penalty='l1', tol=0.01)
models = model.fit(xs,y)

from sklearn import *
from sklearn.model_selection import train_test_split

kk =GradientBoostingClassifier(max_depth=5,subsample=0.8).fit(xs.T[:32].T,y)
print sklearn.metrics.precision_score(y,kk.predict(xs.T[:32].T))
print sklearn.metrics.f1_score(y,kk.predict(xs.T[:32].T))
kk =GradientBoostingClassifier(max_depth=5,subsample=0.8).fit(xs.T[:].T,y)
print sklearn.metrics.recall_score(y,kk.predict(xs.T[:].T))
print sklearn.metrics.f1_score(y,kk.predict(xs.T[:].T))

'''
kk =RandomForestClassifier().fit(xs.T[:32].T,y)
print sklearn.metrics.recall_score(y,kk.predict(xs.T[:32].T))
print sklearn.metrics.f1_score(y,kk.predict(xs.T[:32].T))
kk =RandomForestClassifier().fit(xs.T[:].T,y)
print sklearn.metrics.recall_score(y,kk.predict(xs.T[:].T))
print sklearn.metrics.f1_score(y,kk.predict(xs.T[:].T))
'''
res = []
for i in range(1000): 
    x_train, x_test, y_train, y_test = train_test_split(
     xs,y,test_size=0.1, random_state=0)
    kk =GradientBoostingClassifier(max_depth=5,subsample=0.8).fit(x_train,y_train)
    res.append(sklearn.metrics.f1_score(y_test,kk.predict(x_test)))
    #print sklearn.metrics.precision_score(y_test,kk.predict(x_test)),sklearn.metrics.recall_score(y_test,kk.predict(x_test))



'''
for i in range(1,10):
    c = i/10
    model = linear_model.LogisticRegression(class_weight='balanced',C=i, penalty='l1', 
                                            tol=0.01)
    models = model.fit(xs,y)
    print models.coef_
    print c,models.score(xs,y),sklearn.metrics.recall_score(y,models.predict(xs))
'''    

'''
model = linear_model.LogisticRegression(class_weight='balanced',C=0.7, penalty='l2', 
                                            tol=0.01)
models = model.fit(xs.T[:32].T,y)
print sklearn.metrics.precision_score(y,models.predict(xs.T[:32].T))
print sklearn.metrics.recall_score(y,models.predict(xs.T[:32].T))
print sklearn.metrics.f1_score(y,models.predict(xs.T[:32].T))
model = linear_model.LogisticRegression(class_weight='balanced',C=0.7, penalty='l2', 
                                            tol=0.01)
models = model.fit(xs,y)
print sklearn.metrics.precision_score(y,models.predict(xs.T[:].T))
print sklearn.metrics.recall_score(y,models.predict(xs.T[:].T))
print sklearn.metrics.f1_score(y,models.predict(xs.T[:].T))
'''



'''
model = sm.Logit(y,xs).fit()
print model.aic
print sm.Logit(y,xs).predict(model.params)


model = sm.Logit(y,xs.T[:32].T).fit()
print model.aic

'''







