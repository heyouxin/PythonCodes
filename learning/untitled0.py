# -*- coding: utf-8 -*-
"""
Created on Sun Mar 19 20:08:42 2017

@author: 何友鑫
"""

from sklearn import linear_model
reg = linear_model.LinearRegression()
fit = reg.fit ([[0, 4], [1, 1], [2, 2]], [0, 1, 2])
print (reg.coef_)

print ("hello !")


import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
X = np.array([[-1, -1], [-2, -1], [-3, -2], [1, 1], [2, 1], [3, 2]])
y = np.array([1, 1, 1, 2, 2, 2])
clf = LinearDiscriminantAnalysis()
clf.fit(X, y)
LinearDiscriminantAnalysis(n_components=None, priors=None, shrinkage=None,
              solver='svd', store_covariance=False, tol=0.0001)
print(clf.predict([[-0.8, -10]]))


from sklearn import svm
X = [[0, 0], [1, 1]]
y = [0, 1]
clf = svm.SVC()
clf.fit(X, y)



  