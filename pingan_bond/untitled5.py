# -*- coding: utf-8 -*-
"""
Created on Fri Jul 13 14:57:05 2018

@author: 何友鑫
"""

import numpy as np
import pandas as pd

data=pd.read_csv("test_data.csv",encoding='gbk')
del data['Unnamed: 0']
del data['index']



#定性指标计算IV值
def calIV_factor(df,var,target):
    eps=0.000001
    gbi=pd.crosstab(df[var],df[target])+eps
    gb=df[target].value_counts()+eps
    gbri=gbi/gb
    gbri['woe']=np.log(gbri[1]/gbri[0])
    gbri['iv']=(gbri[1]-gbri[0])*gbri['woe']
    return gbri

woe_industry2=calIV_factor(data,"industry_name","default")
woe_industry=pd.crosstab(data['industry_name'],data['default'])
woe_industry['Good']=woe_industry.ix[:,0]
woe_industry['Bad']=woe_industry.ix[:,1]
woe_industry['N']=woe_industry['Good']+woe_industry['Bad']
woe_industry['Good_pct']=woe_industry['Good']/woe_industry['N']
woe_industry['Bad_pct']=woe_industry['Bad']/woe_industry['N']

woe_industry=woe_industry.sort_index(by='Good_pct',ascending=False)
 
#1.最安全行业  3.最危险行业
data['industry_seg']='1'
data.loc[data['industry_name'].isin(['综合','电力、热力、燃气及水生产和供应业','交通运输、仓储和邮政业']),'industry_seg']='2'
data.loc[data['industry_name'].isin(['采矿业','建筑业','制造业']),'industry_seg']='3'

woe_industry2=calIV_factor(data,"industry_seg","default")
woe_industry2['industry_seg']=woe_industry2.index
woe_industry2=woe_industry2.rename(columns={'woe':'indust_woe'})          
woe_industry_new=woe_industry2.loc[:,['industry_seg','indust_woe']]


data=pd.merge(data,woe_industry_new,how='left')
