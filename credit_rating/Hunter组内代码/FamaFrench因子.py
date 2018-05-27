#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 27 21:07:24 2018

@author: macbook
"""

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
        
'''
data = pd.read_excel('/Users/macbook/Desktop/factor.xls')


fin = pd.DataFrame({'date':data[data.columns[0]],
                    'RMRF':data[data.columns[1]],
                    'SMB':data[data.columns[2]],
                    'HML':data[data.columns[3]]})
'''
import string 
#data = pd.read_excel('/Users/macbook/Desktop/BND_Yldcurve.xls',skiprows=[1,2])
data = open('/Users/macbook/Desktop/BND_TreasYield.txt')
res = []
for i in data:
    date = i[0:10]
    spot = i[11]
    tomaturity = str(float(i[12:19].replace('\t','')))
    #print tomaturity
    rate = float(str(i[20:27].replace('\t','')))
    res.append([date,spot,tomaturity,rate])
kk = pd.DataFrame(res,columns=['date','type','maturity','rate'])
kk.groupby('date').get_group('2013-12-24').iloc[6:]['rate'].plot()
a3 = 100*kk.groupby('maturity').get_group('30.0')['rate']
a2 = 100*kk.groupby('maturity').get_group('10.0')['rate']
a1 = 100*kk.groupby('maturity').get_group('1.0')['rate']
kk1 = np.array(a1.diff())
kk2 = np.array(a2.diff())
kk3 = np.array(a3.diff())
test = pd.DataFrame([kk1,kk2,kk3]).T
level = map(float,((test[0]>0)&(test[1]>0)&(test[0]>0)) | 
((test[0]<0)&(test[1]<0)&(test[0]<0)))
slope = map(float,((test[2]-test[0])>0)|( ((test[2]-test[0])<0)))
cur= map(float,(((test[2]-test[1])>0)&((test[2]-test[1])>0) | ((test[2]-test[1])>0)&((test[2]-test[1])>0)))
print pd.DataFrame([level,slope,cur]).T.describe ()
#pd.Series(np.abs(kk1-kk2)+np.abs(kk3-kk2)).plot()

#set_sql('mysql', '172.16.8.184', 'qc_data', 'wisesoe.qc', 'qc_data')
#to_sql(kk,'intrate')
#data = search_sql('select * from induindex')
#print data