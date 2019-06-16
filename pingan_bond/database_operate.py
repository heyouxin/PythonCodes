# -*- coding: utf-8 -*-
"""

-------------------------------------------------
   File Name：        database_operate
   Description :
   Author :           何友鑫
   date：             2018-08-22
   latest version:    v1.0.0
-------------------------------------------------
   Change Log:
    v1.0.0            hyx        2018-08-22
    1.create function connect to database , create function DataFromWind and DataToDatabase
    2.get data from Wind API
    3.import the df to the mysql database
-------------------------------------------------
"""

import pandas as pd
from sqlalchemy import create_engine
import pymysql
from WindPy import w

from datetime import datetime
import re
from sklearn.linear_model.logistic import LogisticRegression
import numpy as np
import math as m


def set_sql(gdb, ghost, guser, gpassword, gdatabase):
    global db, host, user, password, database, engine, conn
    db = gdb
    host = ghost
    user = guser
    password = gpassword
    database = gdatabase
    engine = set_engine()
    conn = set_conn()

def set_engine():
    global engine
    try:
        engine.close()
    except:
        pass
    if db.lower() == 'mysql':
        engine = create_engine('mysql+pymysql://' + user + ':' + password + '@' + host + '/' + database)
    if db.lower() == 'mssql':
        engine = create_engine('mssql+pyodbc://' + user + ':' + password + '@' + host + '/' + database)
    return engine

def set_conn():
    if db.lower() == 'mysql':
        conn = pymysql.connect(host=host, user=user, password=password, db=database, charset='utf8')
    if db.lower() == 'mssql':
        conn = pymssql.connect(host=host, user=user, password=password, database=database, charset="utf8")
    return conn


def GetBondCode():

    ##获取现在已有债券代码表
    already_code=pd.read_excel('data/Already_quarter_0807_1.xlsx')['code']
    already_code=already_code.map(lambda x:str(x).strip())
    default_code=pd.read_excel('data/Default_quarter_0807_1.xlsx')['code']
    default_code=default_code.map(lambda x:str(x).strip())
    ##获得所有的公司债  债券代码

    file_object = open('data/所有公司债代码.txt')
    try:
        company_bond_code = file_object.read()
    finally:
        file_object.close()
    #所有公司债代码-所有公司债代码与已有数据代码的交集，为需要下的数据
    company_bond_code=set(company_bond_code.split(','))
    company_bond_code_download=company_bond_code-(company_bond_code & (set(already_code) | set(default_code)))

    #返回所有正在存续公司债数据
    return company_bond_code_download




def BondFromWind(codes):

    w.start()
    #if is_static==1:
    wsd_data=w.wss(codes, "sec_name,exchange_cn,province,listingornot,industry_gics,issuerupdated,comp_name,"
                                       "issueamount,outstandingbalance,carrydate,maturitydate,term,couponrate,windl1type,"
                                       "windl2type,embeddedopt,agency_guarantor,creditrating,issuer_rating,agency_leadunderwriter",
                          "industryType=1;unit=1;tradeDate=20180903")
    bond_static = pd.DataFrame(wsd_data.Data, index=wsd_data.Fields, columns=wsd_data.Codes)
    bond_static = bond_static.T
    bond_static = bond_static.reset_index().rename(columns={'index': 'code'})
    bond_static['CARRYDATE'] = bond_static['CARRYDATE'].apply(lambda x: x.strftime('%Y-%m-%d'))
    bond_static['MATURITYDATE'] = bond_static['MATURITYDATE'].apply(lambda x: x.strftime('%Y-%m-%d'))


    code_issuer=bond_static[['code', 'ISSUERUPDATED']]
    code_issuer=code_issuer.drop_duplicates('ISSUERUPDATED').reset_index()
    #bond_dynamic_code=list(code_issuer['code'])




    #取动态财务数据
    df_all=pd.DataFrame()
    for i in range(len(code_issuer['code'])):
    #for i in range(0,3):
        wsd_data =w.wsd(code_issuer.loc[i,'code'],
              "roe,wgsd_ebit_oper,tot_oper_rev,yoy_tr,debttoassets,yoy_equity,quick,invturn,arturn,assetsturn1,roa,"
              "wgsd_oper_cf,tot_assets,nptocostexpense,caturn,cashtocurrentdebt,yoyop,latestissurercreditrating",
              "2000-01-01", "2018-09-04", "unit=1;rptType=1;currencyType=;Period=Q")
        df = pd.DataFrame(wsd_data.Data, index=wsd_data.Fields, columns=wsd_data.Times)
        df = df.T
        df['ISSUER']=code_issuer.loc[i,'ISSUERUPDATED']
        df['code']=code_issuer.loc[i,'code']
        df_all=pd.concat([df_all,df])

    df_all = df_all.reset_index().rename(columns={'index': 'time_report'})
    month= df_all['time_report'][len(df_all['time_report'])-1].month
    day= df_all['time_report'][len(df_all['time_report'])-1].day
    month_day= str(month)+str(day)
    if month_day not in ['1231','331','630','930']:
        df_all= df_all.loc[0:(len(df_all)-2),:]

    df_all['ID']=df_all['ISSUER'].map(lambda x:str(x))+df_all['time_report'].map(lambda x:str(x))


    #调整列的顺序
    issuer = df_all['ISSUER']
    df_all.drop(labels=['ISSUER'], axis=1, inplace=True)
    df_all.insert(0, 'ISSUER', issuer)


    ID = df_all['ID']
    df_all.drop(labels=['ID'], axis=1, inplace=True)
    df_all.insert(0, 'ID', ID)

    #bond_finance=df_all


    return (bond_static,df_all)

