#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 13 12:15:36 2018

@author: macbook
"""
from __future__ import division
from collections import Counter
from imblearn.over_sampling import ADASYN 
import pandas as pd
import seaborn
'''
X, y = make_classification(n_classes=2, class_sep=2,
weights=[0.1, 0.9], n_informative=3, n_redundant=1, flip_y=0,
n_features=20, n_clusters_per_class=1, n_samples=1000,
random_state=10)
ada = ADASYN(random_state=42,ratio=0.15)
X_res, y_res = ada.fit_sample(X, y)
print X_res.shape,X.shape

'''
import sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics
data = pd.read_csv('/Users/macbook/Desktop/test-2.csv',encoding='gb18030')
data = data[data['industry_name']!=u'金融业'].replace(np.inf,0)
y = data['default']
del data['Unnamed: 0']
del data['industry_name']
del data['fcfcoo_mean']
del data['oiadpsale_mean']
del data['fcfcoo_change']
del data['oiadpsale_mean_change']
del data['default']
kk = data
names = data.columns
data = sklearn.preprocessing.Imputer().fit_transform(data)
x= data[:,:]
print x.shape
res1 = []
for i in range(1,20):
    res11= []
    ada = ADASYN(random_state=42,ratio=i/20)
    x_res, y_res = ada.fit_sample(x, y)
    x_train, x_test, y_train, y_test = train_test_split(
     x_res, y_res, test_size=0.2, random_state=42)
    clf = RandomForestClassifier(max_depth=8, random_state=0)
    yy = clf.fit(x_train, y_train).predict(x_test)

    res11.append(metrics.recall_score(y_test,yy))
    res11.append(metrics.accuracy_score(y_test,yy))
    res11.append(metrics.average_precision_score(y_test,yy))
    res11.append(metrics.roc_auc_score(y_test, yy))
    res1.append(res11)
res1 = pd.DataFrame(res1,columns=['recall','accuracy','precision','auc'])
res1.index = (pd.Series(range(1,20))+1)/20
#res1.plot()
#plt.xlabel("Oversampling Size")
#plt.title("Oversampling with RandomForest")
#plt.show()
importance= pd.DataFrame(clf.feature_importances_,columns=['Feature Importance'])
importance.index = names
importance.sort_values('Feature Importance',ascending=False)[:30].plot.barh(figsize=(8,16))
#plt.xlabel("Relative Importance")
#plt.show()

#fcfcoo_mean
#oiadpsale_mean
#fcfcoo_change
#oiadpsale_mean_change
res1.to_csv("/Users/macbook/Desktop/res1.csv")    
ax1 = plt.subplot(121)
res1.plot()
plt.xlabel("Oversampling Size")
plt.title("Oversampling with Random Forest")
plt.subplot(122)
res1.plot()
plt.xlabel("Oversampling Size")
plt.title("Oversampling with Pennalized Logostic")
plt.show()


'''


res2 = []
for i in range(1,10):
    print i/10
    res22= []
    ada = ADASYN(random_state=42,ratio=i/10)
    x_res, y_res = ada.fit_sample(x, y)
    x_train, x_test, y_train, y_test = train_test_split(
     x_res, y_res, test_size=0.2, random_state=42)
    gbdt = sklearn.ensemble.GradientBoostingClassifier(subsample=0.8)
    yy = gbdt.fit(x_train, y_train).predict(x_test)
    res22.append(metrics.recall_score(y_test,yy))
    res22.append(metrics.accuracy_score(y_test,yy))
    res22.append(metrics.average_precision_score(y_test,yy))
    res22.append(metrics.roc_auc_score(y_test, yy))
    res2.append(res11)
res2 = pd.DataFrame(res2,columns=['recall','accuracy','precision','auc'])
res2.index = (pd.Series(range(1,40))+1)/40

'''