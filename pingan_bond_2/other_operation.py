# -*- coding: utf-8 -*-
"""

-------------------------------------------------
   File Name：        other_operation
   Description :
   Author :           何友鑫
   date：             2018-09-27
   latest version:    v1.0.0
-------------------------------------------------
   Change Log:
    v1.0.0            hyx        2018-09-27
    1.finance数据去重
    2.合并相同意思的交易所
-------------------------------------------------

"""


import pandas as pd
import re

finance=pd.read_excel('data_sql/finance_0919.xlsx')

finance=finance.drop_duplicates().reset_index().drop('index',1)

finance.to_excel('data_sql/finance_0927.xlsx',index=False,encoding='utf8')



##合并交易所
bond_info=pd.read_excel('data_sql/bond_info_0919.xlsx')
bond_info.exchange=bond_info.exchange.map(lambda x:'上海' if x=='上海证券交易所' else x)
bond_info.exchange=bond_info.exchange.map(lambda x:'深圳' if x=='深圳证券交易所' else x)
bond_info.exchange=bond_info.exchange.map(lambda x:'银行间' if re.search('银行',x) else x)
bond_info.to_excel('data_sql/bond_info_0928.xlsx',index=False,encoding='utf8')



##------------------------------------------------------------------------------------##
##下载未完成的公司债数据--------------------------###

from WindPy import w
w.start()
import pandas as pd
import numpy as np
import datetime


def Rename(df):
    d = {'债券余额(亿元)':'balance_100million','代码':'code','公司属性':'company_type','发行总额[单位] 亿元':'total_100million',
         '票面利率(发行时)[单位] %':'coupon_rate','发生日期':'date_default','到期日期':'date_end','起息日期':'date_start',
         '事件摘要':'event','上市交易所':'exchange','净资产收益率ROE(平均)':'ROE','债券期限(年)[单位] 年':'year',
         '营业利润(同比增长率)':'YOYOP','营业利润/营业总收入':'return_income','营业收入(同比增长率)':'YOY_TR','coupon':'coupon_rate',
         '资产负债率':'DEBTTOASSETS','资本累计率':'YOY_EQUITY','速动比率':'QUICK','存货周转率':'INVTURN','证券简称':'name',
         '应收账款周转率':'ARTURN','总资产周转率':'ASSETSTURN1','总资产报酬率ROA':'ROA','公司属性[交易日期] 最新收盘日':'company_type',
         '总资产现金回收率':'cf_to_asset','成本费用利润率':'NPTOCOSTEXPENSE','流动资产周转率':'CATURN','Wind债券一级分类':'bond_type_wind_1',
         '现金比率':'CASHTOCURRENTDEBT','所属wind行业':'industry_wind','Wind债券二级分类':'bond_type_wind_2','上市地点':'exchange',
         '发行人中文名称':'issuer','是否上市公司':'listed','省份':'province','发行时债项评级':'rate_bond_issue','China News-Based EPU':'ChinaNewsBasedEPU',
         '最新债项评级':'rate_bond_lastest','发行时主体评级':'rate_comp_issue','最新主体评级':'rate_comp_lastest','NATURE':'company_type',
         '评级历史':'rate_history','担保人':'sponsor','主承销商':'underwriter','所属Wind行业名称[行业级别] 一级行业':'industry','EXCHANGE_CN':'exchange',
         '票面利率':'coupon_rate','发行人':'issuer','名称':'name','债券简称':'name','上市日期':'date_start','票面利率(发行时)\r\n[单位] %':'coupon_rate',
         '发行总额\r\n[单位] 亿元':'total_100million','债券期限(年)\r\n[单位] 年':'year','公司属性\r\n[交易日期] 最新收盘日':'company_type',
         '一级行业':'industry','发行人最新评级↓':'rate_comp_lastest','consumption':'consumption','CPI':'CPI','creditspread':'creditspread','GDP':'GDP','SEC_NAME':'name','EMBEDDEDOPT':'has_option',
         'PROVINCE':'province','LISTINGORNOT':'listed','INDUSTRY_GICS':'industry','COMP_NAME':'issuer','ISSUEAMOUNT':'total_100million','OUTSTANDINGBALANCE':'balance',
         'CARRYDATE':'date_start','MATURITYDATE':'date_end','TERM':'year','COUPONRATE':'coupon_rate','WINDL1TYPE':'bond_type_wind_1','WINDL2TYPE':'bond_type_wind_2',
         'AGENCY_GUARANTOR':'sponsor','CREDITRATING':'rate_bond_issue','ISSUER_RATING':'rate_comp_issue','AGENCY_LEADUNDERWRITER':'underwriter','ID':'ID','ISSUER':'issuer',
         'time_report':'time_report','LATESTISSURERCREDITRATING':'rate_comp_lastest','code':'code','finance_1':'ROE','finance_10':'YOYOP','finance_11':'return_to_income','finance_12':'YOY_TR',
         'finance_13':'DEBTTOASSETS','finance_14':'YOY_EQUITY','finance_15':'QUICK','finance_2':'INVTURN','finance_3':'ARTURN','finance_4':'ASSETSTURN1','finance_5':'ROA','finance_6':'cf_to_asset',
         'finance_7':'NPTOCOSTEXPENSE','finance_8': 'CATURN','finance_9':'CASHTOCURRENTDEBT','cf_to_asset':'cf_to_asset','return_to_income':'return_to_income'}
    df = df.rename(columns=d)
    '''
    l=[]
    for m in df.columns:
        if m not in d.values():
            l.append(m)
    print('删除以下列：')
    print(l)
    df = df.drop(l,axis=1)
    '''
    return(df)

