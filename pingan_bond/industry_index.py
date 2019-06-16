# -*- coding: utf-8 -*-
"""
Created on Wed Jul 18 19:44:32 2018

@author: 何友鑫
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 13:36:21 2018

@author: 何友鑫
latest version: V1.0.0

change log:
v1.0.0
-----------------------
1.行业层面数据
2.按行业计算CAPM alpha belta
3.uncertainty belta
-----------------------
"""
import pandas as pd
import statsmodels.api as sm
import numpy as np


indust_table=pd.read_excel("data/行业CAPM.xlsx").dropna()
bond=pd.read_excel("data/短期融资券代码日期行业.xlsx")

bond['SEC_NAME']=bond['industry']+str('指数')




## 分行业做CAPM回归
l_name=[]
l_alpha=[]
l_belta=[]
for i in range(0,len(bond)):
    if bond.loc[i,'SEC_NAME']==np.nan:
        continue
    indust_group=indust_table.loc[indust_table['SEC_NAME']==bond.loc[i,'SEC_NAME']]
    try:
        indust_group=indust_group[(indust_group.index >= bond['time_start'][i]) & (indust_group.index < bond['time_end'][i])]
        fit=sm.OLS(np.array(indust_group['Ri_Rf']),sm.add_constant(np.array(indust_group['Rm_Rf']))).fit()
        
        l_belta.append(fit.params[1])
        l_name.append(bond['code'][i])
        l_alpha.append(fit.params[0])
    except:
        
        l_belta.append(np.nan)
        l_name.append(bond['code'][i])
        l_alpha.append(np.nan)
    
alpha_belta={"code":l_name,"alpha":l_alpha,"belta":l_belta}
alpha_belta=pd.DataFrame(alpha_belta)
alpha_belta.to_excel('CAPM_alhpha_belta_超短期债券.xlsx')



indust_un=pd.read_excel('data/行业uncertainty_beta.xlsx').dropna()
## 分行业 每20个月一个周期回归一次，取平均
l_name = []
l_yj=[]
l_yz=[]


for i in range(0,len(bond)):
    indust_group=indust_un.loc[indust_un['SEC_NAME']==bond.loc[i,'SEC_NAME']]
    group=indust_group[(indust_group.index >= bond['time_start'][i]) & (indust_group.index < bond['time_end'][i])]
    
    belta_yj=[]
    belta_yz=[]
    
    if len(group) <= 20:
        try:
            model=sm.OLS(np.array(group.ret[0:len(group)]),sm.add_constant(np.array(group.yj_index[0:len(group)]))).fit()
            l_yj.append(model.params[1])
        except:
            l_yj.append(np.nan)
        
        try:
            model=sm.OLS(np.array(group.ret[0:len(group)]),sm.add_constant(np.array(group.yz_index[0:len(group)]))).fit()
            l_yz.append(model.params[1])
        except:
            l_yz.append(np.nan)
     
        l_name.append(bond['code'][i])
            
    else:
    
        for j in range(20,len(group)):
            model = sm.OLS(np.array(group.ret[j-20:j]),sm.add_constant(np.array(group.yj_index[j-20:j]))).fit()
            belta_yj.append(model.params[1])
            
            model = sm.OLS(np.array(group.ret[j-20:j]),sm.add_constant(np.array(group.yz_index[j-20:j]))).fit()
            belta_yz.append(model.params[1])
            
        l_name.append(bond['code'][i])
        l_yj.append(np.array(belta_yj).mean())
        l_yz.append(np.array(belta_yz).mean())
beltas={"code":l_name,"belta_yj":l_yj,"belta_yz":l_yz}
beltas=pd.DataFrame(beltas)
beltas.to_excel("uncertainty_belta_超短期债券.xlsx")


