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

data=pd.read_sql("select count(*) patent_num,city,appliyear from 1985_2011_patent where  type=1 and author='1' and category like 'A61%' and appliyear<2014 AND `foreign`=0 and apprdate<'2011/01/01' \
 group by appliyear,city \
union \
select count(*) patent_num,city,appliyear from sq_2011_2016_2 where  type=1 and author='1' and category like 'A61%' and appliyear<2014 \
 AND `foreign`=0  group by appliyear,city ",conn)


conn.close()


data.to_csv("C:/Users/heyouxin/Desktop/patent_city_year.csv",encoding='gbk', index=False)




