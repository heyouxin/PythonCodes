# -*- coding: utf-8 -*-
"""
Created on Sat Oct 28 18:29:46 2017

@author: 何友鑫
"""


import pandas as pd 
from pandas import DataFrame
import math as m
import numpy as np
import statsmodels.api as sm




##取2005-2016年HS300股票数据 每年6月末进行 调整
##取hs300成分股及权重数据，取股票月度数据。接出hs300中的股票，并按市值、账面市值比分组
##2016年6月30日指数权重数据没有，暂用2017年6月30日的数据代替
def size_bm_group(breakyear):

    global hs300s_stock_m,hs300s_stock_breakpoint,stock_SH,stock_SM,stock_SL,stock_BH,stock_BM,stock_BL
    string1='./HS300数据/hs300_weights_'
    string2='.xls'
    hs_file="%s%s%s"%(string1,breakyear,string2)
    #hs_file='C:/Users/heyouxin/Desktop/HS300数据/hs300_weights_'+breakyear+'.xls'
    hs300s=pd.read_excel(hs_file)
    stock_file="%s%s%s"%('./HS300数据/stock_',breakyear,'.xls')
    #stock_file='C:/Users/heyouxin/Desktop/HS300数据/stock_'+breakyear+'.xls'
    stock_month=pd.read_excel(stock_file)
    hs300s_stock_m=pd.merge(stock_month,hs300s,how='left',left_on='股票代码_Stkcd',right_on='成分股代码_CompoStkCd')
    ##保留hs300的股票月度数据
    hs300s_stock_m=hs300s_stock_m.dropna()
    ##保留市净率大于0
    hs300s_stock_m=hs300s_stock_m[hs300s_stock_m.市净率_PB>0]
    ##计算市值
    hs300s_stock_m['流通市值']=hs300s_stock_m['已上市流通股_Lsttrdshr']*hs300s_stock_m['收盘价_ClPr']
    ##计算账面市值比 即1/PB
    hs300s_stock_m['账面市值比']=1/hs300s_stock_m['市净率_PB']
    ##计算超额收益率 即 R-Rf
    hs300s_stock_m['超额收益率']=hs300s_stock_m['月收益率_Monret']-hs300s_stock_m['月无风险收益率_Monrfret']
  
    ##取出调整日当天的hs300数据
    date1=breakyear+'-06-28  00:00:00'
    date2=breakyear+'-06-30  00:00:00'
    hs300s_stock_breakpoint=hs300s_stock_m[(hs300s_stock_m.日期_Date>=date1)&(hs300s_stock_m.日期_Date<=date2)].dropna()
  
    
    ##按市值分组 small big 
    size_50=np.percentile(hs300s_stock_breakpoint['流通市值'],50)
    hs300s_stock_size_small=hs300s_stock_breakpoint[hs300s_stock_breakpoint.流通市值<=size_50]['股票代码_Stkcd']
    hs300s_stock_size_big=hs300s_stock_breakpoint[hs300s_stock_breakpoint.流通市值>size_50]['股票代码_Stkcd']
    ##按账面市值比分组 L  M   H
    bm_33=np.percentile(hs300s_stock_breakpoint['账面市值比'],100/3)
    bm_66=np.percentile(hs300s_stock_breakpoint['账面市值比'],200/3)
    hs300s_stock_bm_low=hs300s_stock_breakpoint[hs300s_stock_breakpoint.账面市值比<=bm_33]['股票代码_Stkcd']  
    hs300s_stock_bm_middle=hs300s_stock_breakpoint[(hs300s_stock_breakpoint.账面市值比>bm_33)&((hs300s_stock_breakpoint.账面市值比<=bm_66))]['股票代码_Stkcd']      
    hs300s_stock_bm_high=hs300s_stock_breakpoint[(hs300s_stock_breakpoint.账面市值比>bm_66)]['股票代码_Stkcd']    
   
    ##SMB = 1/3(SL+SM+SH)-1/3(BL+BM+BH)
    ##HML = (SH+BH)/2-(SL+BL)/2
    ##获得分组股票代码
    stock_SH=set(hs300s_stock_size_small).intersection(set(hs300s_stock_bm_high))
    stock_SM=set(hs300s_stock_size_small).intersection(set(hs300s_stock_bm_middle))
    stock_SL=set(hs300s_stock_size_small).intersection(set(hs300s_stock_bm_low))
    
    stock_BH=set(hs300s_stock_size_big).intersection(set(hs300s_stock_bm_high))
    stock_BM=set(hs300s_stock_size_big).intersection(set(hs300s_stock_bm_middle))
    stock_BL=set(hs300s_stock_size_big).intersection(set(hs300s_stock_bm_low))
   
    
    stock_SH=list(stock_SH)
    stock_SH=DataFrame(stock_SH)
    stock_SH.columns=['股票代码_Stkcd']
    stock_SH=pd.merge(stock_SH,hs300s_stock_m)
    stock_SH['加权收益率_Weiretun']=(stock_SH['流通市值']/stock_SH['流通市值'].sum())*stock_SH['月收益率_Monret']
  

    stock_SM=list(stock_SM)
    stock_SM=DataFrame(stock_SM)
    stock_SM.columns=['股票代码_Stkcd']
    stock_SM=pd.merge(stock_SM,hs300s_stock_m)
    stock_SM['加权收益率_Weiretun']=(stock_SM['流通市值']/stock_SM['流通市值'].sum())*stock_SM['月收益率_Monret']

    
    stock_SL=list(stock_SL)
    stock_SL=DataFrame(stock_SL)
    stock_SL.columns=['股票代码_Stkcd']
    stock_SL=pd.merge(stock_SL,hs300s_stock_m)
    stock_SL['加权收益率_Weiretun']=(stock_SL['流通市值']/stock_SL['流通市值'].sum())*stock_SL['月收益率_Monret']

    stock_BH=list(stock_BH)
    stock_BH=DataFrame(stock_BH)
    stock_BH.columns=['股票代码_Stkcd']
    stock_BH=pd.merge(stock_BH,hs300s_stock_m)
    stock_BH['加权收益率_Weiretun']=(stock_BH['流通市值']/stock_BH['流通市值'].sum())*stock_BH['月收益率_Monret']

    stock_BM=list(stock_BM)
    stock_BM=DataFrame(stock_BM)
    stock_BM.columns=['股票代码_Stkcd']
    stock_BM=pd.merge(stock_BM,hs300s_stock_m)
    stock_BM['加权收益率_Weiretun']=(stock_BM['流通市值']/stock_BM['流通市值'].sum())*stock_BM['月收益率_Monret']

    stock_BL=list(stock_BL)
    stock_BL=DataFrame(stock_BL)
    stock_BL.columns=['股票代码_Stkcd']
    stock_BL=pd.merge(stock_BL,hs300s_stock_m)
    stock_BL['加权收益率_Weiretun']=(stock_BL['流通市值']/stock_BL['流通市值'].sum())*stock_BL['月收益率_Monret']
    

    

