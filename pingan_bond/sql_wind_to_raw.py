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

all_code = '145065.SH,101551056.IB'
data_static1 = w.wss(all_code, "agency_guarantor,nature,fullname,issuerupdated,par,issueamount,carrydate,maturitydate,term,"
                    "couponrate,issuer,windl1type,municipalbond,embeddedopt,exchange_cn","unit=1")
data_static2 = w.wss(all_code, "agency_guarantor,creditrating,issuer_rating,agency_leadunderwriter,industry_gics,province,"
                    "listingornot","industryType=1")
df = pd.concat([pd.DataFrame(data_static1.Data,columns=data_static1.Codes, index= data_static1.Fields),
                pd.DataFrame(data_static2.Data,columns=data_static2.Codes, index= data_static2.Fields)],
               axis=0)
df_static = df.T
df_static = df_static.reset_index().rename(columns={'index':'code'})

all_code =['145065.SH','101551056.IB']
dynamic = 'roe,wgsd_ebit_oper,tot_oper_rev,wgsd_yoy_or,debttoassets,growth_totalequity,quick,invturn,' \
          'arturn,assetsturn1,roa,net_cash_flows_oper_act,tot_assets,nptocostexpense,caturn,' \
          'cashtocurrentdebt'
df_dyn = ''
for code in all_code:
    date_start = df_static.loc[df_static.code==code,'CARRYDATE'].tolist()[0].strftime("%Y%m%d")
    date_end = min(df_static.loc[df_static.code==code,'MATURITYDATE'].tolist()[0],datetime.datetime.now())
    date_end = date_end.strftime("%Y%m%d")
    data_dynamic = w.wsd(code, dynamic, date_start, date_end, "unit=1;rptType=1;currencyType=;N=1;Period=Q")
    dff = pd.DataFrame(data_dynamic.Data, index=data_dynamic.Fields, columns=data_dynamic.Times).T
    dff = dff.reset_index().rename(columns={'index': 'time_report'})
    dff['code'] = code
    if isinstance(df_dyn,str):
        df_dyn = dff
    else:
        df_dyn = pd.concat([df_dyn,dff],axis=0)



df = pd.merge(df_static,finance,how='left',on='code')
df_now = Rename_finance_reverse(df)
Df_already = pd.read_excel('Already_quarter_0912.xlsx')
df_already = Df_already
df_already.drop(['alpha', 'belta', 'belta_yj', 'belta_yz','consumption', 'interest_rate', 'CPI',
                 'GDP_growth', 'ChinaNewsBasedEPU'],axis=1,inplace=True)


dff = ''
l1 = codes.split(', ')
for code in l1:
    date_start = df2.loc[code,'CARRYDATE']
    date_end = df2.loc[code,'MATURITYDATE']
    if date_end > datetime.datetime(2018,9,1):
        date_end = datetime.datetime(2018,9,1)
    date_start = str(date_start-datetime.timedelta(days=180))[:10]
    date_end =  str(date_end)[:10]
    data_dynamic = w.wsd(code, dynamic,date_start,date_end,"unit=1;rptType=1;currencyType=;N=1;Period=Q")
    if isinstance(dff,str):
        dff = pd.DataFrame(data_dynamic.Data,index=data_dynamic.Fields,columns=data_dynamic.Times).T
        dff = dff.reset_index().rename(columns={'index':'time_report'})
        dff['code'] = code
    else:
        dff_1 = pd.DataFrame(data_dynamic.Data,index=data_dynamic.Fields,columns=data_dynamic.Times).T
        dff_1 = dff.reset_index()#.rename(columns={'index':'time_report'})
        dff_1['code'] = code
        dff_1 = dff_1.drop('index',axis=1)
        dff = pd.concat([dff,dff_1],axis=0)

data_static.Data
w.wss("038006.IB,038014.IB", "comp_name,industry_gics","industryType=1")



static = 'nature,fullname,issuerupdated,issueamount,outstandingbalance,term,couponrate,issuer,windl1type,windl2type,' \
         'agency_guarantor,creditrating,amount,carrydate,maturitydate'



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

df1 = pd.read_excel('Already_quarter_0919_1.xlsx')
df2 = pd.read_excel('Default_quarter_0912.xlsx')
df3 = pd.read_excel('data_now_allFinance&Info_0917.xlsx')

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