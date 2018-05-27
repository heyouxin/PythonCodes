# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 14:43:50 2018

@author: 何友鑫

latest version: V2.0.0

-----------------------

v2.0.0   by hyx   2018.3.6
changelog: 
1.change the function :add_report_year
2.get data from imported table “pyindic2.csv”
3.pass the functions:"finance_indic"and "logistic_regression"
4.add function:add_indic


v1.0.0   by hyx
changelog: 
1.preparation:copy the remote server database to localhost , and create index for the database in order to acceleration
2.create functions: set_sql  add_report_year  finance_indic  logistic_regression


-----------------------

"""


import pandas as pd
from sqlalchemy import create_engine
import pymysql 
from datetime import datetime
import re
from sklearn.linear_model.logistic import LogisticRegression
import numpy as np
import math as m
'''
ghost='210.34.5.184'
guser='group1'
gpassword='Group1.321'
gdatabase='group1'
conn=''
engine=''
'''
gdb = 'mysql'
ghost='localhost'
guser='root'
gpassword='123456'
gdatabase='group1'
conn=''
engine=''


def set_sql(gdb,ghost,guser,gpassword,gdatabase):
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




#1.关联查询static_bond与bond_default 得到所需债券合约信息
#2.表中加入上市年份、退市年份
def add_report_year():
    set_sql(gdb,ghost,guser,gpassword,gdatabase)
    df_static_bond=pd.read_sql('select A.security_id,A.institution_id,A.fullname,A.`default`,A.listed_date,A.delisted_date,B.default_ann_date,B.is_bond_default from static_bond A LEFT JOIN bond_default B ON (A.security_id = B.security_id)',conn)
    conn.close()
    df_static_bond2=df_static_bond
    df_static_bond2['listed_year']=''
    df_static_bond2['delisted_year']=''
    for i in range (0,len(df_static_bond2)):
        #如果上市日期为空
        if df_static_bond2['listed_date'][i]=='':
            p = re.compile(r'\d+')
            if p.findall(df_static_bond2['fullname'][i]) != []:
                if len(p.findall(df_static_bond2['fullname'][i])[0])==2 and int(p.findall(df_static_bond2['fullname'][i])[0])>80 and int(p.findall(df_static_bond2['fullname'][i])[0])<=99 :
                    df_static_bond2['listed_year'][i]='19'+ p.findall(df_static_bond2['fullname'][i])[0]
                else:                   
                    df_static_bond2['listed_year'][i]=p.findall(df_static_bond2['fullname'][i])[0]
            #如果从fullname里找不到年份的话
            else:
                pass
        #如果上市日期不为空
        else:
            df_static_bond2['listed_year'][i]=datetime.strftime(pd.to_datetime(df_static_bond2['listed_date'][i]),'%Y')
        
        if df_static_bond2['delisted_date'][i]=='':
            #如果没有退市日期的话。。。
            pass
        else:
            df_static_bond2['delisted_year'][i]=datetime.strftime(pd.to_datetime(df_static_bond2['delisted_date'][i]),'%Y')
  
            
        
    #检测异常数据 有两处
    #temp1=df_static_bond2[df_static_bond2.listed_date=='']
    print("listed_year:error-----")
    for t in range(0,len(df_static_bond2['listed_year'])):
        if len(df_static_bond2['listed_year'][t])<4:
            print(df_static_bond2['listed_year'][t])
            print(t)
        else:
            if int(df_static_bond2['listed_year'][t])<1980 or  int(df_static_bond2['listed_year'][t])>2020:
                print(df_static_bond2['listed_year'][t])
                print(t)
                
    #1836  1860行找不到上市日期，从fullname也提取不到 1860暂时先赋值2015
    df_static_bond2['listed_year'][1836]='2013'
    df_static_bond2['listed_year'][1860]='2015'
    #11133行原始数据数据错误，更正
    df_static_bond2['listed_year'][11133]='2014'
    
    print("delisted_year:error-----")      
    for t in range(0,len(df_static_bond2['delisted_year'])):
        if len(df_static_bond2['delisted_year'][t])<4:
            #print(df_static_bond2['delisted_year'][t])
            #print(t)
            df_static_bond2['delisted_year'][t]=df_static_bond2['listed_year'][t]
        else:
            if int(df_static_bond2['delisted_year'][t])<1980 or  int(df_static_bond2['delisted_year'][t])>2020:
                #print(df_static_bond2['delisted_year'][t])
                #print(t)               
                df_static_bond2['delisted_year'][t]=df_static_bond2['listed_year'][t]        
                   

                   
    return (df_static_bond2)

def add_indic(df_static_bond2):
    indic_value=pd.read_csv("C:/Users/heyouxin/Documents/PythonCodes/credit_rating/pyindic2.csv")
    indic_value= indic_value.rename(columns={'institutioin_id':'institution_id'})
    str1='_1'
    str2='_2'
    str3='_3'
    str4='_max'
    str5='_min'
    str6='_mean'
    #type(indic_value['institution_id'])
    
    #df_t_1=pd.DataFrame(columns=list(indic_value.columns.values[1:379]+str1))
    l_nan=[]
    for i in range(0,378):
        l_nan.append(np.nan)
    
    
    
    '''
    test:code
   record_t=indic_value[(indic_value['year']==2010) & (indic_value['institution_id']==10199999)].iloc[:,1:379].values
 
    
     record_t=indic_value[ (indic_value['institution_id']==10199999)].iloc[:,1:379].values
 
    
    list(record_t_1[0])
   
       & 
    indic_value[indic_value['year']==(int(df_static_bond2['listed_year'][0])-2) & indic_value['institution_id']==int(df_static_bond2['institution_id'][0])].iloc[:,1:379]
].iloc[:,1:379]
indic_value[(indic_value['year']==int(df_static_bond2['listed_year'][0])-2) & indic_value['institution_id']==int(df_static_bond2['institution_id'][0])]
   2010
    '''
 
    
    
    df_t_1=[]
    df_t_2=[]
    df_t_3=[]
    df_max=[]
    df_min=[]
    df_mean=[]

    for j in range(0,len(df_static_bond2)):   
        
        record_t_1=indic_value[(indic_value['year']==int(df_static_bond2['listed_year'][j])-1) & (indic_value['institution_id']==int(df_static_bond2['institution_id'][j]))].iloc[:,1:379].values
        #record_t_1=indic_value[(indic_value['year']==int(df_static_bond2['listed_year'][j])-2) & indic_value['institution_id']==int(df_static_bond2['institution_id'][j])].iloc[:,1:379]
        if(len(record_t_1)==0):
            df_t_1.append(l_nan)
        else:
            record_t_1=record_t_1[0]
            df_t_1.append(list(record_t_1))

        record_t_2=indic_value[(indic_value['year']==int(df_static_bond2['listed_year'][j])-2) & (indic_value['institution_id']==int(df_static_bond2['institution_id'][j]))].iloc[:,1:379].values
        if(len(record_t_2)==0):
            df_t_2.append(l_nan)
        else:
            record_t_2=record_t_2[0]
            df_t_2.append(list(record_t_2))

        record_t_3=indic_value[(indic_value['year']==int(df_static_bond2['listed_year'][j])-3) & (indic_value['institution_id']==int(df_static_bond2['institution_id'][j]))].iloc[:,1:379].values
        if(len(record_t_3)==0):
            df_t_3.append(l_nan)
        else:
            record_t_3=record_t_3[0]
            df_t_3.append(list(record_t_3))
        
            
            
        record_t=indic_value[(indic_value['year']>=int(df_static_bond2['listed_year'][j])) & (indic_value['year']<=int(df_static_bond2['delisted_year'][j])) & (indic_value['institution_id']==int(df_static_bond2['institution_id'][j]))].iloc[:,1:379]
        if(len(record_t)==0):
            df_max.append(l_nan)
            df_min.append(l_nan)
            df_mean.append(l_nan)
        else:
            df_max.append(list(record_t.max()))
            df_min.append(list(record_t.min()))
            df_mean.append(list(record_t.mean()))



    df_t_1=pd.DataFrame(df_t_1)
    df_t_1.columns=list(indic_value.columns.values[1:379]+str1)
      

    df_t_2=pd.DataFrame(df_t_2)
    df_t_2.columns=list(indic_value.columns.values[1:379]+str2)
                 
    df_t_3=pd.DataFrame(df_t_3)
    df_t_3.columns=list(indic_value.columns.values[1:379]+str3)
                                         
                              
    df_max=pd.DataFrame(df_max)
    df_max.columns=list(indic_value.columns.values[1:379]+str4)
      

    df_min=pd.DataFrame(df_min)
    df_min.columns=list(indic_value.columns.values[1:379]+str5)
                 
    df_mean=pd.DataFrame(df_mean)
    df_mean.columns=list(indic_value.columns.values[1:379]+str6)                            

    bond_indic=pd.merge(df_static_bond2,df_t_1,left_index=True,right_index=True,how='outer')
    bond_indic=pd.merge(bond_indic,df_t_2,left_index=True,right_index=True,how='outer')
    bond_indic=pd.merge(bond_indic,df_t_3,left_index=True,right_index=True,how='outer')
    bond_indic=pd.merge(bond_indic,df_max,left_index=True,right_index=True,how='outer')
    bond_indic=pd.merge(bond_indic,df_min,left_index=True,right_index=True,how='outer')
    bond_indic=pd.merge(bond_indic,df_mean,left_index=True,right_index=True,how='outer')

    bond_indic.to_csv("bond_indic.csv")


if __name__ == "__main__":
    df_bond=add_report_year()
    add_indic(df_bond)

'''
#财务指标构建  从basic_indic  indic_value两张表  按年份提取财务指标的均值  
def finance_indic(df_static_bond):
    #part 1 考察资产规模与质量的主要财务指标有： 
    #总资产和净资产规模          --   资产总计A0060
    #每股净资产和调整后的每股净资产 -- 每股资产J0001   调整后的没有
    #担保比率                     -- 找不到这个指标
    
    #part 2 考察公司资本结构和债务压力的主要指标有： 
    #资产负债率                    -- 资产负债率D0019
    #长期资产适合率                -- 无
    #调整后的有形资产负债率         -- 无
    #债务资本比率                  -- 无
    #长期资本化比率                -- 无
    #总资本化比率                  -- 无
    
    #part 3 考察企业盈利能力的指标主要有： 
    #主营业务收入、EBIT、EBITDA 规模；  -- 营业收入B0002 、EBIT D0024、 EBITDA D0025 
    #主营业务毛利率；                  -- 主营业务利润比F0002
    #净资产收益率；                    -- 净资产收益率H0001
    #资产回报率；                      -- 无
    #成本费用率                        -- 无
    
    #part 4考察现金流的主要指标有：  
    #现金流动负债比，即经营活动现金净流量与流动负债之比。 --   'D0032', '经营活动现金流量净额'    'A0085', '流动负债合计'
    #现金债务总额比，即经营活动现金净流量与负债总额之比。 --   'A0111', '负债合计'
    #经营活动现金净流量与到期债务本息比率，该指标揭示企业偿还到期债务本息的能力。 --无
    #EBITDA/利息支出                                 --利息支出B0024
    #EBITDA/短期债务                                 --无
    #FFO/总债务；                                    --无
    #自由现金流量/总债务；                            --'D0026' 'EBITDA全部债务比'

    indic_list=['A0060','J0001','D0019','B0002','D0024','D0025','F0002','H0001','D0032','A0085','A0111','B0024','D0026']
    indic_name=['total_asset','asset_per_stock','asset_debet_ratio','operation_revenue','EBIT','EBITDA','operation_profit_ratio','ROE','NCFO','Current_Liabilities','Liabilities','interest_expense','EBITDA_Liabilities_ratio']

    df_static_bond['total_asset']=''
    df_static_bond['asset_per_stock']=''
    df_static_bond['asset_debet_ratio']=''
    df_static_bond['operation_revenue']=''
    df_static_bond['EBIT']=''
    df_static_bond['EBITDA']=''
  
    df_static_bond['operation_profit_ratio']=''
    df_static_bond['ROE']=''
    df_static_bond['NCFO']=''
    df_static_bond['Current_Liabilities']=''
    df_static_bond['Liabilities']=''
    df_static_bond['interest_expense']=''
    
    df_static_bond['EBITDA_Liabilities_ratio']=''
    
    set_sql(gdb,ghost,guser,gpassword,gdatabase)
    for i in range(0,len(df_static_bond)):
    #for i in range(0,5000):
        for j in range(0,len(indic_list)):
            #str_sql='select AVG(indic_value)  from indic_value_new_2 where institution_id='+df_static_bond['institution_id'][i]+' and indic_v_year='+df_static_bond['report_year'][i]+' and indic_id='+"'"+indic_list[j]+"'"
            str_sql='select AVG(indic_value)  from indic_value_new_2 where institution_id='+df_static_bond['institution_id'][i]+' and indic_id='+"'"+indic_list[j]+"'"                
            temp=pd.read_sql(str_sql,conn)
            df_static_bond[indic_name[j]][i]= temp.iloc[0,0]
      
    conn.close()

    df_static_bond['cash_Current_Liabilities_ratio']=''
    df_static_bond['cash_Total_Liabilities_ratio']=''
    df_static_bond['EBITDA_interest_expense_ratio']=''
    #现金流动负债比
    try:
        df_static_bond['cash_Current_Liabilities_ratio']= df_static_bond['NCFO']/df_static_bond['Current_Liabilities']
    except:
        pass
    #现金债务总额比
    try:
        df_static_bond['cash_Total_Liabilities_ratio']= df_static_bond['NCFO']/df_static_bond['Liabilities']
    except:
        pass

    #EBITDA/利息支出 
    try:
        df_static_bond['EBITDA_interest_expense_ratio']= df_static_bond['EBITDA']/df_static_bond['interest_expense']
    except:
        pass
    
    return (df_static_bond)

def logistic_regression():
    pass
'''

    #df_bond_finance=finance_indic(df_static_bond)
    #按合约上市年份的报表平均值
    #df_bond_finance.to_excel('bond_finance_1.xlsx',index=False)
    #按合约所有年份的报表平均值
    #df_bond_finance.to_excel('bond_finance_2.xlsx',index=False)

