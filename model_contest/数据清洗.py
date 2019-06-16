# -*- coding: utf-8 -*-
"""
Created on Tue Aug 28 09:42:21 2018

@author: 何友鑫
"""

import pandas as pd
import re
import numpy as np


#省市对照字典
province_city=pd.read_excel('city.xlsx')
pro_ci=province_city[['province_cn','city_cn']]
pro_ci=pro_ci.drop_duplicates().reset_index()
pro_ci=pro_ci[['province_cn','city_cn']]
pro_ci['city_cn']=pro_ci['city_cn'].map(lambda x:x.replace('市',''))




#从标题提取地区填充
data=pd.read_excel('爬虫后数据.xlsx')
#data.reset_index()
df_region_na=data[data['city'].isin([np.nan]) & data['province'].isin([np.nan])]




for i in range(0,len(df_region_na['province'])):
    for j in range(0,len(pro_ci['province_cn'])):
        #data[re.search(pro_ci.loc[j,'province_cn'],data.loc['页面标题']),'province']=pro_ci.loc[j,'province_cn']
        try:
            if(re.search(pro_ci.loc[j,'province_cn'],df_region_na.loc[i,'页面标题'])):
                df_region_na.loc[i,'province']=pro_ci.loc[j,'province_cn']
        except:
            pass
        try:
            if(re.search(pro_ci.loc[j,'city_cn'],df_region_na.loc[i,'页面标题'])):
                df_region_na.loc[i,'city']=pro_ci.loc[j,'city_cn'] 
        except:
            pass
#df=pd.merge(data_all,df_region_na,how='left')
data=data.combine_first(df_region_na)



#用已知市填充省
#data.loc[0,'city']='武汉'
for i in range(0,len(pro_ci['province_cn'])):
    data.loc[data['province'].isin([np.nan]) & (data['city']==pro_ci.loc[i,'city_cn']) ,'province']=pro_ci.loc[i,'province_cn']
   
data=pd.read_excel('region_fill.xlsx')





'''
#爬虫错误数据处理
df=pd.read_excel('scrape_final.xlsx')

df2=df[(~df['classify_1'].isin(['找律师','法律咨询','法律知识','',np.nan,'法律咨询专题'])) & (df['网页类别']==1999001)]
df3=df[~((~df['classify_1'].isin(['找律师','法律咨询','法律知识','',np.nan,'法律咨询专题'])) & (df['网页类别']==1999001))]


df2['classify_3']=df2['classify_2']
df2['classify_2']=df2['classify_1']
df2['classify_1']='法律咨询专题'

data_all=pd.concat([df3,df2])

data_all=data_all.sort_index()

data_all.to_excel('data_final.xlsx',index=False,encoding='utf8')

'''


'''
#同一个用户号的地区填充
groupby_khh=data.groupby('用户号')

len(groupby_khh)

df1=data.loc[0:2,:]


df1['用户号']=df1['用户号'].map(lambda x:str(x))
if (len(df1.loc[~df1['province'].isin([np.nan]),'province']))==1:
    df1['province']=df1['province'].fillna(df1.loc[~df1['province'].isin([np.nan]),'province'].tolist()[0])
else:
    df1['province']=df1['province'].fillna(df1.loc[~df1['province'].isin([np.nan]),'province'][0])
if (len(df1.loc[~df1['city'].isin([np.nan]),'city']))==1:
    df1['city']=df1['city'].fillna(df1.loc[~df1['city'].isin([np.nan]),'city'].tolist()[0])
else:
    df1['city']=df1['city'].fillna(df1.loc[~df1['city'].isin([np.nan]),'city'][0])

'''
'''
data_all=pd.DataFrame()
i=0
for name,df1 in groupby_khh:
 
    try:
        if (len(df1.loc[~df1['province'].isin([np.nan]),'province']))==1:
            df1['province']=df1['province'].fillna(df1.loc[~df1['province'].isin([np.nan]),'province'].tolist()[0])
        else:
            df1['province']=df1['province'].fillna(df1.loc[~df1['province'].isin([np.nan]),'province'][0])
    except:
        pass
    try:
        if (len(df1.loc[~df1['city'].isin([np.nan]),'city']))==1:
            df1['city']=df1['city'].fillna(df1.loc[~df1['city'].isin([np.nan]),'city'].tolist()[0])
        else:
            df1['city']=df1['city'].fillna(df1.loc[~df1['city'].isin([np.nan]),'city'][0])
    except:
        pass
        
    if i==0:
        data_all=df1
        i+=1
    else:
        data_all=pd.concat([data_all,df1])


data_all=data_all.sort_index()

data_all.to_excel('region_fill_final.xlsx',index=False,encoding='utf8')
'''


#关键词填充,用已知关键词词库填充
df_keword_na=data[data['关键词'].isin([np.nan])]
key_word=list(data['关键词'])
n=0
#data[np.isnan(data.loc(5,data['关键词']))]
for i in range(0,len(df_keword_na['页面标题'])):
        for j in range(0,len(key_word)): 
            try:
                if(re.search(key_word[j],df_keword_na.loc[i,'页面标题'])):
                    df_keword_na.loc[i,'关键词']=key_word[j]
                    n+=1
            except:
                pass
       
print(n)

    
    
