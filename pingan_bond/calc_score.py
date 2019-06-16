# -*- coding: utf-8 -*-
"""

-------------------------------------------------
   File Name：        calc_score
   Description :
   Author :           何友鑫
   date：             2018-08-28
   latest version:    v1.0.0
-------------------------------------------------
   Change Log:
    v1.0.0            hyx        2018-08-28
    1.
-------------------------------------------------

"""

import pandas as pd

data_all=pd.DataFrame
i=0
for d in ['20170401','20170701','20180101','20180401','20180701']:
    str1='scores_rolling_'
    str2='.xlsx'
    filename=str1+d+str2
    df=pd.read_excel(filename,index=False)
    df['ID'] = df['code'].map(lambda x: str(x)) + df['date'].map(lambda x: str(x))

    df['total_score'] = df['total_score'].map(lambda x: int(x))
    df['score_basepoint'] = df['score_basepoint'].map(lambda x: int(x))
    df['score_info'] = df['score_info'].map(lambda x: int(x))
    df['score_macro'] = df['score_macro'].map(lambda x: int(x))
    df['score_industry'] = df['score_industry'].map(lambda x: int(x))
    df['score_finance'] = df['score_finance'].map(lambda x: int(x))

    df['total_score']=df['total_score']+df['score_basepoint']
    df['score_info']=df['score_info']+df['score_basepoint']/2
    df['score_macro'] = df['score_macro'] + df['score_basepoint'] / 6
    df['score_industry'] = df['score_industry'] + df['score_basepoint'] / 6
    df['score_finance']= df['score_finance'] + df['score_basepoint'] / 6


    df['total_score'] = df['total_score'].map(lambda x: int(x))
    df['score_basepoint'] = df['score_basepoint'].map(lambda x: int(x))
    df['score_info'] = df['score_info'].map(lambda x: int(x))
    df['score_macro'] = df['score_macro'].map(lambda x: int(x))
    df['score_industry'] = df['score_industry'].map(lambda x: int(x))
    df['score_finance'] = df['score_finance'].map(lambda x: int(x))
    df['news']=0
    df['law']=0
    df=df[['ID','code','date','is_default','prob','y_predit','score_basepoint','score_info','score_macro','score_industry','score_finance','news','law','total_score']]
    if i==0:
        data_all=df
        i+=1
    data_all=pd.concat([data_all,df])

data_all.to_csv('score_data.csv',index=False,encoding='utf8')