##计算因子    
def calc_factors():
    breakpoint=['2005','2006','2007','2008','2009','2010','2011','2012' \
            ,'2013','2014','2015','2016','2017']
    SMB=[]
    HML=[]
    R_Rf=[]
    Rm_Rf=[]
    UMD=pd.Series()
    R_25_group=DataFrame()
    for i in range(0,12):
        #hs300s_stock_m,stock_SH,stock_SM,stock_SL,stock_BH,stock_BM,stock_BL=size_bm_group(breakpoint[i])
        size_bm_group(breakpoint[i])
        SMB_temp=calc_SMB(breakpoint[i],breakpoint[i+1])
        SMB=SMB+SMB_temp
        HML_temp=calc_HML(breakpoint[i],breakpoint[i+1])
        HML=HML+HML_temp
        R_25_group_temp=calc_R_Rf(breakpoint[i],breakpoint[i+1])
        R_25_group=R_25_group.append(R_25_group_temp)
        UMD_temp=calc_UMD(breakpoint[i],breakpoint[i+1])
        UMD=UMD.append(UMD_temp)
    SMB=np.array(SMB)
    HML=np.array(HML)
    Rm_Rf=np.array(calc_RM_Rf())
    UMD=np.array(UMD)
    return (R_25_group,SMB,HML,Rm_Rf,UMD)
        
    
