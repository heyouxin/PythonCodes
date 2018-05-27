
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import pandas as pd
import numpy as np

data = pd.read_csv('/Users/macbook/Desktop/listcom.csv')
def transfer1(x):
    con = []
    for i in x:
        if len(str(i))<6:
            con.append('0'*(6-len(str(i)))+str(i))
        else:
            con.append(str(i))
    return con
def transfer2(x):
    con = []
    for i in x:
        con.append(i.encode('utf-8'))
    return con
names = pd.DataFrame({'code':transfer1(data[data.columns[0]]),
                      'fullname':data[data.columns[2]]})
#!/usr/bin/env python2
# -*- coding: utf-8 -*-



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

set_sql('mysql','210.34.5.184','group1','Group1.321','group1')
data2 = search_sql('select * from static_institution')

data3 = pd.DataFrame({'fullname':transfer2(list(data2['fullname'])),
                    'default':list(data2['default_num']),
                    'id':data2['institution_id']})

'''
data2 = pd.read_csv('/Volumes/qianchen/static_institution.csv',header=None)
'''
#data3 = pd.DataFrame({'codess':data2[1],'name':data2[3],'default':data2[2]}).dropna()
a = pd.merge(names,data3,on=['fullname'])

print a[a['default']!='0']

#for i in pd.Series(list(set(data3['name'])-set(a['name']))):
#    print i#