#!/usr/bin/env python2
# -*- coding: utf-8 -*-


from __future__ import division, unicode_literals
import pandas as pd
import pymysql
import pymssql
from sqlalchemy import create_engine
import re
import numpy as np
import statsmodels.api as sm
from scipy.stats import *
from sklearn import preprocessing
import datetime
import tushare as ts
import re

gdb = ''
ghost = ''
guser = ''
gpassword = ''
gdatabase = ''
conn = ''
engine = ''



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


def execute_sql(sql_str, conn):
    cursor = conn.cursor()
    cursor.execute(sql_str)
    conn.commit()



def search_sql(sql_str):
    s = pd.read_sql(sql_str, conn)
    return s



def to_sql(df, table_name):
    try:
        df.to_sql(table_name, engine, if_exists='append')
    except IOError as e:
        print('to sql error! \n ' + e)

set_sql('mysql', '172.16.8.184', 'qc_data', 'wisesoe.qc', 'qc_data')
data1 = search_sql('select * from industry where field3 = "2017/1/4"')
indu = pd.DataFrame({'code':data1['field2'],'indu':data1['field4']})

data2 = search_sql('select qtid,mktCap,ret,turnover from marketData where date="2011-01-04"')
print data2