##计算SMB因子
def calc_SMB(breakyear,breakyear1):

 
    group=(stock_SH,stock_SM,stock_SL,stock_BH,stock_BM,stock_BL)
    Weireturn_SH=[]
    Weireturn_SM=[]
    Weireturn_SL=[]
    Weireturn_BH=[]
    Weireturn_BM=[]
    Weireturn_BL=[]
    Weireturn=(Weireturn_SH,Weireturn_SM,Weireturn_SL,Weireturn_BH,Weireturn_BM,Weireturn_BL)
    for g in range(0,6):
                
        Weireturn[g].append(group[g][(group[g].日期_Date>=breakyear+'-06-1  00:00:00')&(group[g].日期_Date<=breakyear+'-06-30  00:00:00')]['加权收益率_Weiretun'].sum())
        Weireturn[g].append(group[g][(group[g].日期_Date>=breakyear+'-07-1  00:00:00')&(group[g].日期_Date<=breakyear+'-07-31  00:00:00')]['加权收益率_Weiretun'].sum())
        Weireturn[g].append(group[g][(group[g].日期_Date>=breakyear+'-08-1  00:00:00')&(group[g].日期_Date<=breakyear+'-08-31  00:00:00')]['加权收益率_Weiretun'].sum())
        Weireturn[g].append(group[g][(group[g].日期_Date>=breakyear+'-09-1  00:00:00')&(group[g].日期_Date<=breakyear+'-09-30  00:00:00')]['加权收益率_Weiretun'].sum())
        Weireturn[g].append(group[g][(group[g].日期_Date>=breakyear+'-10-1  00:00:00')&(group[g].日期_Date<=breakyear+'-10-31  00:00:00')]['加权收益率_Weiretun'].sum())
        Weireturn[g].append(group[g][(group[g].日期_Date>=breakyear+'-11-1  00:00:00')&(group[g].日期_Date<=breakyear+'-11-30  00:00:00')]['加权收益率_Weiretun'].sum())
        Weireturn[g].append(group[g][(group[g].日期_Date>=breakyear+'-12-1  00:00:00')&(group[g].日期_Date<=breakyear+'-12-31  00:00:00')]['加权收益率_Weiretun'].sum())
        Weireturn[g].append(group[g][(group[g].日期_Date>=breakyear1+'-1-1  00:00:00')&(group[g].日期_Date<=breakyear1+'-1-31  00:00:00')]['加权收益率_Weiretun'].sum())
        Weireturn[g].append(group[g][(group[g].日期_Date>=breakyear1+'-2-1  00:00:00')&(group[g].日期_Date<=breakyear1+'-2-28  00:00:00')]['加权收益率_Weiretun'].sum())
        Weireturn[g].append(group[g][(group[g].日期_Date>=breakyear1+'-3-1  00:00:00')&(group[g].日期_Date<=breakyear1+'-3-31  00:00:00')]['加权收益率_Weiretun'].sum())
        Weireturn[g].append(group[g][(group[g].日期_Date>=breakyear1+'-4-1  00:00:00')&(group[g].日期_Date<=breakyear1+'-4-30  00:00:00')]['加权收益率_Weiretun'].sum())
        Weireturn[g].append(group[g][(group[g].日期_Date>=breakyear1+'-5-1  00:00:00')&(group[g].日期_Date<=breakyear1+'-5-31  00:00:00')]['加权收益率_Weiretun'].sum())

    SMB_temp=[]
    for m in range(0,12):              
        SMB_temp.append((Weireturn_SH[m]+Weireturn_SM[m]+Weireturn_SL[m])/3+(Weireturn_BH[m]+Weireturn_BM[m]+Weireturn_BL[m])/3)
    return (SMB_temp)
              
 
           
##计算HML因子  
def calc_HML(breakyear,breakyear1):
    group=(stock_SH,stock_BH,stock_SL,stock_BL)
    Weireturn_SH=[]
    Weireturn_BH=[]
    Weireturn_SL=[]
    Weireturn_BL=[]
    Weireturn=(Weireturn_SH,Weireturn_BH,Weireturn_SL,Weireturn_BL)
    for g in range(0,4):          
        Weireturn[g].append(group[g][(group[g].日期_Date>=breakyear+'-06-1  00:00:00')&(group[g].日期_Date<=breakyear+'-06-30  00:00:00')]['加权收益率_Weiretun'].sum())
        Weireturn[g].append(group[g][(group[g].日期_Date>=breakyear+'-07-1  00:00:00')&(group[g].日期_Date<=breakyear+'-07-31  00:00:00')]['加权收益率_Weiretun'].sum())
        Weireturn[g].append(group[g][(group[g].日期_Date>=breakyear+'-08-1  00:00:00')&(group[g].日期_Date<=breakyear+'-08-31  00:00:00')]['加权收益率_Weiretun'].sum())
        Weireturn[g].append(group[g][(group[g].日期_Date>=breakyear+'-09-1  00:00:00')&(group[g].日期_Date<=breakyear+'-09-30  00:00:00')]['加权收益率_Weiretun'].sum())
        Weireturn[g].append(group[g][(group[g].日期_Date>=breakyear+'-10-1  00:00:00')&(group[g].日期_Date<=breakyear+'-10-31  00:00:00')]['加权收益率_Weiretun'].sum())
        Weireturn[g].append(group[g][(group[g].日期_Date>=breakyear+'-11-1  00:00:00')&(group[g].日期_Date<=breakyear+'-11-30  00:00:00')]['加权收益率_Weiretun'].sum())
        Weireturn[g].append(group[g][(group[g].日期_Date>=breakyear+'-12-1  00:00:00')&(group[g].日期_Date<=breakyear+'-12-31  00:00:00')]['加权收益率_Weiretun'].sum())
        Weireturn[g].append(group[g][(group[g].日期_Date>=breakyear1+'-1-1  00:00:00')&(group[g].日期_Date<=breakyear1+'-1-31  00:00:00')]['加权收益率_Weiretun'].sum())
        if (breakyear1=='2008')|(breakyear1=='2012')|(breakyear1=='2016'):
            Weireturn[g].append(group[g][(group[g].日期_Date>=breakyear1+'-2-1  00:00:00')&(group[g].日期_Date<=breakyear1+'-2-29  00:00:00')]['加权收益率_Weiretun'].sum())
        else:
            Weireturn[g].append(group[g][(group[g].日期_Date>=breakyear1+'-2-1  00:00:00')&(group[g].日期_Date<=breakyear1+'-2-28  00:00:00')]['加权收益率_Weiretun'].sum())
   
        Weireturn[g].append(group[g][(group[g].日期_Date>=breakyear1+'-3-1  00:00:00')&(group[g].日期_Date<=breakyear1+'-3-31  00:00:00')]['加权收益率_Weiretun'].sum())
        Weireturn[g].append(group[g][(group[g].日期_Date>=breakyear1+'-4-1  00:00:00')&(group[g].日期_Date<=breakyear1+'-4-30  00:00:00')]['加权收益率_Weiretun'].sum())
        Weireturn[g].append(group[g][(group[g].日期_Date>=breakyear1+'-5-1  00:00:00')&(group[g].日期_Date<=breakyear1+'-5-31  00:00:00')]['加权收益率_Weiretun'].sum())

    HML_temp=[]
    for m in range(0,12):              
        HML_temp.append((Weireturn_SH[m]+Weireturn_BH[m])/2+(Weireturn_SL[m]+Weireturn_BL[m])/2)

    return (HML_temp)

  

