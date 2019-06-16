# -*- coding: utf-8 -*-
"""

-------------------------------------------------
   File Name：        default_bond_update
   Description :
   Author :           何友鑫
   Create date：      2018-10-17
   Latest version:    v1.0.0
-------------------------------------------------
   Change Log:
#-----------------------------------------------#
    v1.0.0            hyx        2018-10-17
    1.
#-----------------------------------------------#
-------------------------------------------------

"""
import pandas as pd

def renameColumn(df):
    d1 = {'code':'代码','date_default':'发生日期','event':'事件摘要','rate_history':'评级历史','balance_100million':'债券余额(亿元)'}
    d2 = dict([(v,k) for (k,v) in d1.items()])
    df = df.rename(columns=d2)
    return(df)

default_bond_lateset = pd.read_excel('raw_data/违约债券报表.xlsx')

#default_bond_sql = pd.read_excel('data_sql/default_1009.xlsx')

#default_bond_lateset =  default_bond_lateset.loc[0:(len(default_bond_lateset)-3),:]

#default_bond_lateset.loc[default_bond_lateset.代码[0:(len(default_bond_lateset)-)].isin(default_bond_sql.code),:]

default_need_update = default_bond_lateset.loc[0:(len(default_bond_lateset)-3),['代码','发生日期','事件摘要','评级历史','债券余额(亿元)']]

default_need_update = renameColumn(default_need_update)

jys = ['.SH','.SZ','.IB','.sh','.sz']

#default_need_update[len(default_need_update.code)-3:len(default_need_update.code)  in jys ]


default_need_update['valid_bond'] = default_need_update.apply(lambda x: 1 if (x.code[(len(x.code)-3):len(x.code)]  in jys) else 0,axis=1)

default_bond = default_need_update[default_need_update.valid_bond == 1].reset_index().drop('valid_bond',1).drop('index',1)

default_bond.to_excel('data_sql/default.xlsx',index=False,encoding='utf8')


bond_info = pd.read_excel('data_sql/bond_info.xlsx')
not_in = default_bond[~default_bond.code.isin(bond_info.code)].reset_index().drop('index',1)

not_in.to_excel('raw_data/default_not_in_bond_info.xlsx',index=False,encoding='utf8')


#default_bond_sql = pd.concat([default_bond_sql,default_need_update]).sort_values(by='date_default',axis=0) .reset_index().drop('index',1)