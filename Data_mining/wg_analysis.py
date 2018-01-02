# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 16:32:18 2017

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

s=pd.read_sql("select 名称 from wg_2011_2016_2 UNION select 名称 from wg_2011_2016_1",conn)
print (s)
conn.close()
s_str=str(s)

wordcloud = WordCloud(background_color="white",font_path='C:\Windows\Fonts\STZHONGS.TTF',width=1000, height=860, margin=2).generate(s_str)
# width,height,margin可以设置图片属性
# generate 可以对全部文本进行自动分词,但是他对中文支持不好,对中文的分词处理请看我的下一篇文章
#wordcloud = WordCloud(font_path = r'D:\Fonts\simkai.ttf').generate(f)
# 你可以通过font_path参数来设置字体集
#background_color参数为设置背景颜色,默认颜色为黑色
plt.imshow(wordcloud)
plt.axis("off")
plt.show()


