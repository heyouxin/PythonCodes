# -*- coding: utf-8 -*-
"""
Created on Sat Jun 30 14:53:21 2018

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



#不可能用原始样本调C
#X_train_1, X_test_1, y_train_1, y_test_1 = train_test_split(X, y, test_size=0.25, random_state=42)
#原始样本的表现

def raw_model(X,y):
    logistic = linear_model.LogisticRegressionCV()
    auc = cross_val_score(logistic, X, y, cv=5, scoring='roc_auc').mean()
    acc = cross_val_score(logistic, X, y, cv=5, scoring='accuracy').mean()
    recall = cross_val_score(logistic, X, y, cv=5, scoring='recall').mean()
    return (auc,acc,recall)
#fit.scores_
#logistic = linear_model.LogisticRegression(C=1/10000, penalty='l1', tol=0.01)

def ada_model(X,y,names):
    ada = ADASYN(random_state=42)
    X_syn,y_syn=ada.fit_sample(X,y)
#X_train, X_test, y_train, y_test = train_test_split(X_syn, y_syn, test_size=0.25, random_state=1)
#logistic = linear_model.LogisticRegressionCV()
#yy = logistic.fit(X_train, y_train).predict(X_test)
    logistic = linear_model.LogisticRegressionCV(penalty='l1',solver='liblinear')
    #logistic = linear_model.LogisticRegression(C=1000,penalty='l1')
    auc = cross_val_score(logistic, X_syn, y_syn, cv=5, scoring='roc_auc').mean()
    acc = cross_val_score(logistic, X_syn, y_syn, cv=5, scoring='accuracy').mean()
    recall = cross_val_score(logistic, X_syn, y_syn, cv=5, scoring='recall').mean()
    print("cross validation results:")
    print("-------------------------")
    print("auc：",auc)
    print("acc：",acc)
    print("recall：",recall)
    
    X_train, X_test, y_train, y_test = train_test_split(X_syn, y_syn, test_size=0.25, random_state=1)
    print(logistic.fit(X_train, y_train).coef_)
    
    RFC = RandomForestClassifier(max_depth=8, random_state=0)
    yy = RFC.fit(X_train, y_train).predict(X_test)
    importance= pd.DataFrame(RFC.feature_importances_,columns=['Feature Importance'])
    importance.index = names
    importance.sort_values('Feature Importance',ascending=True)[len(names)-10:len(names)].plot.barh(figsize=(8,16))



  
'''
#选不平衡比例
#logistic = linear_model.LogisticRegression(C=0.2, penalty='l1', tol=0.01)
l_scores=[]
for i in range(1,20):
    scores= []
    ada = ADASYN(random_state=42,ratio=i/20)
    X_syn,y_syn=ada.fit_sample(X,y)
 
    X_train, X_test, y_train, y_test = train_test_split(X_syn, y_syn, test_size=0.25, random_state=42)
    #clf = RandomForestClassifier(max_depth=8, random_state=0)
    yy = logistic.fit(X_train, y_train).predict(X_test)
 
    scores.append(metrics.recall_score(y_test,yy))
    scores.append(metrics.accuracy_score(y_test,yy))
    scores.append(metrics.average_precision_score(y_test,yy))
    scores.append(metrics.roc_auc_score(y_test, yy))
    l_scores.append(scores)
   
l_scores = pd.DataFrame(l_scores,columns=['recall','accuracy','precision','auc'])
l_scores.index = (pd.Series(range(1,20))+1)/20    
l_scores.plot()
plt.xlabel("Oversampling Size")
plt.title("Oversampling with Pennalized Logostic") 
'''
if __name__ == "__main__":
    data = pd.read_csv('test-2.csv',encoding='gbk')
    #无穷大替换为缺失值
    data = data[data['industry_name']!='金融业'].replace(np.inf,np.nan).replace(-np.inf,np.nan)
    data = data.dropna()
    y = np.array(data['default'])
    del data['Unnamed: 0']
    del data['industry_name']
    del data['default']
    X = data
    #只含财务指标的特征空间 x_fin
    X_fin = data.iloc[:,0:32]
    names = data.columns
    names_fin = X_fin.columns
    #预处理
    X = sklearn.preprocessing.Imputer().fit_transform(X)
    X_fin = sklearn.preprocessing.Imputer().fit_transform(X_fin)
    
    ada_model(X,y,names)
    #ada_model(X_fin,y,names_fin)

