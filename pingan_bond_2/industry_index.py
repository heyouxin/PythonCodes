
# -*- coding: utf-8 -*-
"""
-----------------------
1.行业层面数据
2.按行业计算CAPM alpha belta
3.uncertainty belta
-----------------------
"""
import pandas as pd
import statsmodels.api as sm
import numpy as np
from dateutil.relativedelta import relativedelta


#bond=pd.read_excel("final_All_Data_0719.xlsx")[['code',']]

def Calculate_industry(bond,start,end,filename_capm,filename_zs, number_start=2,number_end=0):
    bond = bond.dropna()
    bond[start] = bond[start].map(pd.Timestamp)
    bond[end] = bond[end].map(pd.Timestamp)
    indust_table=pd.read_excel(filename_capm).dropna()
    try:
        indust_table = indust_table.set_index('time_report')
    except:
        indust_table = indust_table
    bond['SEC_NAME']=bond['industry']+str('指数')
    bond['date_start_before'] = bond[start].map(lambda x:x-relativedelta(months=6)) 
    bond.index = range(len(bond))
    #bond = df
    #bond = bond.rename(columns={'date_default':'date_end'})
    #bond = bond.reset_index().rename(columns={'index':'code'})
    ## 分行业做CAPM回归
    l_name=[]
    l_alpha=[]
    l_belta=[]
    for i in range(0,len(bond)):
        if bond.loc[i,'SEC_NAME']==np.nan:
            continue
        indust_group=indust_table.loc[indust_table['SEC_NAME']==bond.loc[i,'SEC_NAME']]
        try:
            indust_group=indust_group[(indust_group.index >= bond['date_start_before'][i]) & (indust_group.index < bond[end][i])]
            fit=sm.OLS(np.array(indust_group['Ri_Rf']),sm.add_constant(np.array(indust_group['Rm_Rf']))).fit()
            l_belta.append(fit.params[1])
            l_name.append(bond['code'][i])
            l_alpha.append(fit.params[0])
        except:
            l_belta.append(np.nan)
            l_name.append(bond['code'][i])
            l_alpha.append(np.nan)
    alpha_belta={"code":l_name,"alpha":l_alpha,"belta":l_belta}
    alpha_belta=pd.DataFrame(alpha_belta)
    
    indust_un=pd.read_excel(filename_zs).dropna()
    try:
        indust_un = indust_un.set_index('time_report')
    except:
        indust_un = indust_un
    ## 分行业 每20个月一个周期回归一次，取平均
    l_name = []
    l_yj=[]
    l_yz=[]
    
    for i in range(0,len(bond)):
        indust_group=indust_un.loc[indust_un['SEC_NAME']==bond.loc[i,'SEC_NAME']]
        group=indust_group[(indust_group.index >= bond['date_start_before'][i]) & (indust_group.index < bond[end][i])]
        
        belta_yj=[]
        belta_yz=[]
        if len(group) <= 20:
            try:
                model=sm.OLS(np.array(group.ret[0:len(group)]),sm.add_constant(np.array(group.yj_index[0:len(group)]))).fit()
                l_yj.append(model.params[1])
            except:
                l_yj.append(np.nan)
            
            try:
                model=sm.OLS(np.array(group.ret[0:len(group)]),sm.add_constant(np.array(group.yz_index[0:len(group)]))).fit()
                l_yz.append(model.params[1])
            except:
                l_yz.append(np.nan)
         
            l_name.append(bond['code'][i])
                
        else:
            for j in range(20,len(group)):
                model = sm.OLS(np.array(group.ret[j-20:j]),sm.add_constant(np.array(group.yj_index[j-20:j]))).fit()
                belta_yj.append(model.params[1])
                
                model = sm.OLS(np.array(group.ret[j-20:j]),sm.add_constant(np.array(group.yz_index[j-20:j]))).fit()
                belta_yz.append(model.params[1])
                
            l_name.append(bond['code'][i])
            if len(l_yj)<=(number_start): 
                l_yj.append(np.array(belta_yj).mean())
                l_yz.append(np.array(belta_yz).mean())
            else:
                if number_end==0:
                    l_yj.append(np.array(belta_yj)[-number_start:].mean())
                    l_yz.append(np.array(belta_yz)[-number_start:].mean())
                else:
                    l_yj.append(np.array(belta_yj)[-number_start:-number_end].mean())
                    l_yz.append(np.array(belta_yz)[-number_start:-number_end].mean())
            
    beltas={"code":l_name,"belta_yj":l_yj,"belta_yz":l_yz}
    beltas=pd.DataFrame(beltas)
    
    Hangye = pd.concat([alpha_belta.set_index('code'),beltas.set_index('code')],axis=1,join='inner')
    return(Hangye)

'''
df1 = pd.read_excel('Already_Data_Original_0718_无行业.xlsx').set_index('code')
df2 = Hangye
df3 = pd.concat([df1,df2],axis=1,join='inner')
df3 = df3.reset_index().rename(columns={'index':'code'})
df3.to_excel('Already_0719.xlsx',index=False)
df1 = df3
df2 = pd.read_excel('0719短期融资券_部分.xlsx').set_index('code')

Default_riqi = pd.read_excel('Default日期.xlsx').set_index('code')
Default_hangye = pd.read_excel('违约债券行业.xlsx').set_index('code')
df = pd.concat([Default_riqi,Default_hangye],axis=1,join='inner')

Hangye = Hangye.reset_index().rename(columns={'index':'code'})
Hangye.to_excel('Default_hangye.xlsx',index=False)
df1 = pd.read_excel('Default_Data_Original_mean_0718_3_无行业.xlsx').set_index('code')
df2 = pd.read_excel('Default_hangye.xlsx').set_index('code')
df = pd.concat([df1,df2],axis=1,join='inner')
df = df.reset_index().rename(columns={'index':'code'})
df.to_excel('0719Default.xlsx',index=False)'''


