#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 15:59:03 2018

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
ret11 = search_sql('select * from CAPM where qtid="000659.SZ"')
import matplotlib.pyplot as plt
plt.subplot(211)
kk1 = ret11['residStdErr']
#kk1 = ret11['beta']
kk1.index = ret11['date']
kk1.plot()
plt.scatter(datetime.date(2015, 5, 28),float(ret11[ret11['date']==datetime.date(2015,5,28)]
            ['residStdErr']),c='r',s=100)
plt.scatter(datetime.date(2017,3,28),
            float(ret11[ret11['date']==datetime.date(2017,3,28)]
            ['residStdErr']),c='r',s=100)

plt.subplot(212)
se1 = pd.Series(list(rational1.sort_values('date')['factor'].rolling(30).mean()))
se1.index = j
se1.plot.line()
plt.scatter(datetime.date(2015, 5, 28),1,c='r',s=100)
plt.scatter(datetime.date(2017, 3, 1),1,c='r',s=100)


def de(string):
    return datetime.datetime.strptime(string,'%Y-%m-%d')