##计算因变量
##每期将股票按市值、账面市值比分为25个组合，将超额收益率按市值加权合成exReturn序列
def calc_R_Rf(breakyear,breakyear1):
        
    ##按市值分组 
    size_20=np.percentile(hs300s_stock_breakpoint['流通市值'],20) 
    size_40=np.percentile(hs300s_stock_breakpoint['流通市值'],40)
    size_60=np.percentile(hs300s_stock_breakpoint['流通市值'],60) 
    size_80=np.percentile(hs300s_stock_breakpoint['流通市值'],80)

    hs300s_stock_size_1=hs300s_stock_breakpoint[hs300s_stock_breakpoint.流通市值<=size_20]['股票代码_Stkcd']
    hs300s_stock_size_2=hs300s_stock_breakpoint[(hs300s_stock_breakpoint.流通市值>size_20)&(hs300s_stock_breakpoint.流通市值<=size_40)]['股票代码_Stkcd']
    hs300s_stock_size_3=hs300s_stock_breakpoint[(hs300s_stock_breakpoint.流通市值>size_40)&(hs300s_stock_breakpoint.流通市值<=size_60)]['股票代码_Stkcd']
    hs300s_stock_size_4=hs300s_stock_breakpoint[(hs300s_stock_breakpoint.流通市值>size_60)&(hs300s_stock_breakpoint.流通市值<=size_80)]['股票代码_Stkcd']
    hs300s_stock_size_5=hs300s_stock_breakpoint[hs300s_stock_breakpoint.流通市值>size_80]['股票代码_Stkcd']
    size_group=(hs300s_stock_size_1,hs300s_stock_size_2,hs300s_stock_size_3,hs300s_stock_size_4,hs300s_stock_size_5)
    ##按账面市值比分组   
    bm_20=np.percentile(hs300s_stock_breakpoint['账面市值比'],20) 
    bm_40=np.percentile(hs300s_stock_breakpoint['账面市值比'],40)
    bm_60=np.percentile(hs300s_stock_breakpoint['账面市值比'],60) 
    bm_80=np.percentile(hs300s_stock_breakpoint['账面市值比'],80)

    hs300s_stock_bm_1=hs300s_stock_breakpoint[hs300s_stock_breakpoint.账面市值比<=bm_20]['股票代码_Stkcd']
    hs300s_stock_bm_2=hs300s_stock_breakpoint[(hs300s_stock_breakpoint.账面市值比>bm_20)&(hs300s_stock_breakpoint.账面市值比<=bm_40)]['股票代码_Stkcd']
    hs300s_stock_bm_3=hs300s_stock_breakpoint[(hs300s_stock_breakpoint.账面市值比>bm_40)&(hs300s_stock_breakpoint.账面市值比<=bm_60)]['股票代码_Stkcd']
    hs300s_stock_bm_4=hs300s_stock_breakpoint[(hs300s_stock_breakpoint.账面市值比>bm_60)&(hs300s_stock_breakpoint.账面市值比<=bm_80)]['股票代码_Stkcd']
    hs300s_stock_bm_5=hs300s_stock_breakpoint[hs300s_stock_breakpoint.账面市值比>bm_80]['股票代码_Stkcd']
    bm_group=(hs300s_stock_bm_1,hs300s_stock_bm_2,hs300s_stock_bm_3,hs300s_stock_bm_4,hs300s_stock_bm_5)

    
    group_25_oneyear=DataFrame()
    for i in range(0,5):
        for j in range(0,5):
            group_25_temp=DataFrame(list(set(size_group[i]).intersection(set(bm_group[j]))))
            group_25_temp.columns=['股票代码_Stkcd']
            group_25_temp=pd.merge(group_25_temp,hs300s_stock_m)
            ##先算超额收益率再加权
            group_25_temp['加权超额收益率_exWeiretun']=(group_25_temp['流通市值']/group_25_temp['流通市值'].sum())*(group_25_temp['月收益率_Monret']-group_25_temp['月无风险收益率_Monrfret'])
            ex_Weireturn=[]            
            ex_Weireturn.append(group_25_temp[(group_25_temp.日期_Date>=breakyear+'-06-1  00:00:00')&(group_25_temp.日期_Date<=breakyear+'-06-30  00:00:00')]['加权超额收益率_exWeiretun'].sum())
            ex_Weireturn.append(group_25_temp[(group_25_temp.日期_Date>=breakyear+'-07-1  00:00:00')&(group_25_temp.日期_Date<=breakyear+'-07-31  00:00:00')]['加权超额收益率_exWeiretun'].sum())
            ex_Weireturn.append(group_25_temp[(group_25_temp.日期_Date>=breakyear+'-08-1  00:00:00')&(group_25_temp.日期_Date<=breakyear+'-08-31  00:00:00')]['加权超额收益率_exWeiretun'].sum())
            ex_Weireturn.append(group_25_temp[(group_25_temp.日期_Date>=breakyear+'-09-1  00:00:00')&(group_25_temp.日期_Date<=breakyear+'-09-30  00:00:00')]['加权超额收益率_exWeiretun'].sum())
            ex_Weireturn.append(group_25_temp[(group_25_temp.日期_Date>=breakyear+'-10-1  00:00:00')&(group_25_temp.日期_Date<=breakyear+'-10-31  00:00:00')]['加权超额收益率_exWeiretun'].sum())
            ex_Weireturn.append(group_25_temp[(group_25_temp.日期_Date>=breakyear+'-11-1  00:00:00')&(group_25_temp.日期_Date<=breakyear+'-11-30  00:00:00')]['加权超额收益率_exWeiretun'].sum())
            ex_Weireturn.append(group_25_temp[(group_25_temp.日期_Date>=breakyear+'-12-1  00:00:00')&(group_25_temp.日期_Date<=breakyear+'-12-31  00:00:00')]['加权超额收益率_exWeiretun'].sum())
            ex_Weireturn.append(group_25_temp[(group_25_temp.日期_Date>=breakyear1+'-1-1  00:00:00')&(group_25_temp.日期_Date<=breakyear1+'-1-31  00:00:00')]['加权超额收益率_exWeiretun'].sum())
            if (breakyear1=='2008')|(breakyear1=='2012')|(breakyear1=='2016'):
                ex_Weireturn.append(group_25_temp[(group_25_temp.日期_Date>=breakyear1+'-2-1  00:00:00')&(group_25_temp.日期_Date<=breakyear1+'-2-29  00:00:00')]['加权超额收益率_exWeiretun'].sum())
            else:
                ex_Weireturn.append(group_25_temp[(group_25_temp.日期_Date>=breakyear1+'-2-1  00:00:00')&(group_25_temp.日期_Date<=breakyear1+'-2-28  00:00:00')]['加权超额收益率_exWeiretun'].sum())
                      
            ex_Weireturn.append(group_25_temp[(group_25_temp.日期_Date>=breakyear1+'-3-1  00:00:00')&(group_25_temp.日期_Date<=breakyear1+'-3-31  00:00:00')]['加权超额收益率_exWeiretun'].sum())
            ex_Weireturn.append(group_25_temp[(group_25_temp.日期_Date>=breakyear1+'-4-1  00:00:00')&(group_25_temp.日期_Date<=breakyear1+'-4-30  00:00:00')]['加权超额收益率_exWeiretun'].sum())
            ex_Weireturn.append(group_25_temp[(group_25_temp.日期_Date>=breakyear1+'-5-1  00:00:00')&(group_25_temp.日期_Date<=breakyear1+'-5-31  00:00:00')]['加权超额收益率_exWeiretun'].sum())
            col_name='size'+str(i+1)+'_'+'bm'+str(j+1)
            group_25_oneyear[col_name]=ex_Weireturn
    return (group_25_oneyear)                        


