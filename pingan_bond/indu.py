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
from WindPy import w 
import statsmodels.api as sm
import numpy as np
w.start()



##HS300
wsd_data=w.wsd("000300.SH", "pct_chg", "2000-01-01", "2018-06-30", "")
HS300_return=pd.DataFrame(wsd_data.Data,index=wsd_data.Fields,columns=wsd_data.Times)
HS300_return=HS300_return.T 
HS300_return=HS300_return.rename(columns={'PCT_CHG':'ret_hs300'})
##SZ50
wsd_data=w.wsd("000016.SH", "close", "2000-01-01", "2018-06-30", "")
SZ50_close=pd.DataFrame(wsd_data.Data,index=wsd_data.Fields,columns=wsd_data.Times)
SZ50_close=SZ50_close.T

##万得一级行业分类
indust_table=pd.DataFrame()
for i in range(1,12):
    indu_name="88200"+str(i)+".WI"
    if (i>9):
        indu_name="8820"+str(i)+".WI"
    wsd_data=w.wsd(indu_name, "close,pct_chg,sec_name", "2000-01-01", "2018-06-30", "")
    temp=pd.DataFrame(wsd_data.Data,index=wsd_data.Fields,columns=wsd_data.Times)
    temp=temp.T
    temp['Codes']=wsd_data.Codes[0]
    indust_table=pd.concat([indust_table,temp],axis=0)
indust_table=indust_table.rename(columns={'PCT_CHG':'ret'})


##无风险利率  SHIBOR3M
wsd_data=w.wsd("SHIBOR3M.IR", "close", "2000-01-01", "2018-06-30", "")
SHIBOR3M=pd.DataFrame(wsd_data.Data,index=wsd_data.Fields,columns=wsd_data.Times)
SHIBOR3M=SHIBOR3M.T
SHIBOR3M=SHIBOR3M.rename(columns={'CLOSE':'rf'})

## 构造 Rm-Rf  Ri-Rf
Rm_Rf=pd.concat([HS300_return,SHIBOR3M],axis=1)
Rm_Rf['Rm_Rf']=Rm_Rf['ret_hs300']-Rm_Rf['rf']
indust_table=pd.concat([indust_table,SHIBOR3M],axis=1,join_axes=[indust_table.index])
indust_table['Ri_Rf']=indust_table['ret']-indust_table['rf']
indust_table=pd.concat([indust_table,Rm_Rf['Rm_Rf']],axis=1,join_axes=[indust_table.index])

## 分行业做CAPM回归
indust_table2=indust_table.dropna()
group_by_name=indust_table2.groupby('SEC_NAME')
l_name=[]
l_alpha=[]
l_belta=[]
##OLS
for name,group in group_by_name:
    fit=sm.OLS(np.array(group['Ri_Rf']),sm.add_constant(np.array(group['Rm_Rf']))).fit()
    l_name.append(name)
    l_alpha.append(fit.params[0])
    l_belta.append(fit.params[1])
alpha_belta={"indust_name":l_name,"alpha":l_alpha,"belta":l_belta}
alpha_belta=pd.DataFrame(alpha_belta)
'''
#       M=sm.robust.norms.HuberT() 有报错 'float' object has no attribute 'fabs'
for name,group in group_by_name:
    fit=sm.RLM(np.array(group['Ri_Rf']),sm.add_constant(np.array(group['Rm_Rf'])),M=sm.robust.norms.HuberT()).fit()
    l_name.append(name)
    l_alpha.append(fit.params[0])
    l_belta.append(fit.params[1])
alpha_belta={"indust_name":l_name,"alpha":l_alpha,"belta":l_belta}
alpha_belta=pd.DataFrame(alpha_belta)
'''
##债券
'''
wsd_data=w.wsd("1180016.IB", "term,couponrate,amount", "2000-01-01", "2018-06-30", "")
wsd_data=w.wsd("1180016.IB", "amount", "2000-01-01", "2018-06-30", "")
amount=pd.DataFrame(wsd_data.Data,index=wsd_data.Fields,columns=wsd_data.Times)
amount=IB.T
'''

# Uncertainty Beta 
# 预警指数
wsd_data=w.edb("M0041339", "2000-01-01", "2018-06-30","Fill=Previous")
yj_index=pd.DataFrame(wsd_data.Data,index=wsd_data.Fields,columns=wsd_data.Times)
yj_index=yj_index.T 
yj_index=yj_index.rename(columns={'CLOSE':'yj_index'})

# 一致指数
wsd_data=w.edb("M0041340", "2000-01-01", "2018-06-30","Fill=Previous")
yz_index=pd.DataFrame(wsd_data.Data,index=wsd_data.Fields,columns=wsd_data.Times)
yz_index=yz_index.T 
yz_index=yz_index.rename(columns={'CLOSE':'yz_index'})


## 行业指数月度回报
indust_m=pd.DataFrame()
for i in range(1,12):
    indu_name="88200"+str(i)+".WI"
    if (i>9):
        indu_name="8820"+str(i)+".WI"
    wsd_data=w.wsd(indu_name, "sec_name,pct_chg", "2000-01-01", "2018-06-30", "Period=M;Days=Alldays")
    temp=pd.DataFrame(wsd_data.Data,index=wsd_data.Fields,columns=wsd_data.Times)
    temp=temp.T
    temp['Codes']=wsd_data.Codes[0]
    indust_m=pd.concat([indust_m,temp],axis=0)
indust_m=indust_m.rename(columns={'PCT_CHG':'ret'})
indust_m=pd.concat([indust_m,yj_index,yz_index],axis=1,join_axes=[indust_m.index])
indust_m=indust_m.dropna()


indust_table.to_excel("行业CAPM.xlsx")
indust_m.to_excel("行业uncertainty_beta.xlsx")


## 分行业 每20个月一个周期回归一次，取平均
l_name = []
l_yj=[]
l_yz=[]
group_by_name=indust_m.groupby('SEC_NAME')
for name,group in group_by_name:  
    belta_yj=[]
    belta_yz=[]
    for j in range(21,len(group)):
        model = sm.OLS(np.array(group.ret[j-20:j]),sm.add_constant(np.array(group.yj_index[j-20:j]))).fit()
        belta_yj.append(model.params[1])
        
        model = sm.OLS(np.array(group.ret[j-20:j]),sm.add_constant(np.array(group.yz_index[j-20:j]))).fit()
        belta_yz.append(model.params[1])
        
    l_name.append(name)
    l_yj.append(np.array(belta_yj).mean())
    l_yz.append(np.array(belta_yz).mean())
beltas={"indust_name":l_name,"belta_yj":l_yj,"belta_yz":l_yz}
beltas=pd.DataFrame(beltas)


alpha_belta.to_excel("CAPM_alpha_belta.xlsx")
beltas.to_excel("uncertainty_belta.xlsx")


wsd_data=w.wsd("122683.SH", "current,quick,tltoebitda,netdebttoev,cashtocurrentdebt", "2005-02-01", "2018-07-10", "Period=M")
bond=pd.DataFrame(wsd_data.Data,index=wsd_data.Fields,columns=wsd_data.Times)
bond=bond.T 
bond=bond.rename(columns={'PCT_CHG':'ret_hs300'})