def DataToDatabase(gdb, ghost, guser, gpassword, gdatabase,df,table_name,is_static=1):

    df=bond_finance
    set_sql(gdb, ghost, guser, gpassword, gdatabase)
    cur = conn.cursor()

    if is_static==1:
        #债券静态表建表sql语句                                                主键        操作字段
        sql_create_table = "create table IF NOT EXISTS " +table_name+" (code varchar(50) PRIMARY KEY,SEC_NAME varchar(50),EXCHANGE_CN varchar(50),\
            PROVINCE varchar(50),LISTINGOR varchar(4),INDUSTRY_GIGS varchar(50),ISSUERUPDATED varchar(200),COMP_NAME varchar(100),ISSUEAMOUNT double,\
            OUTSTANDINGBALANCE double,CARRYDATE date,MATURITYDATE date,TERM double,COUPONRATE double,WINDL1TYPE varchar(50),WINDL2TYPE varchar(50),\
            EMBEDDEDOPT varchar(4),AGENCY_GUARANTOR varchar(200),CREDITRATING varchar(50),ISSUER_RATING varchar(50),AGENCY_LEADUNDERWRITER varchar(500) )"
    else:
        '''
        bond_finance.columns
        ['ID', 'ISSUER', 'time_report', 'ARTURN', 'ASSETSTURN1',
       'CASHTOCURRENTDEBT', 'CATURN', 'DEBTTOASSETS', 'INVTURN',
       'LATESTISSURERCREDITRATING', 'NPTOCOSTEXPENSE', 'OUTMESSAGE', 'QUICK',
       'ROA', 'ROE', 'TOT_ASSETS', 'TOT_OPER_REV', 'WGSD_EBIT_OPER',
       'WGSD_OPER_CF', 'YOYOP', 'YOY_EQUITY', 'YOY_TR', 'code']
        
        '''
        #债券财务数据建表sql语句                                                主键        操作字段
        sql_create_table = "create table IF NOT EXISTS " +table_name+" (ID varchar(200) PRIMARY KEY ,ISSUER varchar(200),time_report varchar(50),\
                          ARTURN double,ASSETSTURN1 double,CASHTOCURRENTDEBT double,CATURN double,DEBTTOASSETS double,INVTURN double,\
                        LATESTISSURERCREDITRATING double,NPTOCOSTEXPENSE double,OUTMESSAGE double,QUICK double,\
                        ROA double,ROE double,TOT_ASSETS double,TOT_OPER_REV double,WGSD_EBIT_OPER double,WGSD_OPER_CF double,YOYOP double,\
                        YOY_EQUITY double,YOY_TR double,code varchar(50) )"

    sql_insert = "insert into " + table_name + " values (" + "%s," * (len(df.columns) - 1) + "%s);"

    # 这个格式很重要，dataframe是不能当此处参数格式的
    param = df.values.tolist()

    '''
    sql_update = "update 修改表 as x, 临时表 as t \
                   set x.nlp_name_semantics_v3=t.nlp_name_semantics_v3 \
                   where x.id=t.id;"
    # 操作数据库
    '''
    try:
        cur.execute(sql_create_table)  # 向sql语句传递参数
    except:
        pass
    try:
        cur.executemany(sql_insert, param)  # len(param[0])
        # cur.execute(sql_update3)
        conn.commit()
    except Exception as e:
        # 错误回滚
        conn.rollback()
        print('插入数据发生错误，已经回滚')
    finally:
        conn.close()

'''
    code_issuer=pd.read_excel('公司债财务数据.xlsx')
    code_issuer.to_csv('公司债财务数据.csv',index=False,encoding='utf8')
    #row=code_issuer[code_issuer['code']=='145734.SH']
    #code_issuer.loc[31223,:]
    df_all=pd.DataFrame()
    for i in range(31224,len(code_issuer['code'])):
    #for i in range(0,3):
        wsd_data =w.wsd(code_issuer.loc[i,'code'],
              "roe,wgsd_ebit_oper,tot_oper_rev,yoy_tr,debttoassets,yoy_equity,quick,invturn,arturn,assetsturn1,roa,"
              "wgsd_oper_cf,tot_assets,nptocostexpense,caturn,cashtocurrentdebt,yoyop,latestissurercreditrating",
              "2000-01-01", "2018-09-04", "unit=1;rptType=1;currencyType=;Period=Q")
        df = pd.DataFrame(wsd_data.Data, index=wsd_data.Fields, columns=wsd_data.Times)
        df = df.T
        df['ISSUER']=code_issuer.loc[i,'ISSUERUPDATED']
        df['code']=code_issuer.loc[i,'code']
        df_all=pd.concat([df_all,df])

    df_all = df_all.reset_index().rename(columns={'index': 'time_report'})
    month= df_all['time_report'][len(df_all['time_report'])-1].month
    day= df_all['time_report'][len(df_all['time_report'])-1].day
    month_day= str(month)+str(day)
    if month_day not in ['1231','331','630','930']:
        df_all= df_all.loc[0:(len(df_all)-2),:]

    df_all['ID']=df_all['ISSUER'].map(lambda x:str(x))+df_all['time_report'].map(lambda x:str(x))


    #调整列的顺序
    issuer = df_all['ISSUER']
    df_all.drop(labels=['ISSUER'], axis=1, inplace=True)
    df_all.insert(0, 'ISSUER', issuer)


    ID = df_all['ID']
    df_all.drop(labels=['ID'], axis=1, inplace=True)
    df_all.insert(0, 'ID', ID)



'''




