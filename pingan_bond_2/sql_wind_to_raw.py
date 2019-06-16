from WindPy import *
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

'''更新静态'''
data_static1 = w.wss(all_code_str, "agency_guarantor,nature,fullname,issuerupdated,par,issueamount,carrydate,maturitydate,term,"
                    "couponrate,issuer,windl1type,municipalbond,embeddedopt,exchange_cn","unit=1")
data_static2 = w.wss(all_code_str, "agency_guarantor,creditrating,issuer_rating,agency_leadunderwriter,industry_gics,province,"
                    "listingornot","industryType=1")
df = pd.concat([pd.DataFrame(data_static1.Data,columns=data_static1.Codes, index= data_static1.Fields),
                pd.DataFrame(data_static2.Data,columns=data_static2.Codes, index= data_static2.Fields)],
               axis=0)
df_static = df.T
df_static = df_static.reset_index().rename(columns={'index':'code'})

'''更新Finance'''
df_old1 = pd.read_excel('finance0905.xlsx')
df_old2 = pd.read_excel('超短期下载的公司.xlsx')
df_gongsi = pd.read_excel('公司债静态数据0916.xlsx')
df_static = pd.read_excel('data_sql/bond_info_0919.xlsx')
df_comp = pd.read_excel('data_sql/comp_info_0919.xlsx')

comp_code_old = df_old1.drop_duplicates('ISSUER').ISSUER[~df_old1.drop_duplicates('ISSUER').ISSUER.isin(np.array(df_old2.issuer))].tolist()
df_gongsi_single = df_gongsi.drop_duplicates('COMP_NAME')
all_code_list = np.array(df_gongsi_single.code)[~df_gongsi_single.COMP_NAME.isin(comp_code_old)].tolist()
all_code_str = ','.join(all_code_list)

dynamic = 'roe,wgsd_ebit_oper,tot_oper_rev,wgsd_yoy_or,debttoassets,growth_totalequity,quick,invturn,' \
          'arturn,assetsturn1,roa,net_cash_flows_oper_act,tot_assets,nptocostexpense,caturn,' \
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
df_dyn_2 = df_dyn_1.loc[df_dyn_1.OUTMESSAGE.isnull(),:]
df_dyn_2 = Rename_finance_reverse(df_dyn_2)
df_dyn_2['finance_6'] = df_dyn_2.NET_CASH_FLOWS_OPER_ACT/df_dyn_2.TOT_ASSETS
s1 = df_dyn_2.WGSD_EBIT_OPER[4:]
s1.index = range(len(s1))
s2 = df_dyn_2.WGSD_EBIT_OPER[:-4]
s2.index = range(len(s2))
df = pd.concat([s1,s2],axis=1)
df.columns = ['late','early']
df['finance_10'] = df.late/df.early-1
finance_10 = pd.concat([pd.Series([np.NaN,np.NaN,np.NaN,np.NaN]),df['finance_10']],axis=0)
finance_10.index = range(len(finance_10))
df_dyn_2['finance_10'] = finance_10
df_dyn_2['finance_11'] = df_dyn_2.WGSD_EBIT_OPER/df_dyn_2.TOT_OPER_REV
df_dyn_2['finance_12'] = df_dyn_2.WGSD_YOY_OR
df_dyn_2['finance_14'] = df_dyn_2.GROWTH_TOTALEQUITY
df_all = pd.merge(all_bond_info,df_dyn_2,how='right',on='code')
l_finance = ['finance_1', 'finance_10', 'finance_11', 'finance_12', 'finance_13','finance_14', 'finance_15',
             'finance_2', 'finance_3', 'finance_4','finance_5', 'finance_6', 'finance_7', 'finance_8', 'finance_9',
             'time_report','issuer']
df_dyn_3 = df_all[l_finance]
df_old = pd.read_excel('Finance_0927.xlsx')
df_update1 = pd.concat([df_dyn_3,df_old],axis=0)
df_update2 = df_update1.drop_duplicates(['issuer','time_report'])
df_update2.to_excel('data_sql/Finance_1007.xlsx',index=False)



'''============================================================================================================='''
l_bond_info = ['bond_type_wind_1', 'bond_type_wind_2', 'code', 'coupon_rate', 'date_end', 'date_start',
               'exchange', 'issuer', 'name', 'rate_bond_issue', 'rate_comp_issue',
               'sponsor', 'total_100million','underwriter', 'year']
l_comp_info = ['issuer','company_type','industry', 'listed', 'province']
l_bond_info_dyn = ['rate_bond_lastest','time_report','code']
l_comp_info_dyn = ['rate_comp_lastest','time_report','code']
l_finance = ['finance_1', 'finance_10', 'finance_11', 'finance_12', 'finance_13','finance_14', 'finance_15',
             'finance_2', 'finance_3', 'finance_4','finance_5', 'finance_6', 'finance_7', 'finance_8', 'finance_9',
             'time_report','issuer']
l_default = ['code','date_default','event','rate_history','balance_100million']

df1 = pd.read_excel('past_0912.xlsx')

df3 = df_update

all_code = pd.concat([df1[['code','issuer']],df2[['code','issuer']],df3[['code','issuer']]],axis=0).drop_duplicates('code')
all_issuer = pd.concat([df1[['code','issuer']],df2[['code','issuer']],df3[['code','issuer']]],axis=0).drop_duplicates('issuer')
all_issuer['issuer_ID'] = range(len(all_issuer))

all_bond_info = pd.concat([df1[l_bond_info],df2[l_bond_info],df3[l_bond_info]],axis=0).drop_duplicates('code')
all_comp_info = pd.concat([df1[l_comp_info],df2[l_comp_info],df3[l_comp_info]],axis=0).drop_duplicates('issuer')

finance_com = df3[l_finance]
finance_com_issuer = df3.issuer.drop_duplicates()
finance_not_com1 = pd.concat([df1[l_finance],df2[l_finance]],axis=0)
finance_not_com2 = finance_not_com1.loc[~finance_not_com1.issuer.isin(np.array(finance_com_issuer)),:]
finance_not_com = finance_not_com2.drop_duplicates(['issuer','time_report'])
all_finance = pd.concat([finance_com,finance_not_com],axis=0)
all_finance = all_finance.sort_values(by=['issuer','time_report'],axis=0)

all_default = df2[l_default]

all_code.to_excel('data_sql/code_0919.xlsx',index=False)
all_issuer.to_excel('data_sql/issuer_0919.xlsx',index=False)
all_bond_info.to_excel('data_sql/bond_info_0919.xlsx',index=False)
all_comp_info.to_excel('data_sql/comp_info_0919.xlsx',index=False)
all_finance.to_excel('data_sql/finance_0919.xlsx',index=False)
all_default.to_excel('data_sql/default_0919.xlsx',index=False)


