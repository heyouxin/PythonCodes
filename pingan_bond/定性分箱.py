
#data=pd.read_excel("data/All_data_Original_0716.xlsx")
data=pd.read_excel("data/All_data_Original_0717_2.xlsx")
data.loc[data['listed']=='是','listed']=1
data.loc[data['listed']=='否','listed']=0

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
        

data=pd.merge(data,woe_company_new,how='left')# -*- coding: utf-8 -*-
"""
Created on Wed Jul 18 11:18:45 2018

@author: 何友鑫
"""