def Rename_finance(df):
    d = {'finance_1':'ROE','finance_10':'YOYOP','finance_11':'return_to_income','finance_12':'YOY_TR',
         'finance_13':'DEBTTOASSETS','finance_14':'YOY_EQUITY','finance_15':'QUICK','finance_2':'INVTURN','finance_3':'ARTURN',
         'finance_4':'ASSETSTURN1','finance_5':'ROA','finance_6':'cf_to_asset',
         'finance_7':'NPTOCOSTEXPENSE','finance_8': 'CATURN','finance_9':'CASHTOCURRENTDEBT'}
    df = df.rename(columns=d)
    return(df)

def Rename_finance_reverse(df):
    d1 = {'finance_1':'ROE','finance_10':'YOYOP','finance_11':'return_to_income','finance_12':'YOY_TR',
         'finance_13':'DEBTTOASSETS','finance_14':'YOY_EQUITY','finance_15':'QUICK','finance_2':'INVTURN','finance_3':'ARTURN',
         'finance_4':'ASSETSTURN1','finance_5':'ROA','finance_6':'cf_to_asset',
         'finance_7':'NPTOCOSTEXPENSE','finance_8': 'CATURN','finance_9':'CASHTOCURRENTDEBT'}
    d2 = dict([(v,k) for (k,v) in d1.items()])
    df = df.rename(columns=d2)
    return df


company_left=pd.read_excel('finance_gongsi_left_1007.xlsx')
all_code_list = np.array(company_left.code).tolist()
all_code_str = ','.join(all_code_list)

dynamic = 'roe,wgsd_ebit_oper,tot_oper_rev,wgsd_yoy_or,debttoassets,growth_totalequity,quick,invturn,' \
          'arturn,assetsturn1,roa,net_cash_flows_oper_act,tot_assets,nptocostexpense,caturn,yoyop,' \
          'cashtocurrentdebt'
df_dyn = ''

for code in all_code_list:
    date_start = '20100101'
    date_end = datetime.datetime.now().strftime("%Y%m%d")
    data_dynamic = w.wsd(code, dynamic, date_start, date_end, "unit=1;rptType=1;currencyType=;N=1;Period=Q;Days=Alldays")
    dff = pd.DataFrame(data_dynamic.Data, index=data_dynamic.Fields, columns=data_dynamic.Times).T
    dff = dff.reset_index().rename(columns={'index': 'time_report'})
    dff['code'] = code
    if isinstance(df_dyn,str):
        df_dyn = dff
    else:
        df_dyn = pd.concat([df_dyn,dff],axis=0)


df_dyn_1 = df_dyn
#df_dyn_2 = df_dyn_1.loc[df_dyn_1.OUTMESSAGE.isnull(),:]
df_dyn_2=df_dyn_1
df_dyn_2 = Rename_finance_reverse(df_dyn_2)
df_dyn_2['finance_6'] = df_dyn_2.NET_CASH_FLOWS_OPER_ACT/df_dyn_2.TOT_ASSETS
##finance_10可以直接下载
df_dyn_2['finance_11'] = df_dyn_2.WGSD_EBIT_OPER/df_dyn_2.TOT_OPER_REV
df_dyn_2['finance_12'] = df_dyn_2.WGSD_YOY_OR
df_dyn_2['finance_14'] = df_dyn_2.GROWTH_TOTALEQUITY
all_bond_info=pd.read_excel('data_sql/bond_info_1007.xlsx')
df_all = pd.merge(all_bond_info,df_dyn_2,how='right',on='code')
#df_all=df_dyn_2
l_finance = ['finance_1', 'finance_10', 'finance_11', 'finance_12', 'finance_13','finance_14', 'finance_15',
             'finance_2', 'finance_3', 'finance_4','finance_5', 'finance_6', 'finance_7', 'finance_8', 'finance_9',
             'time_report','issuer']
