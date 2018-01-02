# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 16:32:18 2017

@author: 何友鑫
"""
import pandas as pd
from sqlalchemy import create_engine
import pymysql 
ghost='localhost'
guser='root'
gpassword='123456'
gdatabase='patent'
conn=''
engine=''

def set_sql(ghost,guser,gpassword,gdatabase):
    global host,user,password,database,engine,conn
    host=ghost
    user=guser
    password=gpassword
    database=gdatabase
    engine=set_engine()
    conn=set_conn()

def set_engine():
    engine = create_engine('mysql+pymysql://'+user+':'+password+'@'+host+'/'+
                           database+'?driver=Adaptive Server Enterprise')
    return engine

def set_conn():
    conn = pymysql.connect(host=host,user=user,password=password,
                           database=database,charset="utf8")
    return conn

def execute_sql(sql_str,conn):
    cursor = conn.cursor()
    cursor.execute(sql_str)
    cursor.close()
    conn.commit()

def search_sql(sql_str):
    s=pd.read_sql(sql_str,conn)
    return s

def getData(database,tablename):
    var = ' * '
    set_sql(ghost,guser,gpassword,gdatabase)
    s_1 = 'select '
    s_2 = var
    s_3 = ' from '
    s_4 = tablename
    #s_5 = ' where date >='
    #s_6 = start
    #s_7 = ' and date<= '
    #s_8 = end
    s = ''.join([s_1,s_2,s_3,s_4])
    #print s
    res = search_sql(s)
    return res


####就这两个是有用的
set_sql(ghost,guser,gpassword,gdatabase)
#execute_sql("update new_table set new_tablecol='a' where idnew_table=1 ",conn)
#execute_sql("update new_table set new_tablecol='b' where idnew_table=2 ",conn)
#execute_sql("update new_table set new_tablecol='c' where idnew_table=3 ",conn)

s=pd.read_sql("select 名称 from wg_2011_2016_2",conn)
print (s)

conn.close()


