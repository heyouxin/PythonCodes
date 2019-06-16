# -*- coding: utf-8 -*-
"""
Created on Tue Aug 28 21:02:45 2018

@author: 何友鑫
"""

import pandas as pd
import numpy as np
from datetime import datetime
   
df=pd.read_excel('data_final_2.xlsx')



df['网页时间'] = pd.to_datetime(df['网页时间'])

df['year'] = df.网页时间.dt.year
df['year'].head()

df['year']=df['year'].fillna(0).astype(int)

#提取月份
df['month'] = df.网页时间.dt.month
df['month'].head()
df['month']=df['month'].fillna(0).astype(int)
 
#提取日
df['day'] = df.网页时间.dt.day
df['day'].head()

df['province']=df['province'].map(lambda x: str(x).strip())



'''
##################################################################
省份分析
'''
group_key='province'
regroup=df.groupby(group_key)
len(regroup)

data_pro_all=pd.DataFrame()
      
province=[]
        
max_site=[]
max_site_num=[]

max_tag=[]
max_tag_num=[]

second_tag=[]
second_tag_num=[]

third_tag=[]
third_tag_num=[]

max_keyword=[]
max_keyword_num=[]

max_classify_1=[]
max_classify_1_num=[]
       

max_classify_2=[]
max_classify_2_num=[]
       

max_classify_3=[]
max_classify_3_num=[]
       


for name,g in regroup:
    province.append(name) 
    
    max_site.append(g['来源网站'].value_counts().index[0])
    max_site_num.append(g['来源网站'].value_counts()[0])
      
    
    max_tag.append(g['标签'].value_counts().index[0])
    max_tag_num.append(g['标签'].value_counts()[0])
    
    try:
        second_tag.append(g['标签'].value_counts().index[1])
        second_tag_num.append(g['标签'].value_counts()[1])
        
        
        third_tag.append(g['标签'].value_counts().index[2])
        third_tag_num.append(g['标签'].value_counts()[2])
    except:
        second_tag.append(np.nan)
        second_tag_num.append(np.nan)
        
        third_tag.append(np.nan)
        third_tag_num.append(np.nan)

    max_keyword.append(g['关键词'].value_counts().index[0])
    max_keyword_num.append(g['关键词'].value_counts()[0])
    
    try:
        max_classify_1.append(g['classify_1'].value_counts().index[0])
        max_classify_1_num.append(g['classify_1'].value_counts()[0])
        
        max_classify_2.append(g['classify_2'].value_counts().index[0])
        max_classify_2_num.append(g['classify_2'].value_counts()[0])
        
        max_classify_3.append(g['classify_3'].value_counts().index[0])
        max_classify_3_num.append(g['classify_3'].value_counts()[0])
    except:
        max_classify_1.append(np.nan)
        max_classify_1_num.append(np.nan)
        
        max_classify_2.append(np.nan)
        max_classify_2_num.append(np.nan)
        
        max_classify_3.append(np.nan)
        max_classify_3_num.append(np.nan)
        
d={'省份':province,'最多来源网站':max_site,'来源网站最大数':max_site_num,\
'最多标签':max_tag,'标签最大数':max_tag_num,\
'第二多标签':second_tag,'标签第二大数':second_tag_num,\
'第三多标签':third_tag,'标签第三大数':third_tag_num,\
   '最多关键词':max_keyword,'关键词最大数':max_keyword_num,\
   '最多一级分类':max_classify_1,'一级分类最大数':max_classify_1_num,\
   '最多二级分类':max_classify_2,'二级分类最大数':max_classify_2_num,\
   '最多三级分类':max_classify_3,'三级分类最大数':max_classify_3_num}
data_pro_all=pd.DataFrame(d) 
data_pro_all=data_pro_all[['省份','最多来源网站','来源网站最大数','最多标签','标签最大数',\
'第二多标签','标签第二大数','第三多标签','标签第三大数','最多关键词','关键词最大数',\
 '最多一级分类','一级分类最大数','最多二级分类','二级分类最大数','最多三级分类','三级分类最大数']]
    
data_pro_all2=data_pro_all.loc[1:34,['省份','最多标签','标签最大数',\
'第二多标签','标签第二大数','第三多标签','标签第三大数','最多关键词','关键词最大数',\
 '最多一级分类','一级分类最大数','最多二级分类','二级分类最大数','最多三级分类','三级分类最大数']]
 
data_pro_all.to_excel('省分析.xlsx',index=False,encoding='utf8')

'''
####################################################################################
年份分析
'''


group_key='year'
regroup=df.groupby(group_key)
len(regroup)

data_pro_all=pd.DataFrame()
      
year=[]
        
max_site=[]
max_site_num=[]

max_tag=[]
max_tag_num=[]

second_tag=[]
second_tag_num=[]

third_tag=[]
third_tag_num=[]

max_keyword=[]
max_keyword_num=[]

max_classify_1=[]
max_classify_1_num=[]
       

max_classify_2=[]
max_classify_2_num=[]
       

