# -*- coding: utf-8 -*-
"""
Created on Mon Jul 16 17:43:59 2018

@author: 何友鑫
latest version: V1.2.0

change log:
    
v1.2.0  hyx    2018.7.30:
-----------------------
1.预测模型较为稳定，只需要改变因子
-----------------------

v1.1.0  hyx    2018.7.17:
-----------------------
1.定性指标 company_type  industry  province  underwriter WOE转换后入模
2.缺失值用'missing'替换
-----------------------
    
v1.0.0  hyx    2018.7.17:
-----------------------
1.用第一版数据，包括宏观、行业、财务，用过采样的方法，做违约预测。  recall:60%  f1:60%   precision:40%   auc:80%+ 
2.分别用随机森林，逻辑回归，SVM， 随机森林效果最好   recall 94%+    pre 80%    f1 89%  auc 97%
-----------------------



"""


from imblearn.over_sampling import ADASYN 
import pandas as pd
import sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn import linear_model
from sklearn.metrics import classification_report
from sklearn import metrics
import numpy as np
from sklearn import svm
from sklearn.preprocessing import OneHotEncoder



'''
Already=pd.read_excel("data/Already_Data_Original_0716.xlsx")
Default=pd.read_excel("data/Default_Data_Original_0716.xlsx")

Already['is_default']=0
Default['is_default']=1      

data=pd.concat([Already,Default])
'''



#data=pd.read_excel("data/All_data_Original_0716.xlsx")
data=pd.read_excel("data/All_data_0723_2.xlsx")
#data.to_csv("final_All_Data_0719_2.csv")
data.loc[data['listed']=='是','listed']=1
data.loc[data['listed']=='否','listed']=0
'''
data=data.fillna('missing')

company_woe_table=calIV_factor(data,'company_type','is_default')
woe_company=pd.crosstab(data['company_type'],data['is_default'])
woe_company['Good']=woe_company.ix[:,0]
woe_company['Bad']=woe_company.ix[:,1]
woe_company['N']=woe_company['Good']+woe_company['Bad']
woe_company['Good_pct']=woe_company['Good']/woe_company['N']
woe_company['Bad_pct']=woe_company['Bad']/woe_company['N']

woe_company=woe_company.sort_index(by='Good_pct',ascending=False)
 
#1.最安全企业  3.最危险企业
data['company_type_seg']='1'
data.loc[data['company_type'].isin(['地方国有企业','中央国有企业']),'company_type_seg']='2'
data.loc[data['company_type'].isin(['公众企业','集体企业','外商独资企业','民营企业','中外合资企业']),'company_type_seg']='3'

woe_company_seg=calIV_factor(data,"company_type_seg","is_default")
woe_company_seg['company_type_seg']=woe_company_seg.index
woe_company_seg=woe_company_seg.rename(columns={'woe':'company_woe'})          
woe_company_new=woe_company_seg.loc[:,['company_type_seg','company_woe']]
        

data=pd.merge(data,woe_company_new,how='left')
'''
#data=data.loc[:,['CPI','ChinaNewsBasedEPU','GDP','alpha','belta','belta_yj','belta_yz','consumption','creditspread','finance_1','finance_2','finance_3','finance_4','finance_5','finance_6','finance_7','finance_8','finance_9','finance_10','finance_11','finance_12','finance_13','finance_14','finance_15','listed','is_default']].dropna()

data=data.loc[:,['CPI','ChinaNewsBasedEPU','GDP','alpha','belta','belta_yj','belta_yz','consumption','creditspread','finance_1','finance_2','finance_3','finance_4','finance_5','finance_6','finance_7','finance_8','finance_9','finance_10','finance_11','finance_12','finance_13','finance_14','finance_15','listed','company_type','exchange','industry','province','is_default']].dropna()

data=pd.get_dummies(data)


        
data_not_default=data[data['is_default']==0]
data_default=data[data['is_default']==1]





