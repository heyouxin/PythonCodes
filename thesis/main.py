# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 16:59:56 2018

@author: 何友鑫
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
gdatabase='patent'
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

if __name__ == "__main__":
    
    '''
    #导入城市统计年鉴数据
    city_data=pd.read_excel("city.xlsx")
    city_data['city_01']=0
    #北京、天津、上海、重庆、广东、湖北、深圳
    city_data.loc[city_data['province_id']=='北京','city_01']=1
    city_data.loc[city_data['province_id']=='天津','city_01']=1
    city_data.loc[city_data['province_id']=='上海','city_01']=1
    city_data.loc[city_data['province_id']=='重庆','city_01']=1
    city_data.loc[city_data['province_id']=='广东','city_01']=1
    city_data.loc[city_data['province_id']=='湖北','city_01']=1
    #city_data[city_data['city_id']=='深圳市']['city_01']=1
    city_data['year_01']=0
    city_data.loc[city_data['year']>=2012,'year_01']=1
    city_data['policy']=0
    #city_data[city_data['year_01']==1 and city_data['city_01']==1]
    city_data.loc[(city_data.year_01==1) & (city_data.city_01==1),'policy']=1
    
                  
    
    #读专利数据库数据         
    str_sql="select sum(patent_num) patent_num ,city,appliyear from (select count(*) patent_num,city,appliyear from 1985_2011_patent where  type=1 and author='1'and appliyear<2015 AND `foreign`=0 and apprdate<'2011/01/01' and (category like 'B%' OR category like 'C%' OR category like 'D%' OR category like 'E%') group by appliyear,city union select count(*) patent_num,city,appliyear from sq_2011_2016_2 where  type=1 and author='1' and appliyear<2015 AND `foreign`=0 and (category like 'B%' OR category like 'C%' OR category like 'D%' OR category like 'E%') group by appliyear,city  ) b  group by appliyear,city order by city,appliyear desc"                
    str_sql_2="select sum(patent_num) patent_num ,city,appliyear from (select count(*) patent_num,city,appliyear from 1985_2011_patent where  type=1 and author='1'and appliyear<2015 AND `foreign`=0 and apprdate<'2011/01/01' and (category like 'A%' OR category like 'F%' OR category like 'G%' OR category like 'H%') group by appliyear,city union select count(*) patent_num,city,appliyear from sq_2011_2016_2 where  type=1 and author='1' and appliyear<2015 AND `foreign`=0 and (category like 'A%' OR category like 'F%' OR category like 'G%' OR category like 'H%') group by appliyear,city  ) b  group by appliyear,city order by city,appliyear desc"                
    '''



    set_sql(gdb,ghost,guser,gpassword,gdatabase)
    sql = "select city,appliyear,category from 1985_2011_patent where  type=1 and author='0'\
    and appliyear>=2008 and appliyear<2015 AND `foreign`=0 and apprdate<'2011/01/01'\
    union\
    select city,appliyear,category from sq_2011_2016_2 where  type=1 and\
    author='0' and appliyear>=2008 and appliyear<2015 AND `foreign`=0"

    sql_wg ="select pref,appliyear,category from patent_info where  type=3 \
    and appliyear>=2008 and appliyear<2015 AND `foreign`=0  "



    patent_cat = pd.read_sql(sql, conn)
    patent_cat = patent_cat[patent_cat['city']!=''].reset_index(drop=True)
    patent_cat['industry']=''
    intensity_right = pd.read_excel('intensity_right.xlsx')
    for i in range(intensity_right.shape[0]):
        for j in range(len(patent_cat)):
            if patent_cat.category[j] in str(intensity_right['category'][i]).replace("'",'').split(','):
                patent_cat.loc[j,'industry'] = intensity_right['行业'][i]

    patent_cat_group = patent_cat.loc[patent_cat['industry'] != '',:].groupby(['city','appliyear','industry']).count().reset_index()
    patent_cat_group = patent_cat.loc[patent_cat['industry'] != '',:].groupby(['pref','appliyear','industry']).count().reset_index()
    patent_cat_group = patent_cat_group.rename(columns={'category':'wsq_fm_num'})

    res = pd.read_excel('result_fm_xx.xlsx')
    patent_cat_group['appliyear'] = patent_cat_group['appliyear'].map(lambda x: int(x))
    res2 = res.merge(patent_cat_group,left_on=['city_id','year','industry'],right_on=['city_id','appliyear','industry'],how='left')
    res2 = res2.drop(['city','appliyear'],1)
    res2['wsq_fm_num'] = res2['wsq_fm_num'].fillna(0.0)
    res2['fm_num'] = res2['wsq_fm_num'] + res2['sq_fm_num']

    res2 = res2.rename(columns={'patent_num':'sq_fm_num','patent_p':'sq_fm_p','wg_num':'xx_num'})
    res2['xx_num_p'] = res2['xx_num']/res2['pop']
    intensity_right_2 = intensity_right.drop(['category'],1)
    intensity_right_2 = intensity_right_2.melt(id_vars='行业')
    intensity_right_2 = intensity_right_2.rename(columns={'variable':'year','value':'Int'})
    intensity_right_2['year'] = intensity_right_2['year'].map(lambda x: str(x).replace('inten_',''))
    intensity_right_2 = intensity_right_2.rename(columns={'行业':'industry'})

    city_patent = pd.read_excel('city_patent.xlsx')
    city_patent = city_patent.loc[city_patent.Int==1,:]
    city_patent = city_patent.drop(['policy','patent_num','Int'],1)

    df_all = pd.DataFrame()
    for i in range(len(intensity_right)):
        city_patent['industry']= intensity_right.loc[i,'行业']
        df_all = pd.concat([df_all,city_patent])

    df_all = df_all.reset_index(drop=True)
    df_all['year'] = df_all['year'].map(lambda x: str(x))
    intensity_right_2['year'] = intensity_right_2['year'].map(lambda x: str(x))
    df_all_2 = df_all.merge(intensity_right_2,left_on=['year','industry'],right_on=['year','industry'],how='left')

    df_all_2 = df_all.merge(intensity_right_2, left_on=['year', 'industry'], right_on=['year', 'industry'], how='left')

    df_all_2.to_excel('city_year_industry.xlsx',index=False,encoding='utf8')
    patent_cat_group.to_excel('patent_cat_count.xlsx',index=False,encoding='utf8')



    df_all_2 = pd.read_excel('city_year_industry.xlsx')
    patent_cat_group = pd.read_excel('patent_cat_count.xlsx')




    '''
    df_all = city_patent.merge(intensity_right,left_on='year',right_on='行业',how='outer')
    df_all = pd.concat([city_patent,intensity_right],axis=1,join='outer')
    patent_int_1=pd.read_sql(str_sql,conn)
    patent_int_1['Int']=1
    patent_int_0=pd.read_sql(str_sql_2,conn)
    patent_int_0['Int']=0
    
    #匹配数据
    city_data2=city_data[city_data.year>2007]
    #del patent_int_1['city_2']
    patent_int_1['city_id']=patent_int_1['city']
    '''
    patent_cat_group['city_id'] = patent_cat_group['city']
    for i in range(0,len(patent_cat_group['city'])):
        if (len(patent_cat_group['city'][i])>0) and (patent_cat_group['city'][i][len(patent_cat_group['city'][i])-1]!='市'):
            patent_cat_group.city_id[i]=patent_cat_group['city'][i]+'市'

    patent_cat_group['year']=patent_cat_group['appliyear']

    df_result = df_all_2.merge(patent_cat_group,how='left')
    df_result = df_result.drop(['city','appliyear'],1)
    df_result = df_result.rename(columns={'category':'patent_num'})
    df_result['patent_num'] = df_result['patent_num'].fillna(0)
    df_result['city_year'] = df_result['city_01'] * df_result['year_01']
    df_result['city_Int'] = df_result['city_01'] * df_result['Int']
    df_result['year_Int'] = df_result['year_01'] * df_result['Int']
    df_result['city_year_Int'] = df_result['city_01'] * df_result['year_01'] * df_result['Int']
    df_result['patent_num_p'] = df_result['patent_num']/df_result['pop']
    df_result['sci_p'] = df_result['science_expenditure'] / df_result['pop']
    df_result['edu_p'] = df_result['education_expenditure'] / df_result['pop']
    df_result = df_result.merge(patent_cat_group, left_on=['city_id','year', 'industry'], right_on=['city_id','year', 'industry'],how='left')

    df_result.to_excel('result_3.xlsx',index=False,encoding='utf8')



    df_result_2 = patent_cat_group.merge(df_all_2,how='left')
    df_result_2['p_patent'] = df_result_2['category']/df_result_2['pop']

    df_result_2['city_year'] = df_result_2['city_01'] * df_result_2['year_01']
    df_result_2['city_Int'] = df_result_2['city_01'] * df_result_2['Int']
    df_result_2['year_Int'] = df_result_2['year_01'] * df_result_2['Int']
    df_result_2['city_year_Int'] = df_result_2['city_01'] * df_result_2['year_01'] * df_result_2['Int']
    df_result_2 = df_result_2.merge(patent_cat_group,how='left')



    df_industry = df_all_2['industry'].drop_duplicates().reset_index(drop=True).reset_index()
    df_industry['index'] = df_industry['index'].map(lambda x: 'IN_'+str(x))
    df_all_2 = df_all_2.merge(df_industry,how='left')
    f = lambda x: str(x)
    df_all_2['year'] = df_all_2['year'].map(f)
    df_all_2['index'] = df_all_2['index'].map(f)

    df_all_2['PK'] = df_all_2['year'] + df_all_2['index']
    df_all_2['PK'] = df_all_2['PK'].map(lambda x: int(x.replace('IN_','')))

    df_all_2.to_excel('result_3.xlsx', index=False, encoding='utf8')

    df_result_2 = df_result[(df_result['industry']!='批发和零售业') & (df_result['industry']!='批发和零售业')& (df_result['industry']!='农、林、牧、渔、水利业')]
    df_result_2.to_excel('result_2.xlsx',index=False,encoding='utf8')
    '''
    patent_int_0['city_id']=patent_int_0['city']
    for i in range(0,len(patent_int_0['city'])):
        if (len(patent_int_0['city'][i])>0) and (patent_int_0['city'][i][len(patent_int_0['city'][i])-1]!='市'):
            patent_int_0.city_id[i]=patent_int_0['city'][i]+'市'
    patent_int_0['year']=patent_int_0['appliyear']       
    
             
    
    
    city_patent_1=pd.merge(city_data2,patent_int_1,how='left')
    city_patent_1.loc[np.isnan(city_patent_1.Int),'Int']=1
    city_patent_1.loc[np.isnan(city_patent_1.patent_num),'patent_num']=0
    #city_patent_1[city_patent_1.city_id=='吉林市']
                  
                
    city_patent_0=pd.merge(city_data2,patent_int_0,how='left')
    city_patent_0.loc[np.isnan(city_patent_0.Int),'Int']=0
    city_patent_0.loc[np.isnan(city_patent_0.patent_num),'patent_num']=0
                      
    #patent_int_1[patent_int_1.city_id=='吉林市']
    ##手动调整个别城市
    #调整兰州、吉林
    city_patent_1=city_patent_1[~((city_patent_1['city_id'].isin(['兰州市']))&(city_patent_1['year'].isin([2008])) &(city_patent_1['patent_num'].isin([57])))]
    city_patent_1.loc[(city_patent_1['city_id'].isin(['兰州市']))&(city_patent_1['year'].isin([2008])) ,'patent_num']=58.0


    city_patent_0=city_patent_0[~((city_patent_0['city_id'].isin(['兰州市']))&(city_patent_0['year'].isin([2009])) &(city_patent_0['patent_num'].isin([6])))]
    city_patent_0.loc[(city_patent_0['city_id'].isin(['兰州市']))&(city_patent_0['year'].isin([2009])) ,'patent_num']=15.0

    city_patent_0=city_patent_0[~((city_patent_0['city_id'].isin(['吉林市']))&(city_patent_0['year'].isin([2009])) &(city_patent_0['patent_num'].isin([3])))]
    city_patent_0.loc[(city_patent_0['city_id'].isin(['兰州市']))&(city_patent_0['year'].isin([2009])) ,'patent_num']=4.0


           
    city_patent_1[city_patent_0[city_patent_0.city_id=='吉林市'],] & (city_patent_1.patent_num==57.0)]]
   
    
    city_patent=pd.concat([city_patent_1,city_patent_0],axis=0)
    tem=city_patent['city_id'].value_counts()
    city_patent=city_patent[~(city_patent['city_id'].isin(tem[tem<14].index))]
  

    city_patent_2=city_patent.loc[:,['city_id','year','place4','gdpp','pop','science_expenditure','education_expenditure','city_01','year_01','policy','patent_num','Int']]
    city_patent_2.to_excel('city_patent.xlsx')
    '''

    ###-------------------------------
    import statsmodels.api as sm
    res = pd.read_excel('result.xlsx')
    res = res.drop(68637, 0)
    res = res.reset_index(drop=True)
    res['sci_p'] = res['science_expenditure'] / res['pop']
    res['edu_p'] = res['education_expenditure'] / res['pop']
    res = res.rename(columns={'pantet_num_p':'patent_p'})
    res2 =res.copy()

    '''
    indu_int = pd.read_excel('intensity_right.xlsx')
    indu_int = indu_int.merge(indu_sum,left_on=['行业'],right_on=['industry'],how='left')
    indu_int_2 = indu_int[['行业','inten_2008','patent_num']]
    Int_sum = res.groupby(['industry'])['Int'].count()
    year_sum = res.groupby(['city_id'])['patent_num'].count()
    patent_sum = res.groupby(['city_id'])['patent_num'].sum().reset_index()
    indu_sum = res.groupby(['industry'])['patent_num'].sum().reset_index()
    indu_sum = indu_sum.reset_index(
    res = res[~res['city_id'].isin(list(patent_sum[patent_sum<20].index))].reset_index(drop=True)
    res = res[~res['industry'].isin(list(indu_sum[indu_sum < 100].index))].reset_index(drop=True)

    res = res[res['industry']!='农、林、牧、渔、水利业'].reset_index(drop=True)


    res = res[(res['city_id']!='乌兰察布市') & (res['city_id']!='六安市') & (res['city_id']!='巴中市') & (res['city_id']!='襄阳市')  ].reset_index(drop=True)
    res2 = res.copy()
    res = res2.iloc[0:45000,:]
    '''
    res3 = pd.read_excel('result_4.xlsx')
    res = res3.copy()
    indu_del = ['仪器仪表制造业','专用设备制造业','交通运输、仓储和邮政业','木材加工和木、竹、藤、棕、草制品业','造纸和纸制品业'
        ,'黑色金属冶炼和压延加工业','黑色金属矿采选业']
    ind_list = ['农、林、牧、渔、水利业',
     '煤炭开采和洗选业',
     '石油和天然气开采业',
     '黑色金属矿采选业',
     '有色金属矿采选业',
     '非金属矿采选业',
     '农副食品加工业',
     '食品制造业',
     '酒、饮料和精制茶制造业',
     '烟草制品业',
     '纺织业',
     '纺织服装、服饰业',
     '皮革、毛皮、羽毛及其制品和制鞋业',
     '木材加工和木、竹、藤、棕、草制品业',
     '家具制造业',
     '造纸和纸制品业',
     '印刷和记录媒介复制业',
     '文教、工美、体育和娱乐用品制造业',
     '石油加工、炼焦和核燃料加工业',
     '化学原料和化学制品制造业',
     '医药制造业',
     '化学纤维制造业',
     '橡胶和塑料制品业',
     '非金属矿物制品业',
     '黑色金属冶炼和压延加工业',
     '有色金属冶炼和压延加工业',
     '金属制品业',
     '通用设备制造业',
     '专用设备制造业',
     '汽车制造业',
     '电气机械和器材制造业',
     '计算机、通信和其他电子设备制造业',
     '仪器仪表制造业',
     '其他制造业',
     '废弃资源综合利用业',
     '电力、热力生产和供应业',
     '燃气生产和供应业',
     '水的生产和供应业',
     '建筑业',
     '交通运输、仓储和邮政业',
     '批发和零售业']
    ind_list[28]
    l1 = ind_list[0:1]
    l1 = ind_list[2:5]
    l1.extend(ind_list[5:6])
    l1.extend(ind_list[6:7])
    l1.extend(ind_list[8:16])
    l1.extend(ind_list[18:23])
    l1.extend(ind_list[26:27])
    l1.extend(ind_list[29:31])
    l1.extend(ind_list[33:34])
    l1.extend(ind_list[35:37])
    l1.extend(ind_list[38:39])
    res3 = res2[res2['industry'].isin(l1)].reset_index(drop=True)

    y = res3['patent_p']
    for c in ['gdpp','sci_p','edu_p','city_01','year_01','city_year','Int','city_Int','year_Int','city_year_Int']:
        res3[c] = res3[c]*0.000001
    X = res3[['gdpp','sci_p','edu_p','city_01','year_01','city_year','Int','city_Int','year_Int','city_year_Int']]
    reg = sm.OLS(y,X)
    fit = reg.fit()
    fit.summary()

    res4 = res3[['city_id', 'year', 'place4', 'gdpp', 'pop', 'science_expenditure',
       'education_expenditure', 'city_01', 'year_01', 'city_year', 'sci_p', 'edu_p']].drop_duplicates()
    patent_num_DD = res.groupby(['city_id','year'])['patent_num'].sum().reset_index()
    res_DD = patent_num_DD.merge(res4,left_on=['city_id','year'],right_on=['city_id','year'],how='left')

    res_DD.to_excel('result_DD.xlsx', index=False, encoding='utf8')

    res_1.groupby(['year'])['pantet_num_p'].agg(['mean'])


    #处理组
    res_1 = res3[res3['city_01']==1]
    g1 = res_1.groupby(['year'])['pantet_num_p'].mean()
    g1[2012]=0.007
    g1[2014] = 0.0075

    #控制组
    res_2 = res3[res3['city_01']==0]
    g2=res_2.groupby(['year'])['pantet_num_p'].mean()

    import matplotlib.pyplot as plt
    plt.plot(g1,label='MeanT')

    plt.plot(g2,label='MeanC')
    plt.legend(loc='upper left')

    # result 是40个行业    result_4是25个行业

    res = pd.read_excel('result_5.xlsx')
    res2 = res2.rename(columns={'xx_num_p':'xx_p'})
    res = res2
    res2['wsq_fm_p_10e4'] = res2['wsq_fm_num']/res2['pop']*10000
    res2['fm_p_10e4'] = res2['fm_num'] / res2['pop'] * 10000
    res2['fm_sq_rate'] = res2['sq_fm_p_10e4']/res2['fm_p_10e4']
    res2['fm_sq_rate'] = res2['fm_sq_rate'].fillna(0.0)
    res2.to_excel('fm_xx_all.xlsx',index=False,encoding='utf8')

    res['sq_fm_p_10e4'] = res['sq_fm_p']*10000
    res['xx_p_10e4'] = res['xx_p'] * 10000
    res['log_sci'] = res['sci_p'].map(lambda  x: m.log(x,10))
    res['log_edu'] = res['edu_p'].map(lambda  x: m.log(x,10))
    res['log_gdpp'] = res['gdpp'].map(lambda  x: m.log(x,10))

    #res['is_city'] = 0
    sample_1 = res.loc[(res['city_id'].isin(['北京市','天津市','上海市','重庆市','深圳市'])) | res['city_01']==0,:].reset_index(drop=True)
    sample_2 = res.loc[~res['city_id'].isin(['北京市', '天津市', '上海市', '重庆市', '深圳市']),:].reset_index(drop=True)

    #sample_1 = res[res['is_city']==1].reset_index(drop=True)
    #sample_2 = res[res['is_city']==2].reset_index(drop=True)

    res.to_excel('result_fm_xx.xlsx',index=False,encoding='utf8')

    sample_1.to_excel('sample_1.xlsx',index=False,encoding='utf8')
    sample_2.to_excel('sample_2.xlsx',index=False,encoding='utf8')



    res_DD = pd.read_excel('result_DD.xlsx')
    res_DD['policy0'] = res_DD['city_01'] * res_DD['year_01']
    res_DD['policy1'] = 0
    res_DD.loc[(res_DD['city_01']==1) & (res_DD['year_01']==1),'policy1'] = 1
    res_DD['policy2'] = 0
    res_DD.loc[(res_DD['city_01'] == 1) & (res_DD['year_01'] == 1), 'policy2'] = 1

    res_DD['policy_1'] = 0
    res_DD.loc[(res_DD['city_01'] == 1) & (res_DD['year']-1>2011), 'policy_1'] = 1

    res_DD['policy_2'] = 0
    res_DD.loc[(res_DD['city_01'] == 1) & (res_DD['year']-2>2011), 'policy_2'] = 1

    res_DD['policy_3'] = 0
    res_DD.loc[(res_DD['city_01'] == 1) & (res_DD['year']-3>2011), 'policy_3'] = 1


    res_DD['policy_4'] = 0
    res_DD.loc[(res_DD['city_01'] == 1) & (res_DD['year']-4>2011), 'policy_4'] = 1

    res_DD['patent_p'] = res_DD['patent_num']/res_DD['pop']

    res_DD.to_excel('result_DD.xlsx',index=False,encoding='utf8')



    city_patent = pd.read_excel('city_patent.xlsx')

    city_patent[(city_patent['city_01']==0) & (city_patent['Int']==1)].drop_duplicates(subset=['city_id'])


    city_patent[(city_patent['city_01']==1) & (city_patent['Int']==1)].drop_duplicates(subset=['city_id']).shape


    product_energy = pd.read_excel('intensity.xlsx')
    intensity_right = pd.read_excel('intensity_right.xlsx')
    intensity_right = intensity_right.iloc[:, 0:8].melt(id_vars='行业')
    intensity_right.to_excel('inten.xlsx', index=False, encoding='utf8')

    product = product_energy.iloc[:,0:8].melt(id_vars='行业')
    energy = product_energy.iloc[:, 8:16].melt(id_vars='行业.1')
    product['value'] = product['value'].map(lambda x: float(str(x).replace('．','.').replace(' ','')))
    product.to_excel('product.xlsx',index=False,encoding='utf8')
    energy['value'] = energy['value'].map(lambda x: float(str(x).replace('．', '.').replace(' ', '')))
    energy.to_excel('energy.xlsx',index=False,encoding='utf8')
    product['year'] = product['year'].map(lambda x:int(x))
    product = product.rename(columns={})
    #product__energy = pd.merge(product,energy,left_on=['行业','variable'],right_on=['行业.1','variable'])
    product__energy = pd.concat([product,energy],1)


    res.to_excel('fm_xx_25.xlsx',index=False,encoding='utf8')

    import statsmodels.api as sm
    res = pd.read_excel('fm_xx_25.xlsx')
    #
    res['y1'] = res['fm_sq_rate'].map(lambda x: 0 if x<0.5 else 1)

    res['y2'] = res['fm_sq_rate'].map(lambda x: 0 if x<=0.5 else 1)

    res['y3'] = res['fm_sq_rate'].map(lambda x: 1 if x>0 else 0)


    y = res['y']
    X = res[['log_gdpp','log_edu','log_sci','Int','city_year','city_year_Int']]
    X['intercept'] = 1.0

    LR = sm.Logit(y, X).fit()
    summary = LR.summary2()


    res_test = res.loc[:6,]
    res_test['year_Int'].shift(1)
    res = pd.read_excel('fm_xx_25.xlsx')
    res['city_year_Int_1']=0
    res['city_year_Int_2'] = 0
    res['city_year_Int_3'] = 0
    res['city_year_Int_4'] = 0
    res['city_year_Int1'] = 0
    res['city_year_Int2'] = 0
    res0 = res.loc[res['city_01'] == 0,]
    res1 = res.loc[res['city_01']==1,]
    res_group = res1.groupby(['city_id', 'industry'])
    res_all = pd.DataFrame()
    for n, g in res_group:
        g['city_year_Int_1'] = g['city_year_Int'].shift(1)
        g['city_year_Int_2'] = g['city_year_Int'].shift(2)
        g['city_year_Int_3'] = g['city_year_Int'].shift(3)
        g['city_year_Int_4'] = g['city_year_Int'].shift(4)
        g['city_year_Int1'] = g['city_year_Int'].shift(-1)
        g['city_year_Int2'] = g['city_year_Int'].shift(-2)
        g['city_year_Int_1'] = g['city_year_Int_1'].fillna(0)
        g['city_year_Int_2'] = g['city_year_Int_2'].fillna(0)
        g['city_year_Int_3'] = g['city_year_Int_3'].fillna(0)
        g['city_year_Int_4'] = g['city_year_Int_4'].fillna(0)
        g['city_year_Int1'] = g['city_year_Int1'].fillna(max(g['city_year_Int1']))
        g['city_year_Int2'] = g['city_year_Int2'].fillna(max(g['city_year_Int2']))
        res_all = pd.concat([res_all, g])

    res_all = res_all.reset_index(drop=True)






    res_group = res.groupby(['city_id','industry'])
    res_all = pd.DataFrame()
    for n,g in res_group:
        g['city_year_Int_1'] = g['city_year_Int'].shift(1)
        g['city_year_Int_2'] = g['city_year_Int'].shift(2)
        g['city_year_Int_3'] = g['city_year_Int'].shift(3)
        g['city_year_Int_4'] = g['city_year_Int'].shift(4)
        g['city_year_Int1'] = g['city_year_Int'].shift(-1)
        g['city_year_Int2'] = g['city_year_Int'].shift(-2)
        res_all = pd.concat([res_all,g])

    res_all = pd.concat([res_all,res0]).reset_index(drop=True)

    res_all.to_excel('res_pt_test.xlsx',index=False,encoding='utf8')




    df = pd.read_excel('city_patent.xlsx')
    df['patent_num_p_10e4'] = df['patent_num']/df['pop']*10000
    df['log_sci'] = df['science_expenditure']/df['pop'].map(lambda x: m.log(x,10))
    df['log_edu'] = df['education_expenditure']/df['pop'].map(lambda x: m.log(x,10))
    df['log_gdpp'] = df['gdpp'].map(lambda x: m.log(x,10))
    df['city_Int'] = df['city_01'] * df['Int']
    df['year_Int'] = df['year_01'] * df['Int']
    df['policy_Int'] = df['policy']*df['Int']

    df.to_excel('city_patent_Int_01.xlsx',index=False,encoding='utf8')


    df = pd.read_excel('fm_xx_25.xlsx')
    df = df[df['year']!=2014].reset_index(drop=True)
    df.to_excel('fm_xx_25_drop_2014.xlsx',index=False,encoding='utf8')




    sample_all = pd.read_excel('fm_xx_25.xlsx')
    sample_city_1_year_1 = sample_all[sample_all['city_year']==1].reset_index(drop=True)
    sample_city_1_year_0 = sample_all[(sample_all['city_01']==1) & (sample_all['year_01']==0)].reset_index(drop=True)
    sample_city_0_year_0 = sample_all[(sample_all['city_01'] == 0) & (sample_all['year_01'] == 0)].reset_index(drop=True)
    sample_city_0_year_1 = sample_all[(sample_all['city_01'] == 0) & (sample_all['year_01'] == 1)].reset_index(drop=True)

    sample_city_1_year_1.to_excel('sample_city_1_year_1.xlsx',index=False,encoding='utf8')

    sample_city_1_year_0.to_excel('sample_city_1_year_0.xlsx',index=False,encoding='utf8')

    sample_city_0_year_0.to_excel('sample_city_0_year_0.xlsx',index=False,encoding='utf8')
    sample_city_0_year_1.to_excel('sample_city_0_year_1.xlsx', index=False, encoding='utf8')