if __name__ == "__main__":
    gdb = 'mysql'
    ghost = 'localhost'
    guser = 'root'
    gpassword = '123456'
    gdatabase = 'raw_data'
    conn = ''
    engine = ''
    table_name="bond_static"
    company_bond_code_download=GetBondCode()
    codes = ','.join(list(company_bond_code_download))

    (bond_static,bond_finance)= BondFromWind(codes)
    DataToDatabase(gdb, ghost, guser, gpassword, gdatabase, bond_static,table_name)
    table_name = "bond_finance"
    DataToDatabase(gdb, ghost, guser, gpassword, gdatabase, bond_finance,table_name,0)

    #df.to_excel('test_data.xlsx',index=False,encoding='utf8')

    bond_static.to_excel('公司债静态数据.xlsx',index=False,encoding='utf8')

    bond_finance.to_excel('公司债财务数据.xlsx',index=False,encoding='utf8')
    data_static=pd.read_csv('data_static0903.csv',encoding='gbk')
    data_static=data_static.T


    bond_static[bond_static['code']=='145734.SH']

    gdb = 'mysql'
    ghost = 'localhost'
    guser = 'root'
    gpassword = '123456'
    gdatabase = 'raw_data'
    conn = ''
    engine = ''


    '''
    df=df.reset_index().rename(columns={'index':'time_report'})
    d = {'NATURE1':'company_type','ISSUERUPDATED':'issuer','证券代码':'code','公司属性':'company_type','发行总额[单位] 亿元':'total_100million',
         '票面利率(发行时)[单位] %':'coupon_rate','发生日期':'date_default','到期日期':'date_end','起息日期':'date_start',
         '事件摘要':'event','上市交易所':'exchange','净资产收益率ROE(平均)':'finance_1','债券期限(年)[单位] 年':'year',
         '营业利润(同比增长率)':'finance_10','营业利润/营业总收入':'finance_11','营业收入(同比增长率)':'finance_12','coupon':'coupon_rate',
         '资产负债率':'finance_13','资本累计率':'finance_14','速动比率':'finance_15','存货周转率':'finance_2','证券简称':'name',
         '应收账款周转率':'finance_3','总资产周转率':'finance_4','总资产报酬率ROA':'finance_5','公司属性[交易日期] 最新收盘日':'company_type',
         '总资产现金回收率':'finance_6','成本费用利润率':'finance_7','流动资产周转率':'finance_8','Wind债券一级分类':'bond_type_wind_1',
         '现金比率':'finance_9','所属wind行业':'industry_wind','Wind债券二级分类':'bond_type_wind_2','上市地点':'exchange',
         '发行人中文名称':'issuer','是否上市公司':'listed','省份':'province','发行时债项评级':'rate_bond_issue','China News-Based EPU':'ChinaNewsBasedEPU',
         '最新债项评级':'rate_bond_lastest','发行时主体评级':'rate_comp_issue','最新主体评级':'rate_comp_lastest',
         '评级历史':'rate_history','担保人':'sponsor','主承销商':'underwriter','所属Wind行业名称[行业级别] 一级行业':'industry',
         '票面利率':'coupon_rate','发行人':'issuer','名称':'name','债券简称':'name','上市日期':'date_start','票面利率(发行时)\r\n[单位] %':'coupon_rate',
         '发行总额\r\n[单位] 亿元':'total_100million','债券期限(年)\r\n[单位] 年':'year','公司属性\r\n[交易日期] 最新收盘日':'company_type',
         '一级行业':'industry','发行人最新评级↓':'rate_comp_lastest','ROE_AVG':'finance_1','YOYOP':'finance_10','OPTOGR':'finance_11',
         'YOY_TR':'finance_12','DEBTTOASSETS':'finance_13','QUICK':'finance_15','INVTURN':'finance_2','ARTURN':'finance_3','ASSETSTURN1':'finance_4',
         'ROA2':'finance_5','NPTOCOSTEXPENSE':'finance_7','CATURN':'finance_8','CASHTOCURRENTDEBT':'finance_9',
         'consumption':'consumption','CPI':'CPI','creditspread':'creditspread','GDP':'GDP','time_report':'time_report'}
    df = df.rename(columns=d)
    '''