##计算市场因子
def calc_RM_Rf():
    market_file='C:/Users/heyouxin/Desktop/HS300数据/市场因子.xls'
    hs300s_index_m=pd.read_excel(market_file)
    Rm_Rf=hs300s_index_m['指数月收益率_IdxMonRet']-hs300s_index_m['月无风险收益率_Monrfret']
    return (Rm_Rf)

#计算动量因子
def calc_UMD(breakyear,breakyear1): 
    

    ##取出当期期末的hs300数据
    date1=breakyear1+'-05-01  00:00:00'
    date2=breakyear1+'-05-31  00:00:00'
    hs300s_stock_breakpoint1=hs300s_stock_m[(hs300s_stock_m.日期_Date>=date1)&(hs300s_stock_m.日期_Date<=date2)].dropna()
     
    ##按期末的收益率分组
    return_30=np.percentile(hs300s_stock_breakpoint1['月收益率_Monret'],30) 
    return_70=np.percentile(hs300s_stock_breakpoint1['月收益率_Monret'],70) 
   
    hs300s_stock_return_D=hs300s_stock_breakpoint1[hs300s_stock_breakpoint1.月收益率_Monret<=return_30]['股票代码_Stkcd']
    hs300s_stock_return_U=hs300s_stock_breakpoint1[hs300s_stock_breakpoint1.月收益率_Monret>=return_70]['股票代码_Stkcd']
    return_group=(hs300s_stock_return_U,hs300s_stock_return_D)

    
    group_return_oneyear=DataFrame()
    for i in range(0,2):
        
        return_group_temp=DataFrame(return_group[i])
        return_group_temp.columns=['股票代码_Stkcd']
        return_group_temp=pd.merge(return_group_temp.dropna(),hs300s_stock_m.dropna())
        #return_group_temp=pd.merge(return_group_temp,hs300s_stock_m)
        
        Return=[]            
        Return.append(return_group_temp[(return_group_temp.日期_Date>=breakyear+'-06-1  00:00:00')&(return_group_temp.日期_Date<=breakyear+'-06-30  00:00:00')]['月收益率_Monret'].dropna().mean())
        Return.append(return_group_temp[(return_group_temp.日期_Date>=breakyear+'-07-1  00:00:00')&(return_group_temp.日期_Date<=breakyear+'-07-31  00:00:00')]['月收益率_Monret'].dropna().mean())
        Return.append(return_group_temp[(return_group_temp.日期_Date>=breakyear+'-08-1  00:00:00')&(return_group_temp.日期_Date<=breakyear+'-08-31  00:00:00')]['月收益率_Monret'].dropna().mean())
        Return.append(return_group_temp[(return_group_temp.日期_Date>=breakyear+'-09-1  00:00:00')&(return_group_temp.日期_Date<=breakyear+'-09-30  00:00:00')]['月收益率_Monret'].dropna().mean())
        Return.append(return_group_temp[(return_group_temp.日期_Date>=breakyear+'-10-1  00:00:00')&(return_group_temp.日期_Date<=breakyear+'-10-31  00:00:00')]['月收益率_Monret'].dropna().mean())
        Return.append(return_group_temp[(return_group_temp.日期_Date>=breakyear+'-11-1  00:00:00')&(return_group_temp.日期_Date<=breakyear+'-11-30  00:00:00')]['月收益率_Monret'].dropna().mean())
        Return.append(return_group_temp[(return_group_temp.日期_Date>=breakyear+'-12-1  00:00:00')&(return_group_temp.日期_Date<=breakyear+'-12-31  00:00:00')]['月收益率_Monret'].dropna().mean())
        Return.append(return_group_temp[(return_group_temp.日期_Date>=breakyear1+'-1-1  00:00:00')&(return_group_temp.日期_Date<=breakyear1+'-1-31  00:00:00')]['月收益率_Monret'].dropna().mean())
        if (breakyear1=='2008')|(breakyear1=='2012')|(breakyear1=='2016'):
            Return.append(return_group_temp[(return_group_temp.日期_Date>=breakyear1+'-2-1  00:00:00')&(return_group_temp.日期_Date<=breakyear1+'-2-29  00:00:00')]['月收益率_Monret'].dropna().mean())
        else:
            Return.append(return_group_temp[(return_group_temp.日期_Date>=breakyear1+'-2-1  00:00:00')&(return_group_temp.日期_Date<=breakyear1+'-2-28  00:00:00')]['月收益率_Monret'].dropna().mean())
        Return.append(return_group_temp[(return_group_temp.日期_Date>=breakyear1+'-3-1  00:00:00')&(return_group_temp.日期_Date<=breakyear1+'-3-31  00:00:00')]['月收益率_Monret'].dropna().mean())
        Return.append(return_group_temp[(return_group_temp.日期_Date>=breakyear1+'-4-1  00:00:00')&(return_group_temp.日期_Date<=breakyear1+'-4-30  00:00:00')]['月收益率_Monret'].dropna().mean())
        Return.append(return_group_temp[(return_group_temp.日期_Date>=breakyear1+'-5-1  00:00:00')&(return_group_temp.日期_Date<=breakyear1+'-5-31  00:00:00')]['月收益率_Monret'].dropna().mean())
        if i==0:
            col_name='UpStock'
        else:
            col_name='DownStock'   
        group_return_oneyear[col_name]=Return
    #group_return_oneyear['动量因子UMD']=group_return_oneyear['UpStock']-group_return_oneyear['DownStock']
    UMD_temp=group_return_oneyear['UpStock']-group_return_oneyear['DownStock']
    return (UMD_temp)                        


    
