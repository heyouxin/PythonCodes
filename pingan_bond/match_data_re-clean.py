# -*- coding: utf-8 -*-
"""
Created on Thu Jul 12 13:50:43 2018

@author: 何友鑫
"""


import pandas as pd
from sqlalchemy import create_engine
import pymysql 
from datetime import datetime
import re
from sklearn.linear_model.logistic import LogisticRegression
import numpy as np
import math as m
'''
ghost='210.34.5.184'
guser='group1'
gpassword='Group1.321'
gdatabase='group1'
conn=''
engine=''
'''
gdb = 'mysql'
ghost='localhost'
guser='root'
gpassword='123456'
gdatabase='group1'
conn=''
engine=''


def set_sql(gdb,ghost,guser,gpassword,gdatabase):
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



set_sql(gdb,ghost,guser,gpassword,gdatabase)
df_static_bond=pd.read_sql("select security_id,institution_id,fullname,`default`,listed_date,delisted_date,type_name from static_bond where type_name!='金融债'",conn)
df_default_bond=pd.read_sql("select security_id,default_ann_date,reason from bond_default ",conn)
df_default_bond['security_id']=df_default_bond['security_id'].astype(str)


df_bond=pd.merge(df_static_bond,df_default_bond,left_on='security_id',right_on='security_id',how='left')


conn.close()
df_static_bond2=df_bond
df_static_bond2['listed_year']=''
df_static_bond2['delisted_year']=''
for i in range (0,len(df_static_bond2)):
    #如果上市日期为空
    if df_static_bond2['listed_date'][i]=='':
        p = re.compile(r'\d+')
        if p.findall(df_static_bond2['fullname'][i]) != []:
            if len(p.findall(df_static_bond2['fullname'][i])[0])==2 and int(p.findall(df_static_bond2['fullname'][i])[0])>80 and int(p.findall(df_static_bond2['fullname'][i])[0])<=99 :
                df_static_bond2['listed_year'][i]='19'+ p.findall(df_static_bond2['fullname'][i])[0]
            else:                   
                df_static_bond2['listed_year'][i]=p.findall(df_static_bond2['fullname'][i])[0]
        #如果从fullname里找不到年份的话
        else:
            pass
    #如果上市日期不为空
    else:
        df_static_bond2['listed_year'][i]=datetime.strftime(pd.to_datetime(df_static_bond2['listed_date'][i]),'%Y')
    
    if df_static_bond2['delisted_date'][i]=='':
        #如果没有退市日期的话。。。
        pass
    else:
        df_static_bond2['delisted_year'][i]=datetime.strftime(pd.to_datetime(df_static_bond2['delisted_date'][i]),'%Y')
  
        
    
#检测异常数据 有两处
#temp1=df_static_bond2[df_static_bond2.listed_date=='']
print("listed_year:error-----")
for t in range(0,len(df_static_bond2['listed_year'])):
    if len(df_static_bond2['listed_year'][t])<4:
        print(df_static_bond2['listed_year'][t])
        print(t)
    else:
        if int(df_static_bond2['listed_year'][t])<1980 or  int(df_static_bond2['listed_year'][t])>2020:
            print(df_static_bond2['listed_year'][t])
            print(t)
            
#1488 12014  8769  行找不到上市日期，从fullname也提取不到   1488暂时先赋值2014    12014
df_static_bond2['listed_year'][1488]='2014'
#df_static_bond2['listed_year'][1860]='2015'
#8769行原始数据数据错误，更正
df_static_bond2['listed_year'][8769]='2014'

print("delisted_year:error-----")      
for t in range(0,len(df_static_bond2['delisted_year'])):
    if len(df_static_bond2['delisted_year'][t])<4:
        #print(df_static_bond2['delisted_year'][t])
        #print(t)
        df_static_bond2['delisted_year'][t]=df_static_bond2['listed_year'][t]
    else:
        if int(df_static_bond2['delisted_year'][t])<1980 or  int(df_static_bond2['delisted_year'][t])>2020:
            #print(df_static_bond2['delisted_year'][t])
            #print(t)               
            df_static_bond2['delisted_year'][t]=df_static_bond2['listed_year'][t]   
            
            
df_institution=pd.read_sql("select institution_id,fullname institution_name,province,city,comp_type,industry_code,industry_name,nature,nature_id,is_finance,is_listed is_listed_error from static_institution ",conn)
            
df_bond_institu=pd.merge(df_bond,df_institution,how='left')
                   
df_bond_institu[df_bond_institu['default']=='1']

df_bond_institu.to_excel('test_data.xlsx')