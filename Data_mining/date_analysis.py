# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 16:58:56 2017

@author: 何友鑫
"""

import pandas as pd
from sqlalchemy import create_engine
import pymysql

#词云包
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import jieba
import numpy as np
 
 
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




####就这两个是有用的
set_sql(ghost,guser,gpassword,gdatabase)
#execute_sql("update new_table set new_tablecol='a' where idnew_table=1 ",conn)
#execute_sql("update new_table set new_tablecol='b' where idnew_table=2 ",conn)
#execute_sql("update new_table set new_tablecol='c' where idnew_table=3 ",conn)

#date_data=pd.read_sql("select 公开（公告）日 , 申请日 from sq_2011_2016 where 主分类号 like 'A61%' AND 申请来源='国家'   ",conn)
#print (s)

date_data=pd.read_sql("select 公开（公告）日 , 申请日 from sq_2011_2016 where 主分类号 like 'A61%' AND 申请来源='国家' and 国省代码!='美国;US' and 国省代码!='日本;JP' and 国省代码!='中国台湾;71' and 国省代码!='法国;FR' and 国省代码!='瑞士;CH' and 国省代码!='韩国;KR' and 国省代码!='德国;DE' and 国省代码!='以色列;IL'   \
union select apprdate,applidate from 1985_2011_patent where  type=1 and author='1' and category like 'A61%' AND `foreign`=0 and apprdate<'2011/01/01' ",conn)


conn.close()


dd=date_data


dd['授权期']=pd.to_datetime(dd['公开（公告）日'])-pd.to_datetime(dd['申请日'])

SQQ=dd['授权期']
SQQ[1].days
SQQ.mean()
SQQ.max()
SQQ.median()

l1=list()
for i in range(1,101,1):
    i=i/100
    q=SQQ.quantile(i)
    l1.append(q.days)


import matplotlib.pyplot as plt
x=range(1,101)
plt.plot(x,l1)

SQQ.quantile(0.8)