##CAPM模型回归
def do_regression_CAPM(R_25_group,Rm_Rf):
    #(R_25_group,SMB,HML,Rm_Rf,UMD)=calc_factors()
    global columns,index
    columns=['Low_BE/ME','2','3','4','High_BE/ME']
    index=['Small_Size','2','3','4','Big_Size']
    alpha1=[]
    t_alpha1=[]
    belta_mkt=[] 
    R2=[]
    for i in range(1,6):
        for j in range(1,6):
            colname='size'+str(i)+'_bm'+str(j)        
            fit=sm.OLS(np.array(R_25_group[colname]),sm.add_constant(Rm_Rf)).fit()
            alpha1=np.append(alpha1,fit.params[0])
            t_alpha1=np.append(t_alpha1,fit.tvalues[0])
            belta_mkt=np.append(belta_mkt,fit.params[1])
            R2=np.append(R2,fit.rsquared)
            
    alpha_CAPM=pd.DataFrame(DataFrame(alpha1).values.reshape(5,5))
    alpha_CAPM.columns=columns
    alpha_CAPM.index=index
  
    t_alpha_CAPM=pd.DataFrame(DataFrame(t_alpha1).values.reshape(5,5))
    t_alpha_CAPM.columns=columns
    t_alpha_CAPM.index=index
    
    belta_mkt_CAPM=pd.DataFrame(DataFrame(belta_mkt).values.reshape(5,5))
    belta_mkt_CAPM.columns=columns
    belta_mkt_CAPM.index=index
    
    R2_CAPM=pd.DataFrame(DataFrame(R2).values.reshape(5,5))
    R2_CAPM.columns=columns
    R2_CAPM.index=index
    
    return(alpha_CAPM,t_alpha_CAPM,belta_mkt_CAPM,R2_CAPM)
    
    
        
    
    
    
    #fit=sm.OLS(np.array(R_25_group[colname]),sm.add_constant(Rm_Rf)).fit()
    #fit.summary()
    #fit.params[1]
    #fit.tvalues[0]
    #return (fit)