df_dyn_3 = df_all[l_finance]
df_old = pd.read_excel('data_sql/Finance_1007.xlsx')
df_update1 = pd.concat([df_dyn_3,df_old],axis=0)
df_update2 = df_update1.drop_duplicates(['issuer','time_report'])
df_update2.to_excel('data_sql/finance_1008.xlsx',index=False)

##-----------------------------------------------------------------------------------##
##----------把公司属性补上------------------##

comp_info = pd.read_excel('data_sql/comp_info_1007.xlsx')

comp_info_na=comp_info[comp_info['company_type']=='ERROR! please fill it'].reset_index().drop('index',1)


bond_info = pd.read_excel('data_sql/bond_info_1007.xlsx')

comp_info_na_bond=pd.merge(comp_info_na,bond_info,how='left').drop_duplicates('issuer').reset_index().drop('index',1)


codes = ','.join(list(comp_info_na_bond.code))

wsd_data = w.wss(codes, "nature" , "industryType=1;unit=1")

bond_static = pd.DataFrame(wsd_data.Data, index=wsd_data.Fields, columns=wsd_data.Codes)

bond_static = bond_static.T
bond_static = bond_static.reset_index().rename(columns={'index': 'code'})

comp_info_na_bond_2=pd.merge(comp_info_na_bond,bond_static)
comp_info_na_bond_2=comp_info_na_bond_2[['issuer','NATURE']]

comp_info_2=pd.merge(comp_info,comp_info_na_bond_2,how='left')
comp_info_2['company_type'] = comp_info_2.apply(lambda x: x.NATURE if x.company_type == 'ERROR! please fill it' else x.company_type, axis=1)

comp_info_2=comp_info_2.drop(['NATURE'],1)

comp_info_2.to_excel('data_sql/comp_info_1008.xlsx',index=False,encoding='utf8')





##----------------------------------------------------------------##
##超短期公司财务数据加入

##静态写入bond_info comp_info

bond_static_CP = pd.read_excel('raw_data/短期融资融券静态数据.xlsx')
bond_static_CP=Rename(bond_static_CP)
l_bond_info = ['bond_type_wind_1', 'bond_type_wind_2', 'code', 'coupon_rate', 'date_end', 'date_start',
               'exchange', 'issuer', 'name', 'rate_bond_issue', 'rate_comp_issue',
               'sponsor', 'total_100million','underwriter', 'year']
l_comp_info = ['issuer','company_type','industry', 'listed', 'province']

#更新bond_info
bond_info_update = bond_static_CP[l_bond_info]
bond_info_old = pd.read_excel('data_sql/bond_info_1007.xlsx')
df_update1 = pd.concat([bond_info_old,bond_info_update],axis=0)
df_update2 = df_update1.drop_duplicates(['code'])
df_update2.to_excel('data_sql/bond_info_1009.xlsx',index=False)


#更新comp_info
comp_info_update = bond_static_CP[l_comp_info]
comp_info_old = pd.read_excel('data_sql/comp_info_1008.xlsx')
df_update1 = pd.concat([comp_info_old,comp_info_update],axis=0)
df_update2 = df_update1.drop_duplicates(['issuer'])
df_update2.to_excel('data_sql/comp_info_1009.xlsx',index=False)




CP_bond_company_download=pd.read_excel('raw_data/超短期下载的公司.xlsx')
#company_left=pd.read_excel('raw_data/CP_bond_company_download.xlsx')
all_code_list = np.array(CP_bond_company_download.code).tolist()
all_code_str = ','.join(all_code_list)

dynamic = 'roe,wgsd_ebit_oper,tot_oper_rev,wgsd_yoy_or,debttoassets,growth_totalequity,quick,invturn,' \
          'arturn,assetsturn1,roa,net_cash_flows_oper_act,tot_assets,nptocostexpense,caturn,yoyop,' \
          'cashtocurrentdebt'
df_dyn = ''

for code in all_code_list:
    date_start = '20100101'
    date_end = datetime.datetime.now().strftime("%Y%m%d")
    data_dynamic = w.wsd(code, dynamic, date_start, date_end, "unit=1;rptType=1;currencyType=;N=1;Period=Q;Days=Alldays")
    dff = pd.DataFrame(data_dynamic.Data, index=data_dynamic.Fields, columns=data_dynamic.Times).T
    dff = dff.reset_index().rename(columns={'index': 'time_report'})
    dff['code'] = code
    if isinstance(df_dyn,str):
        df_dyn = dff
    else:
        df_dyn = pd.concat([df_dyn,dff],axis=0)


