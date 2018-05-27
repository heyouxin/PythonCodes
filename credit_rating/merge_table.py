# -*- coding: utf-8 -*-
"""
Created on Fri Mar  9 15:05:19 2018

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





if __name__ == "__main__":
    others_tab=pd.read_csv("finfin.csv")
    set_sql(gdb,ghost,guser,gpassword,gdatabase)
    institu_indu=pd.read_sql('select institution_id,industry_name from static_institution',conn)
    institu_indu['institution_id'] = institu_indu['institution_id'].astype('int64')
    bond_indic=pd.read_csv("bond_indic.csv",encoding='gbk')
    #bond_indic先匹配上industry_name
    bond_indic2=pd.merge(bond_indic,institu_indu, on='institution_id')
    
    
    #bond_indic2匹配上others_tab的指标按 年月  行业名称
    l_nan=[]
    for i in range(0,28):
        l_nan.append(np.nan)
    df_t_1=[]
    for i in range(0,len(bond_indic2)):
        #合约上市日期为空的情况  先取上市年份， 上市月份没有，取全年所有月份平均
        if bond_indic2['listed_date'][i] is np.nan:
            year=bond_indic2['listed_year'][i]
            record_t_1=others_tab[(others_tab['year']==int(year)) & (others_tab['industry_name']==bond_indic2['industry_name'][i])].iloc[:,1:29]
            if(len(record_t_1)==0):
                df_t_1.append(l_nan)
            else:
                df_t_1.append(list(record_t_1.mean()))
   
        else:  
            year=bond_indic2['listed_date'][i][0:4]           
            month=bond_indic2['listed_date'][i][5:7]            
            record_t_1=others_tab[(others_tab['year']==int(year)) & (others_tab['month']==int(month)) & (others_tab['industry_name']==bond_indic2['industry_name'][i]) ].iloc[:,1:29].values
            if(len(record_t_1)==0):
                df_t_1.append(l_nan)
            else:
                record_t_1=record_t_1[0]
                df_t_1.append(list(record_t_1))
   
    df_t_1=pd.DataFrame(df_t_1)
    df_t_1.columns=list(others_tab.columns.values[1:29])
    bond_indic_indust=pd.merge(bond_indic2,df_t_1,left_index=True,right_index=True,how='outer')
    bond_indic_indust.to_csv("bond_indic_indust.csv")