##两因子回归
def do_regression_2factors(R_25_group,Rm_Rf,HML):
    #(R_25_group,SMB,HML,Rm_Rf,UMD)=calc_factors()
    alpha1=[]
    t_alpha1=[]
    belta_mkt=[] 
    belta_hml=[]
    R2=[]
    for i in range(1,6):
        for j in range(1,6):
            colname='size'+str(i)+'_bm'+str(j)
            X=np.vstack((Rm_Rf,HML)).transpose()
            fit=sm.OLS(np.array(R_25_group[colname]),sm.add_constant(X)).fit()
            alpha1=np.append(alpha1,fit.params[0])
            t_alpha1=np.append(t_alpha1,fit.tvalues[0])
            belta_mkt=np.append(belta_mkt,fit.params[1])
            belta_hml=np.append(belta_hml,fit.params[2])
            R2=np.append(R2,fit.rsquared)
            
    alpha_2FACTORS=pd.DataFrame(DataFrame(alpha1).values.reshape(5,5))
    alpha_2FACTORS.columns=columns
    alpha_2FACTORS.index=index
  
    t_alpha_2FACTORS=pd.DataFrame(DataFrame(t_alpha1).values.reshape(5,5))
    t_alpha_2FACTORS.columns=columns
    t_alpha_2FACTORS.index=index
    
    belta_mkt_2FACTORS=pd.DataFrame(DataFrame(belta_mkt).values.reshape(5,5))
    belta_mkt_2FACTORS.columns=columns
    belta_mkt_2FACTORS.index=index
    
    belta_hml_2FACTORS=pd.DataFrame(DataFrame(belta_hml).values.reshape(5,5))
    belta_hml_2FACTORS.columns=columns
    belta_hml_2FACTORS.index=index
    
    
    R2_2FACTORS=pd.DataFrame(DataFrame(R2).values.reshape(5,5))
    R2_2FACTORS.columns=columns
    R2_2FACTORS.index=index
    
    return(alpha_2FACTORS,t_alpha_2FACTORS,belta_mkt_2FACTORS,belta_hml_2FACTORS,R2_2FACTORS)



##三因子回归
def do_regression_3factors(R_25_group,Rm_Rf,HML,SMB):
    #(R_25_group,SMB,HML,Rm_Rf,UMD)=calc_factors()
    alpha1=[]
    t_alpha1=[]
    belta_mkt=[] 
    belta_hml=[]
    belta_smb=[]
    R2=[]
    for i in range(1,6):
        for j in range(1,6):
            colname='size'+str(i)+'_bm'+str(j)
            X=np.vstack((Rm_Rf,HML,SMB)).transpose()
            fit=sm.OLS(np.array(R_25_group[colname]),sm.add_constant(X)).fit()
            alpha1=np.append(alpha1,fit.params[0])
            t_alpha1=np.append(t_alpha1,fit.tvalues[0])
            belta_mkt=np.append(belta_mkt,fit.params[1])
            belta_hml=np.append(belta_hml,fit.params[2])
            belta_smb=np.append(belta_smb,fit.params[3])
            R2=np.append(R2,fit.rsquared)
            
    alpha_3factors=pd.DataFrame(DataFrame(alpha1).values.reshape(5,5))
    alpha_3factors.columns=columns
    alpha_3factors.index=index
  
    t_alpha_3factors=pd.DataFrame(DataFrame(t_alpha1).values.reshape(5,5))
    t_alpha_3factors.columns=columns
    t_alpha_3factors.index=index
    
    belta_mkt_3factors=pd.DataFrame(DataFrame(belta_mkt).values.reshape(5,5))
    belta_mkt_3factors.columns=columns
    belta_mkt_3factors.index=index
    
    belta_hml_3factors=pd.DataFrame(DataFrame(belta_hml).values.reshape(5,5))
    belta_hml_3factors.columns=columns
    belta_hml_3factors.index=index
    
    belta_smb_3factors=pd.DataFrame(DataFrame(belta_smb).values.reshape(5,5))
    belta_smb_3factors.columns=columns
    belta_smb_3factors.index=index
    
    
    R2_3factors=pd.DataFrame(DataFrame(R2).values.reshape(5,5))
    R2_3factors.columns=columns
    R2_3factors.index=index
    
    return(alpha_3factors,t_alpha_3factors,belta_mkt_3factors,belta_hml_3factors,belta_smb_3factors,R2_3factors)