l_recall=[]
l_acc=[]
l_pre=[]
l_auc=[]
l_f1=[]
for i in range(1,50):
    
    #i=3
    X_Ndefault=data_not_default.loc[:,['CPI','ChinaNewsBasedEPU','GDP','alpha','belta','belta_yj','belta_yz','consumption','creditspread','finance_1','finance_2','finance_3','finance_4','finance_5','finance_6','finance_7','finance_8','finance_9','finance_10','finance_11','finance_12','finance_13','finance_14','finance_15','listed']]
    y_Ndefault=data_not_default.loc[:,'is_default']
    X_Ndefault_train,X_Ndefault_test,y_Ndefault_train,y_Ndefault_test=train_test_split(X_Ndefault,y_Ndefault,test_size=0.25,random_state=i)
    
    X_default=data_default.loc[:,['CPI','ChinaNewsBasedEPU','GDP','alpha','belta','belta_yj','belta_yz','consumption','creditspread','finance_1','finance_2','finance_3','finance_4','finance_5','finance_6','finance_7','finance_8','finance_9','finance_10','finance_11','finance_12','finance_13','finance_14','finance_15','listed']]
    y_default=data_default.loc[:,'is_default']
    X_default_train,X_default_test,y_default_train,y_default_test=train_test_split(X_default,y_default,test_size=0.25,random_state=i)
    
    X_train=pd.concat([X_Ndefault_train,X_default_train])
    y_train=pd.concat([y_Ndefault_train,y_default_train])
    
    
    X_test=pd.concat([X_Ndefault_test,X_default_test])
    y_test=pd.concat([y_Ndefault_test,y_default_test])
    
    '''
    X_train=X_train.dropna(axis=1,how='all')
    y_train=y_train.dropna(axis=1,how='all')
    
    X_test=X_test.dropna(axis=1,how='all')
    y_test=y_test.dropna(axis=1,how='all')
    
    a=X_train[X_train.isnull().values==True]
    '''
    
    ada = ADASYN(random_state=i,ratio=5/20)
    X_syn,y_syn=ada.fit_sample(X_train,y_train)
    
    
    #logistic = linear_model.LogisticRegressionCV(penalty='l1',solver='liblinear')
    
    #logistic = linear_model.LogisticRegressionCV()
    #y_predit = logistic.fit(X_syn, y_syn).predict(X_test)
    RFC = RandomForestClassifier( max_depth=8,random_state=i)
    y_predit = RFC.fit(X_syn, y_syn).predict(X_test)
  
    #SVM=svm.SVC()
    #y_predit =SVM.fit(X_syn,y_syn).predict(X_test)
    
    #print(classification_report(y_test,y_predit))
    #np.array(l_f1).mean()
    l_recall.append(metrics.recall_score(y_test,y_predit))
    l_acc.append(metrics.accuracy_score(y_test,y_predit))
    l_pre.append(metrics.average_precision_score(y_test,y_predit))
    l_f1.append(metrics.f1_score(y_test, y_predit))
    l_auc.append(metrics.roc_auc_score(y_test, y_predit))

np.array(l_recall).mean()
np.array(l_acc).mean()
np.array(l_pre).mean()
np.array(l_f1).mean()
np.array(l_auc).mean()

from sklearn.metrics import confusion_matrix
confusion_matrix(y_test,y_predit)


## RFC


'''
data=pd.read_excel("data/All_data_Original_0717_2.xlsx")
data.loc[data['listed']=='是','listed']=1
data.loc[data['listed']=='否','listed']=0
      


#data=pd.DataFrame(data,columns=['bond_type_wind_1','bond_type_wind_2','company_type'])
data=data.loc[:,['CPI','ChinaNewsBasedEPU','GDP','alpha','belta','belta_yj','belta_yz','consumption','creditspread','finance_1','finance_2','finance_3','finance_4','finance_5','finance_6','finance_7','finance_8','finance_9','finance_10','finance_11','finance_12','finance_13','finance_14','finance_15','listed','bond_type_wind_1','company_type','exchange','industry','province','is_default']].dropna()


label = sklearn.preprocessing.LabelEncoder()
data['industry'] =  label.fit_transform(data['industry'])
data['bond_type_wind_1']= label.fit_transform(data['bond_type_wind_1'])

data['company_type'] =  label.fit_transform(data['company_type'])
data['exchange']= label.fit_transform(data['exchange'])

data['province'] =  label.fit_transform(data['province'])
  
        
        
data_not_default=data[data['is_default']==0]
data_default=data[data['is_default']==1]        


X_Ndefault=data_not_default.loc[:,['CPI','ChinaNewsBasedEPU','GDP','alpha','belta','belta_yj','belta_yz','consumption','creditspread','finance_1','finance_2','finance_3','finance_4','finance_5','finance_6','finance_7','finance_8','finance_9','finance_10','finance_11','finance_12','finance_13','finance_14','finance_15','listed','bond_type_wind_1','company_type','exchange','industry','province']]
y_Ndefault=data_not_default.loc[:,'is_default']
X_Ndefault_train,X_Ndefault_test,y_Ndefault_train,y_Ndefault_test=train_test_split(X_Ndefault,y_Ndefault,test_size=0.25,random_state=0)

X_default=data_default.loc[:,['CPI','ChinaNewsBasedEPU','GDP','alpha','belta','belta_yj','belta_yz','consumption','creditspread','finance_1','finance_2','finance_3','finance_4','finance_5','finance_6','finance_7','finance_8','finance_9','finance_10','finance_11','finance_12','finance_13','finance_14','finance_15','listed','bond_type_wind_1','company_type','exchange','industry','province']]
y_default=data_default.loc[:,'is_default']
X_default_train,X_default_test,y_default_train,y_default_test=train_test_split(X_default,y_default,test_size=0.25,random_state=0)


#X_Ndefault=data_not_default.drop('is_default',1)

X_train=pd.concat([X_Ndefault_train,X_default_train])
y_train=pd.concat([y_Ndefault_train,y_default_train])


X_test=pd.concat([X_Ndefault_test,X_default_test])
y_test=pd.concat([y_Ndefault_test,y_default_test])



  

ada = ADASYN(random_state=0,ratio=5/20)
X_syn,y_syn=ada.fit_sample(X_train,y_train)





RFC = RandomForestClassifier(max_depth=8, random_state=0)

yy = RFC.fit(X_syn, y_syn).predict(X_test)
importance= pd.DataFrame(RFC.feature_importances_,columns=['Feature Importance'])
importance.index = X_test.columns
importance.sort_values('Feature Importance',ascending=True)[len(X_test.columns)-10:len(X_test.columns)].plot.barh(figsize=(8,16))
'''