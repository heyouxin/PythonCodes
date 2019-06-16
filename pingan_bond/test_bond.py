# -*- coding: utf-8 -*-
"""

-------------------------------------------------
   File Name：        test_bond
   Description :
   Author :           何友鑫
   date：             2018-09-03
   latest version:    v1.0.0
-------------------------------------------------
   Change Log:
    v1.0.0            hyx        2018-09-03
    1.
-------------------------------------------------

"""
import pandas as pd
import numpy as np

test_bond=pd.read_csv('112(1).csv',encoding='gbk')

already_bond=pd.read_excel('data/Already_quarter_0807_1.xlsx')
already_bond.columns
default_bond=pd.read_excel('data/Default_quarter_0807_1.xlsx')
default_bond.industry_wind=='能源'
#default_bond['date_default']
test_bond_yongtai=test_bond[test_bond['issuer']=='永泰能源股份有限公司']
test_bond_yongtai.columns

test_bond_dunan=test_bond[test_bond['issuer']=='浙江盾安人工环境股份有限公司']
test_bond_dunan.columns


#default
Index(['code', 'time_report', 'finance_1', 'finance_2', 'finance_3',
       'finance_4', 'finance_5', 'finance_6', 'finance_7', 'finance_8',
       'finance_9', 'finance_10', 'finance_11', 'finance_12', 'finance_13',
       'finance_14', 'finance_15', 'name', 'date_default', 'event', 'issuer',
       'rate_history', 'balance_100million', 'coupon_rate', 'company_type',
       'date_start', 'date_end', 'listed', 'industry_wind', 'industry',
       'total_100million', 'year', 'bond_type_wind_1', 'alpha', 'belta',
       'belta_yj', 'belta_yz', 'bond_type_wind_2', 'underwriter', 'sponsor',
       'province', 'rate_comp_issue', 'rate_bond_issue', 'rate_bond_lastest',
       'rate_comp_lastest', 'exchange', 'consumption', 'interest_rate', 'CPI',
       'GDP_growth', 'ChinaNewsBasedEPU'],
      dtype='object')

yongtai_default_date=pd.read_excel('违约债券报表1.xlsx')
yongtai_default_date=yongtai_default_date[['代码','发生日期']]
yongtai_default_date=yongtai_default_date.rename(columns={'代码':'code','发生日期':'date_default'})
test_bond_yongtai2=pd.merge(test_bond_yongtai,yongtai_default_date,on='code',how='inner')

#column name
test_bond_yongtai2['event']=''
test_bond_yongtai2['rate_history']=''
test_bond_yongtai2['rate_bond_lastest']=''
test_bond_yongtai2['rate_comp_lastest']=''
test_bond_yongtai2['interest_rate']=0.0


test_bond_yongtai2['balance_100million']=0.0
test_bond_yongtai2['province']='山西省'
test_bond_yongtai2['listed']=1
test_bond_yongtai2['industry_wind']='煤炭与消费用燃料'
test_bond_yongtai2['bond_type_wind_2']=''

test_bond_yongtai2=test_bond_yongtai2[['code', 'time_report', 'finance_1', 'finance_2', 'finance_3',
       'finance_4', 'finance_5', 'finance_6', 'finance_7', 'finance_8',
       'finance_9', 'finance_10', 'finance_11', 'finance_12', 'finance_13',
       'finance_14', 'finance_15', 'name', 'date_default', 'event', 'issuer',
       'rate_history', 'balance_100million', 'coupon_rate', 'company_type',
       'date_start', 'date_end', 'listed', 'industry_wind', 'industry',
       'total_100million', 'year', 'bond_type_wind_1', 'alpha', 'belta',
       'belta_yj', 'belta_yz', 'bond_type_wind_2', 'underwriter', 'sponsor',
       'province', 'rate_comp_issue', 'rate_bond_issue', 'rate_bond_lastest',
       'rate_comp_lastest', 'exchange', 'consumption', 'interest_rate', 'CPI',
       'GDP_growth', 'ChinaNewsBasedEPU']]

default_bond_0903=pd.concat([default_bond,test_bond_yongtai2])

default_bond_0903.to_excel('default_bond_0903.xlsx',index=False,encoding='utf8')



test_bond_dunan['event']=''
test_bond_dunan['rate_history']=''
test_bond_dunan['rate_bond_lastest']=''
test_bond_dunan['rate_comp_lastest']=''
test_bond_dunan['interest_rate']=0.0


test_bond_dunan['balance_100million']=0.0
test_bond_dunan['province']='浙江省'
test_bond_dunan['listed']=1
test_bond_dunan['industry_wind']=test_bond_dunan['industry']
test_bond_dunan['bond_type_wind_2']=''


test_bond_dunan2=test_bond_dunan[['code', 'bond_type_wind_1', 'company_type', 'coupon_rate', 'date_end',
       'date_start', 'finance_1', 'finance_10', 'finance_11', 'finance_12',
       'finance_13', 'finance_14', 'finance_15', 'finance_2', 'finance_3',
       'finance_4', 'finance_5', 'finance_6', 'finance_7', 'finance_8',
       'finance_9', 'industry', 'issuer', 'listed', 'name', 'time_report',
       'total_100million', 'year', 'alpha', 'belta', 'belta_yj', 'belta_yz',
       'bond_type_wind_2', 'underwriter', 'sponsor', 'province',
       'rate_comp_issue', 'rate_bond_issue', 'rate_bond_lastest',
       'rate_comp_lastest', 'exchange', 'consumption', 'interest_rate', 'CPI',
       'GDP_growth', 'ChinaNewsBasedEPU']]

already_bond_0903=pd.concat([already_bond,test_bond_dunan2])
already_bond_0903.to_excel('already_bond_0903.xlsx',index=False,encoding='utf8')
'''
Index(['code', 'time_report', 'finance_2', 'finance_3', 'finance_5',
       'finance_4', 'finance_7', 'finance_8', 'finance_9', 'finance_14',
       'finance_13', 'finance_15', 'finance_12', 'finance_1', 'finance_6',
       'finance_11', 'finance_10', 'company_type', 'name', 'total_100million',
       'balance_100million', 'year', 'coupon_rate', 'issuer',
       'bond_type_wind_1', 'sponsor', 'rate_bond_issue', 'date_start',
       'date_end', 'underwriter', 'rate_comp_issue', 'industry', 'exchange',
       'underwriter.1', 'rate_comp_issue.1', 'GDP_growth', 'ChinaNewsBasedEPU',
       'CPI', 'interest_rate', 'consumption', 'alpha', 'belta', 'belta_yj',
       'belta_yz'],
      dtype='object')


'''
#already
Index(['code', 'bond_type_wind_1', 'company_type', 'coupon_rate', 'date_end',
       'date_start', 'finance_1', 'finance_10', 'finance_11', 'finance_12',
       'finance_13', 'finance_14', 'finance_15', 'finance_2', 'finance_3',
       'finance_4', 'finance_5', 'finance_6', 'finance_7', 'finance_8',
       'finance_9', 'industry', 'issuer', 'listed', 'name', 'time_report',
       'total_100million', 'year', 'alpha', 'belta', 'belta_yj', 'belta_yz',
       'bond_type_wind_2', 'underwriter', 'sponsor', 'province',
       'rate_comp_issue', 'rate_bond_issue', 'rate_bond_lastest',
       'rate_comp_lastest', 'exchange', 'consumption', 'interest_rate', 'CPI',
       'GDP_growth', 'ChinaNewsBasedEPU'],
      dtype='object')


#dunan


'''