max_classify_3=[]
max_classify_3_num=[]
       


for name,g in regroup:
    year.append(name)
     
        
    
    
    max_site.append(g['来源网站'].value_counts().index[0])
    max_site_num.append(g['来源网站'].value_counts()[0])
      
    
    max_tag.append(g['标签'].value_counts().index[0])
    max_tag_num.append(g['标签'].value_counts()[0])
    
    try:
        second_tag.append(g['标签'].value_counts().index[1])
        second_tag_num.append(g['标签'].value_counts()[1])
        
        
        third_tag.append(g['标签'].value_counts().index[2])
        third_tag_num.append(g['标签'].value_counts()[2])
    except:
        second_tag.append(np.nan)
        second_tag_num.append(np.nan)
        
        third_tag.append(np.nan)
        third_tag_num.append(np.nan)

    max_keyword.append(g['关键词'].value_counts().index[0])
    max_keyword_num.append(g['关键词'].value_counts()[0])
    
    try:
        max_classify_1.append(g['classify_1'].value_counts().index[0])
        max_classify_1_num.append(g['classify_1'].value_counts()[0])
        
        max_classify_2.append(g['classify_2'].value_counts().index[0])
        max_classify_2_num.append(g['classify_2'].value_counts()[0])
        
        max_classify_3.append(g['classify_3'].value_counts().index[0])
        max_classify_3_num.append(g['classify_3'].value_counts()[0])
    except:
        max_classify_1.append(np.nan)
        max_classify_1_num.append(np.nan)
        
        max_classify_2.append(np.nan)
        max_classify_2_num.append(np.nan)
        
        max_classify_3.append(np.nan)
        max_classify_3_num.append(np.nan)
        
d={'年份':year,'最多来源网站':max_site,'来源网站最大数':max_site_num,\
'最多标签':max_tag,'标签最大数':max_tag_num,\
'第二多标签':second_tag,'标签第二大数':second_tag_num,\
'第三多标签':third_tag,'标签第三大数':third_tag_num,\
   '最多关键词':max_keyword,'关键词最大数':max_keyword_num,\
   '最多一级分类':max_classify_1,'一级分类最大数':max_classify_1_num,\
   '最多二级分类':max_classify_2,'二级分类最大数':max_classify_2_num,\
   '最多三级分类':max_classify_3,'三级分类最大数':max_classify_3_num}
data_pro_all=pd.DataFrame(d) 
data_pro_all=data_pro_all[['年份','最多来源网站','来源网站最大数','最多标签','标签最大数',\
'第二多标签','标签第二大数','第三多标签','标签第三大数','最多关键词','关键词最大数',\
 '最多一级分类','一级分类最大数','最多二级分类','二级分类最大数','最多三级分类','三级分类最大数']]

data_pro_all['年份']=data_pro_all['年份'].map(lambda x:int(x))


data_pro_all.to_excel('年份分析.xlsx',index=False,encoding='utf8')
'''
#########################################################################################
月份分析
'''



group_key='month'
regroup=df.groupby(group_key)
len(regroup)

data_pro_all=pd.DataFrame()
      
month=[]
        
max_site=[]
max_site_num=[]

max_tag=[]
max_tag_num=[]

second_tag=[]
second_tag_num=[]

third_tag=[]
third_tag_num=[]

max_keyword=[]
max_keyword_num=[]

max_classify_1=[]
max_classify_1_num=[]
       

max_classify_2=[]
max_classify_2_num=[]
       

max_classify_3=[]
max_classify_3_num=[]
       


for name,g in regroup:
    month.append(name)
     
        
    
    
    max_site.append(g['来源网站'].value_counts().index[0])
    max_site_num.append(g['来源网站'].value_counts()[0])
      
    
    max_tag.append(g['标签'].value_counts().index[0])
    max_tag_num.append(g['标签'].value_counts()[0])
    
    try:
        second_tag.append(g['标签'].value_counts().index[1])
        second_tag_num.append(g['标签'].value_counts()[1])
        
        
        third_tag.append(g['标签'].value_counts().index[2])
        third_tag_num.append(g['标签'].value_counts()[2])
    except:
        second_tag.append(np.nan)
        second_tag_num.append(np.nan)
        
        third_tag.append(np.nan)
        third_tag_num.append(np.nan)

    max_keyword.append(g['关键词'].value_counts().index[0])
    max_keyword_num.append(g['关键词'].value_counts()[0])
    
    try:
        max_classify_1.append(g['classify_1'].value_counts().index[0])
        max_classify_1_num.append(g['classify_1'].value_counts()[0])
        
        max_classify_2.append(g['classify_2'].value_counts().index[0])
        max_classify_2_num.append(g['classify_2'].value_counts()[0])
        
        max_classify_3.append(g['classify_3'].value_counts().index[0])
        max_classify_3_num.append(g['classify_3'].value_counts()[0])
    except:
        max_classify_1.append(np.nan)
        max_classify_1_num.append(np.nan)
        
        max_classify_2.append(np.nan)
        max_classify_2_num.append(np.nan)
        
        max_classify_3.append(np.nan)
        max_classify_3_num.append(np.nan)
        
