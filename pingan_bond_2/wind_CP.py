# -*- coding: utf-8 -*-
"""

-------------------------------------------------
   File Name：        wind_CP
   Description :
   Author :           何友鑫
   Create date：      2018-09-28
   Latest version:    v1.0.0
-------------------------------------------------
   Change Log:
#-----------------------------------------------#
    v1.0.0            hyx        2018-09-28
    1.下载短期融资融券债券
#-----------------------------------------------#
-------------------------------------------------

"""

import pandas as pd
from sqlalchemy import create_engine
import pymysql
from WindPy import w
w.start()
from datetime import datetime
import re
from sklearn.linear_model.logistic import LogisticRegression
import numpy as np
import math as m

##获取现在已有债券代码表
already_code = pd.read_excel('data_sql/bond_info_1009.xlsx')['code']
already_code = already_code.map(lambda x: str(x).strip())

file_object = open('raw_data/短期融资融券代码.txt')
try:
    company_bond_code = file_object.read()
finally:
    file_object.close()
# 所有公司债代码-所有公司债代码与已有数据代码的交集，为需要下的数据
company_bond_code = set(company_bond_code.split(','))
company_bond_code_download = company_bond_code - (company_bond_code & (set(already_code)))

codes = ','.join(list(company_bond_code_download))

'''
wsd_data = w.wss(company_bond_code, "sec_name,nature,fullname,issuerupdated,par,exchange_cn,province,listingornot,"
                                      "industry_gics,issuerupdated,comp_name,"
                                       "issueamount,outstandingbalance,carrydate,maturitydate,term,couponrate,windl1type,"
                                       "windl2type,embeddedopt,agency_guarantor,creditrating,issuer_rating,agency_leadunderwriter,"
                                        "rate_creditratingagency,issurercreditratingcompany,industry_sw",
                                        "industryType=1;unit=1")
'''
wsd_data = w.wss(company_bond_code, "sec_name")
bond_static = pd.DataFrame(wsd_data.Data, index=wsd_data.Fields, columns=wsd_data.Codes)

bond_static = bond_static.T
bond_static = bond_static.reset_index().rename(columns={'index': 'code'})
bond_static['CARRYDATE'] = bond_static['CARRYDATE'].apply(lambda x: x.strftime('%Y-%m-%d'))
bond_static['MATURITYDATE'] = bond_static['MATURITYDATE'].apply(lambda x: x.strftime('%Y-%m-%d'))

bond_static.to_excel('raw_data/短期融资融券静态数据.xlsx',index=False,encoding='utf8')



bond_static=pd.read_excel('raw_data/短期融资融券静态数据.xlsx')
code_issuer = bond_static[['code', 'ISSUERUPDATED']]
code_issuer = code_issuer.drop_duplicates('ISSUERUPDATED').reset_index()
code_issuer=code_issuer.drop('index',1)


###取动态数据，公司名称
finance_issuer = pd.read_excel('data_sql/finance_0927.xlsx')['issuer']
finance_issuer = finance_issuer.map(lambda x: str(x).strip())
finance_issuer=finance_issuer.drop_duplicates().reset_index()
finance_issuer=finance_issuer.drop('index',1)
finance_issuer_set=set(finance_issuer['issuer'])

#CP_bond_company_download = set(code_issuer['ISSUERUPDATED']) - (set(code_issuer['ISSUERUPDATED']) & (finance_issuer_set))


l_bond_id=[]
l_issuer=[]
for i in range(0,len(code_issuer['ISSUERUPDATED'])):
    if code_issuer.loc[i,'ISSUERUPDATED'] not in list(finance_issuer['issuer']):
        l_bond_id.append(code_issuer.loc[i,'code'])
        l_issuer.append(code_issuer.loc[i,'ISSUERUPDATED'])
d={'code':l_bond_id,'issuer':l_issuer}
CP_bond_company_download=pd.DataFrame(d)
CP_bond_company_download.to_excel('raw_data/超短期下载的公司.xlsx',index=False,encoding='utf8')


##超短期公司财务数据

#all_code =','.join(list(CP_bond_company_download['code']))


CP_bond_company_download=pd.read_excel('raw_data/超短期下载的公司.xlsx')

df_all=pd.DataFrame()
for i in range(len(CP_bond_company_download['code'])):
#for i in range(0,3):
    wsd_data =w.wsd(CP_bond_company_download.loc[i,'code'],
                    "roe,wgsd_ebit_oper,tot_oper_rev,wgsd_yoy_or,debttoassets,growth_totalequity,quick,invturn,arturn,"
                    "assetsturn1,roa,net_cash_flows_oper_act,tot_assets,nptocostexpense,caturn,cashtostdebt",
                    "2010-03-01", "2018-06-30", "unit=1;rptType=1;currencyType=;N=3;Period=Q;Days=Alldays")
    df = pd.DataFrame(wsd_data.Data, index=wsd_data.Fields, columns=wsd_data.Times)
    df = df.T
    df['ISSUER']=CP_bond_company_download.loc[i,'issuer']
    df['code']=CP_bond_company_download.loc[i,'code']
    df_all=pd.concat([df_all,df])

df_all = df_all.reset_index().rename(columns={'index': 'time_report'})

df_all.to_excel('raw_data/超短期债券公司财务数据.xlsx',index=False,encoding='utf8')

'''
month= df_all['time_report'][len(df_all['time_report'])-1].month
day= df_all['time_report'][len(df_all['time_report'])-1].day
month_day= str(month)+str(day)
if month_day not in ['1231','331','630','930']:
    df_all= df_all.loc[0:(len(df_all)-2),:]

df_all['ID']=df_all['ISSUER'].map(lambda x:str(x))+df_all['time_report'].map(lambda x:str(x))
'''