##四因子回归
def do_regression_4factors(R_25_group,Rm_Rf,HML,SMB,UMD):
    #(R_25_group,SMB,HML,Rm_Rf,UMD)=calc_factors()
    alpha1=[]
    t_alpha1=[]
    belta_mkt=[] 
    belta_hml=[]
    belta_smb=[]
    belta_umd=[]
    R2=[]
    for i in range(1,6):
        for j in range(1,6):
            colname='size'+str(i)+'_bm'+str(j)
            X=np.vstack((Rm_Rf,HML,SMB,UMD)).transpose()
            fit=sm.OLS(np.array(R_25_group[colname]),sm.add_constant(X)).fit()
            alpha1=np.append(alpha1,fit.params[0])
            t_alpha1=np.append(t_alpha1,fit.tvalues[0])
            belta_mkt=np.append(belta_mkt,fit.params[1])
            belta_hml=np.append(belta_hml,fit.params[2])
            belta_smb=np.append(belta_smb,fit.params[3])
            belta_umd=np.append(belta_umd,fit.params[4])
            R2=np.append(R2,fit.rsquared)
            
    alpha_4factors=pd.DataFrame(DataFrame(alpha1).values.reshape(5,5))
    alpha_4factors.columns=columns
    alpha_4factors.index=index
  
    t_alpha_4factors=pd.DataFrame(DataFrame(t_alpha1).values.reshape(5,5))
    t_alpha_4factors.columns=columns
    t_alpha_4factors.index=index
    
    belta_mkt_4factors=pd.DataFrame(DataFrame(belta_mkt).values.reshape(5,5))
    belta_mkt_4factors.columns=columns
    belta_mkt_4factors.index=index
    
    belta_hml_4factors=pd.DataFrame(DataFrame(belta_hml).values.reshape(5,5))
    belta_hml_4factors.columns=columns
    belta_hml_4factors.index=index
    
    belta_smb_4factors=pd.DataFrame(DataFrame(belta_smb).values.reshape(5,5))
    belta_smb_4factors.columns=columns
    belta_smb_4factors.index=index
   
    belta_umd_4factors=pd.DataFrame(DataFrame(belta_umd).values.reshape(5,5))
    belta_umd_4factors.columns=columns
    belta_umd_4factors.index=index
    
    R2_4factors=pd.DataFrame(DataFrame(R2).values.reshape(5,5))
    R2_4factors.columns=columns
    R2_4factors.index=index

    return(alpha_4factors,t_alpha_4factors,belta_mkt_4factors,belta_hml_4factors,belta_smb_4factors,belta_umd_4factors,R2_4factors)


def display(R_25_group,SMB,HML,Rm_Rf,UMD):
    
    Er=pd.DataFrame(R_25_group.mean().values.reshape(5,5))
    columns=['Low_BE/ME','2','3','4','High_BE/ME']
    index=['Small_Size','2','3','4','Big_Size']
    Er.columns=columns
    Er.index=index
    print(Er)
    
    (alpha_CAPM,t_alpha_CAPM,belta_mkt_CAPM,R2_CAPM)=do_regression_CAPM(R_25_group,Rm_Rf)
    print(alpha_CAPM)
    print(t_alpha_CAPM)
    print(belta_mkt_CAPM)
    print(R2_CAPM)
    
    
    (alpha_2factors,t_alpha_2factors,belta_mkt_2factors,belta_hml_2factors,R2_2factors)=do_regression_2factors(R_25_group,Rm_Rf,HML)
    print(alpha_2factors,belta_mkt_2factors,belta_hml_2factors,R2_2factors)
  
    
    (alpha_3factors,t_alpha_3factors,belta_mkt_3factors,belta_hml_3factors,belta_smb_3factors,R2_3factors)=do_regression_3factors(R_25_group,Rm_Rf,HML,SMB)
    print(alpha_3factors,t_alpha_3factors,belta_mkt_3factors,belta_hml_3factors,belta_smb_3factors,R2_3factors)

    
    (alpha_4factors,t_alpha_4factors,belta_mkt_4factors,belta_hml_4factors,belta_smb_4factors,belta_umd_4factors,R2_4factors)=do_regression_4factors(R_25_group,Rm_Rf,HML,SMB,UMD)
    print(alpha_4factors,t_alpha_4factors,belta_mkt_4factors,belta_hml_4factors,belta_smb_4factors,belta_umd_4factors,R2_4factors)
    

    
    
    
    
    