d={'月份':month,'最多来源网站':max_site,'来源网站最大数':max_site_num,\
'最多标签':max_tag,'标签最大数':max_tag_num,\
'第二多标签':second_tag,'标签第二大数':second_tag_num,\
'第三多标签':third_tag,'标签第三大数':third_tag_num,\
   '最多关键词':max_keyword,'关键词最大数':max_keyword_num,\
   '最多一级分类':max_classify_1,'一级分类最大数':max_classify_1_num,\
   '最多二级分类':max_classify_2,'二级分类最大数':max_classify_2_num,\
   '最多三级分类':max_classify_3,'三级分类最大数':max_classify_3_num}
data_pro_all=pd.DataFrame(d) 
data_pro_all=data_pro_all[['月份','最多来源网站','来源网站最大数','最多标签','标签最大数',\
'第二多标签','标签第二大数','第三多标签','标签第三大数','最多关键词','关键词最大数',\
 '最多一级分类','一级分类最大数','最多二级分类','二级分类最大数','最多三级分类','三级分类最大数']]

data_pro_all.to_excel('月份分析.xlsx',index=False,encoding='utf8')

'''
######################################################################################
省份+年份
'''
group_key=['province','year']
regroup=df.groupby(group_key)
#len(regroup)

data_pro_all=pd.DataFrame()
      
province=[]
year=[]
        
max_site=[]
max_site_num=[]

max_tag=[]
max_tag_num=[]

second_tag=[]
second_tag_num=[]

third_tag=[]
third_tag_num=[]

max_keyword=[]
max_keyword_num=[]

max_classify_1=[]
max_classify_1_num=[]
       

max_classify_2=[]
max_classify_2_num=[]
       

max_classify_3=[]
max_classify_3_num=[]
       


for (name,y),g in regroup:
    province.append(name)
    year.append(y)
    
    max_site.append(g['来源网站'].value_counts().index[0])
    max_site_num.append(g['来源网站'].value_counts()[0])
      
    
    max_tag.append(g['标签'].value_counts().index[0])
    max_tag_num.append(g['标签'].value_counts()[0])
    
    try:
        second_tag.append(g['标签'].value_counts().index[1])
        second_tag_num.append(g['标签'].value_counts()[1])
    except:
        second_tag.append(np.nan)
        second_tag_num.append(np.nan)  
        
    try:   
        third_tag.append(g['标签'].value_counts().index[2])
        third_tag_num.append(g['标签'].value_counts()[2])

    except:
        third_tag.append(np.nan)
        third_tag_num.append(np.nan)
    try:
        max_keyword.append(g['关键词'].value_counts().index[0])
        max_keyword_num.append(g['关键词'].value_counts()[0])
    except:
        max_keyword.append(np.nan)
        max_keyword_num.append(np.nan)
    
    try:
        max_classify_1.append(g['classify_1'].value_counts().index[0])
        max_classify_1_num.append(g['classify_1'].value_counts()[0])
        
        max_classify_2.append(g['classify_2'].value_counts().index[0])
        max_classify_2_num.append(g['classify_2'].value_counts()[0])
        
        max_classify_3.append(g['classify_3'].value_counts().index[0])
        max_classify_3_num.append(g['classify_3'].value_counts()[0])
    except:
        max_classify_1.append(np.nan)
        max_classify_1_num.append(np.nan)
        
        max_classify_2.append(np.nan)
        max_classify_2_num.append(np.nan)
        
        max_classify_3.append(np.nan)
        max_classify_3_num.append(np.nan)
        
d={'省份':province,'年份':year,'最多来源网站':max_site,'来源网站最大数':max_site_num,\
'最多标签':max_tag,'标签最大数':max_tag_num,\
'第二多标签':second_tag,'标签第二大数':second_tag_num,\
'第三多标签':third_tag,'标签第三大数':third_tag_num,\
   '最多关键词':max_keyword,'关键词最大数':max_keyword_num,\
   '最多一级分类':max_classify_1,'一级分类最大数':max_classify_1_num,\
   '最多二级分类':max_classify_2,'二级分类最大数':max_classify_2_num,\
   '最多三级分类':max_classify_3,'三级分类最大数':max_classify_3_num}
data_pro_all=pd.DataFrame(d) 
data_pro_all=data_pro_all[['省份','年份','最多来源网站','来源网站最大数','最多标签','标签最大数',\
'第二多标签','标签第二大数','第三多标签','标签第三大数','最多关键词','关键词最大数',\
 '最多一级分类','一级分类最大数','最多二级分类','二级分类最大数','最多三级分类','三级分类最大数']]
data_pro_all['年份']=data_pro_all['年份'].map(lambda x:int(x))
data_pro_all=data_pro_all.sort_values(by=['省份', '年份'])

data_pro_all.to_excel('省_年份分析.xlsx',index=False,encoding='utf8')