df_dyn_1 = df_dyn
#df_dyn_2 = df_dyn_1.loc[df_dyn_1.OUTMESSAGE.isnull(),:]
df_dyn_2=df_dyn_1
df_dyn_2 = Rename_finance_reverse(df_dyn_2)
df_dyn_2['finance_6'] = df_dyn_2.NET_CASH_FLOWS_OPER_ACT/df_dyn_2.TOT_ASSETS
##finance_10可以直接下载
df_dyn_2['finance_11'] = df_dyn_2.WGSD_EBIT_OPER/df_dyn_2.TOT_OPER_REV
df_dyn_2['finance_12'] = df_dyn_2.WGSD_YOY_OR
df_dyn_2['finance_14'] = df_dyn_2.GROWTH_TOTALEQUITY
all_bond_info=pd.read_excel('data_sql/bond_info_1009.xlsx')
df_all = pd.merge(all_bond_info,df_dyn_2,how='right',on='code')
#df_all=df_dyn_2
l_finance = ['finance_1', 'finance_10', 'finance_11', 'finance_12', 'finance_13','finance_14', 'finance_15',
             'finance_2', 'finance_3', 'finance_4','finance_5', 'finance_6', 'finance_7', 'finance_8', 'finance_9',
             'time_report','issuer']
df_dyn_3 = df_all[l_finance]
df_old = pd.read_excel('data_sql/finance_1008.xlsx')
df_update1 = pd.concat([df_dyn_3,df_old],axis=0)
df_update2 = df_update1.drop_duplicates(['issuer','time_report'])
df_update2.to_excel('data_sql/finance_1009.xlsx',index=False)



##-----------------------------------------------
##default表去重
import pandas as pd
default_old = pd.read_excel('data_sql/default_0919.xlsx')
default_new = default_old.drop_duplicates()
default_new.to_excel('data_sql/default_1009.xlsx',index=False,encoding='utf8')




##------------------------------------------------##
#下载流动性数据

df=pd.DataFrame()
codes={"M0010096":'excess_reserve_ratio','M0330245':'R007_amount','M0330244':'R001_amount',
       'M1004529':'R001_rate','M1004533':'R007_rate',"M0061614":'OMO_net_delivery','M0061615':'OMO_delivery',
       'M0061616':'OMO_maturity','M5206730':'social_finance'}

for k,v in codes.items():
    temp = w.edb(k, "2016-10-01", "2018-10-10","Fill=Previous")
    temp = pd.DataFrame(temp.Data, index=temp.Fields, columns=temp.Times).T.reset_index().rename(columns={'index': 'time_report','CLOSE':'value'})
    temp['variable']=v
    df=pd.concat([df,temp])


df.to_excel('data_sql/liquidity.xlsx',index=False,encoding='utf8')



######################################################
#下载补充宏观数据
df=pd.DataFrame()
date_end = datetime.datetime.now().strftime("%Y%m%d")
codes={'S0059744':'1Y_treasury_rate','S0059749':'10Y_treasury_rate',
       'M0265861':'net_debt_index','S0059742':'6M_treasury_rate','S0059746':'3Y_treasury_rate',
       'S0059747':'5Y_treasury_rate','S0059748':'7Y_treasury_rate'}

for k,v in codes.items():
    temp = w.edb(k, "2016-10-01", date_end,"Fill=Previous")
    temp = pd.DataFrame(temp.Data, index=temp.Fields, columns=temp.Times).T.reset_index().rename(columns={'index': 'time_report','CLOSE':'value'})
    temp['variable']=v
    df=pd.concat([df,temp])

df_old = pd.read_excel('data_sql/macro.xlsx')

df = pd.concat([df_old,df]).drop_duplicates()
df = df.reset_index().drop('index',1)

df.to_excel('data_sql/macro.xlsx',index=False,encoding='utf8')

##----------------------------------------------
##超额存款准备

date_end = datetime.datetime.now().strftime("%Y%m%d")
df = w.edb("M0001690,M0001691,M0001384,M0001492,M0001727,M0001693,M0061518,M0043821,M0252070,M0251979,M0001622",
      "2017-10-12", date_end,"Fill=Previous")

df.Data

df2 = pd.DataFrame(df.Data, index=df.Fields, columns=df.Times).T