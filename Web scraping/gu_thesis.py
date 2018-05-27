# -*- coding: utf-8 -*-
"""
Created on Sun May 20 14:42:21 2018

@author: 何友鑫
"""

import pandas as pd
import numpy as np
CEPS=pd.read_csv("C:/Users/heyouxin/Desktop/guting/CEPS.csv",encoding='gbk',usecols=['ids','ids_score','stu_f1','clsids','schids','ctyids','stdchn','stdmat','stdeng','b14a1','b14a2','b18a','b18b','cog3pl'])
CEPS['stdtotal']=CEPS['stdchn']+CEPS['stdmat']+CEPS['stdeng']
#缺失值记为0
where_are_nan = np.isnan(CEPS)  
CEPS[where_are_nan] = 0 

#作业总时长，按小时计
CEPS['b14a_1_2']=CEPS['b14a1']+CEPS['b14a2']/60

#睡眠总时长，按小时计
CEPS['b18_a_b']=CEPS['b18a']+CEPS['b18b']/60
#CEPS[CEPS['b18a']>12]

#CEPS2=CEPS[]
#语文 男对男
CEPS['chn_m_m']=0.0
#女对男
CEPS['chn_f_m']=0.0
CEPS['chn_m_f']=0.0
CEPS['chn_f_f']=0.0
    
    
CEPS['mat_m_m']=0.0
CEPS['mat_f_m']=0.0
CEPS['mat_m_f']=0.0
CEPS['mat_f_f']=0.0
  
CEPS['eng_m_m']=0.0
CEPS['eng_f_m']=0.0
CEPS['eng_m_f']=0.0
CEPS['eng_f_f']=0.0
    
CEPS['total_m_m']=0.0
CEPS['total_f_m']=0.0
CEPS['total_m_f']=0.0
CEPS['total_f_f']=0.0    

CEPS['cog3pl_m_m']=0.0
CEPS['cog3pl_f_m']=0.0
CEPS['cog3pl_m_f']=0.0
CEPS['cog3pl_f_f']=0.0     
    
CEPS['b14a_1_2_m_m']=0.0
CEPS['b14a_1_2_f_m']=0.0
CEPS['b14a_1_2_m_f']=0.0
CEPS['b14a_1_2_f_f']=0.0     

CEPS['b18_a_b_m_m']=0.0
CEPS['b18_a_b_f_m']=0.0
CEPS['b18_a_b_m_f']=0.0
CEPS['b18_a_b_f_f']=0.0     

for r in range(0,len(CEPS['ids'])):
#for r in range(0,1):
    classmate_set=CEPS[(CEPS.ids!=CEPS['ids'][r])&(CEPS.ids_score==CEPS['ids_score'][r])&(CEPS.clsids==CEPS['clsids'][r])&(CEPS.schids==CEPS['schids'][r])&((CEPS.ctyids==CEPS['ctyids'][r]))]
    '''
    l_chn_m_m=[]
    l_chn_f_m=[]
    l_chn_m_f=[]
    l_chn_f_f=[]
    
    l_mat_m_m=[]
    l_mat_f_m=[]
    l_mat_m_f=[]
    l_mat_f_f=[]
    
    l_eng_m_m=[]
    l_eng_f_m=[]
    l_eng_m_f=[]
    l_eng_f_f=[]
    
    l_total_m_m=[]
    l_total_f_m=[]
    l_total_m_f=[]
    l_total_f_f=[]
    
    l_cog3pl_m_m=[]
    l_cog3pl_f_m=[]
    l_cog3pl_m_f=[]
    l_cog3pl_f_f=[]
    
    l_b14a_1_2_m_m=[]
    l_b14a_1_2_f_m=[]
    l_b14a_1_2_m_f=[]
    l_b14a_1_2_f_f=[]
    
    l_b18_a_b_m_m=[]
    l_b18_a_b_f_m=[]
    l_b18_a_b_m_f=[]
    l_b18_a_b_f_f=[]
    '''
    male=classmate_set[classmate_set['stu_f1']==0]
    female=classmate_set[classmate_set['stu_f1']==1]
    if CEPS['stu_f1'][r]==0:
        CEPS.loc[r,'chn_m_m']=male['stdchn'].mean()
        CEPS.loc[r,'chn_f_m']=female['stdchn'].mean()
        
        CEPS.loc[r,'mat_m_m']=male['stdmat'].mean()
        CEPS.loc[r,'mat_f_m']=female['stdmat'].mean()

        CEPS.loc[r,'eng_m_m']=male['stdeng'].mean()
        CEPS.loc[r,'eng_f_m']=female['stdeng'].mean()
        
        CEPS.loc[r,'total_m_m']=male['stdtotal'].mean()
        CEPS.loc[r,'total_f_m']=female['stdtotal'].mean()
        
        CEPS.loc[r,'cog3pl_m_m']=male['cog3pl'].mean()
        CEPS.loc[r,'cog3pl_f_m']=female['cog3pl'].mean()

        CEPS.loc[r,'b14a_1_2_m_m']=male['b14a_1_2'].mean()
        CEPS.loc[r,'b14a_1_2_f_m']=female['b14a_1_2'].mean()
        
        CEPS.loc[r,'b18_a_b_m_m']=male['b18_a_b'].mean()
        CEPS.loc[r,'b18_a_b_f_m']=female['b18_a_b'].mean()
        

    if CEPS['stu_f1'][r]==1:
        CEPS.loc[r,'chn_m_f']=male['stdchn'].mean()
        CEPS.loc[r,'chn_f_f']=female['stdchn'].mean()
        
        CEPS.loc[r,'mat_m_f']=male['stdmat'].mean()
        CEPS.loc[r,'mat_f_f']=female['stdmat'].mean()

        CEPS.loc[r,'eng_m_f']=male['stdeng'].mean()
        CEPS.loc[r,'eng_f_f']=female['stdeng'].mean()
        
        CEPS.loc[r,'total_m_f']=male['stdtotal'].mean()
        CEPS.loc[r,'total_f_f']=female['stdtotal'].mean()
        
        CEPS.loc[r,'cog3pl_m_f']=male['cog3pl'].mean()
        CEPS.loc[r,'cog3pl_f_f']=female['cog3pl'].mean()

        CEPS.loc[r,'b14a_1_2_m_f']=male['b14a_1_2'].mean()
        CEPS.loc[r,'b14a_1_2_f_f']=female['b14a_1_2'].mean()
        
        CEPS.loc[r,'b18_a_b_m_f']=male['b18_a_b'].mean()
        CEPS.loc[r,'b18_a_b_f_f']=female['b18_a_b'].mean()
        
CEPS.to_excel("CEPS_effect.xlsx",index=False)
    '''
    for i in classmate_set.index:
        #男对男
        if (CEPS['stu_f1'][r]==0) & (classmate_set['stu_f1'][i]==0):
            l_chn_m_m.append(classmate_set['stdchn'][i])
            l_mat_m_m.append(classmate_set['stdmat'][i])
            l_eng_m_m.append(classmate_set['stdeng'][i])
            l_total_m_m.append(classmate_set['stdtotal'][i])
            l_cog3pl_m_m.append(classmate_set['cog3pl'][i])
            l_b14a_1_2_m_m.append(classmate_set['b14a_1_2'][i])
            l_b18_a_b_m_m.append(classmate_set['b18_a_b'][i])
            
        if (CEPS['stu_f1'][r]==0) & (classmate_set['stu_f1'][i]==1):
            l_chn_f_m.append(classmate_set['stdchn'][i])
            l_mat_f_m.append(classmate_set['stdmat'][i])
            l_eng_f_m.append(classmate_set['stdeng'][i])
            l_total_f_m.append(classmate_set['stdtotal'][i])
            l_cog3pl_f_m.append(classmate_set['cog3pl'][i])
            l_b14a_1_2_f_m.append(classmate_set['b14a_1_2'][i])
            l_b18_a_b_f_m.append(classmate_set['b18_a_b'][i])

        if (CEPS['stu_f1'][r]==1) & (classmate_set['stu_f1'][i]==0):
            l_chn_m_f.append(classmate_set['stdchn'][i])
            l_mat_m_f.append(classmate_set['stdmat'][i])
            l_eng_m_f.append(classmate_set['stdeng'][i])
            l_total_m_f.append(classmate_set['stdtotal'][i])
            l_cog3pl_m_f.append(classmate_set['cog3pl'][i])
            l_b14a_1_2_m_f.append(classmate_set['b14a_1_2'][i])
            l_b18_a_b_m_f.append(classmate_set['b18_a_b'][i])
        if (CEPS['stu_f1'][r]==1) & (classmate_set['stu_f1'][i]==1):
            l_chn_f_f.append(classmate_set['stdchn'][i])
            l_mat_f_f.append(classmate_set['stdmat'][i])
            l_eng_f_f.append(classmate_set['stdeng'][i])
            l_total_f_f.append(classmate_set['stdtotal'][i])
            l_cog3pl_f_f.append(classmate_set['cog3pl'][i])
            l_b14a_1_2_f_f.append(classmate_set['b14a_1_2'][i])
            l_b18_a_b_f_f.append(classmate_set['b18_a_b'][i])
   
    CEPS['chn_m_m'][r]=np.array(l_chn_m_m).mean()
    CEPS['chn_f_m'][r]=np.array(l_chn_f_m).mean()
    CEPS['chn_m_f'][r]=np.array(l_chn_m_f).mean()
    CEPS['chn_f_f'][r]=np.array(l_chn_f_f).mean()
        
        
    CEPS['mat_m_m'][r]=np.array(l_mat_m_m).mean()
    CEPS['mat_f_m'][r]=np.array(l_mat_f_m).mean()
    CEPS['mat_m_f'][r]=np.array(l_mat_m_f).mean()
    CEPS['mat_f_f'][r]=np.array(l_mat_f_f).mean()
      
    CEPS['eng_m_m'][r]=np.array(l_eng_m_m).mean()
    CEPS['eng_f_m'][r]=np.array(l_eng_f_m).mean()
    CEPS['eng_m_f'][r]=np.array(l_eng_m_f).mean()
    CEPS['eng_f_f'][r]=np.array(l_eng_f_f).mean()
        
    CEPS['total_m_m'][r]=np.array(l_total_m_m).mean()
    CEPS['total_f_m'][r]=np.array(l_total_f_m).mean()
    CEPS['total_m_f'][r]=np.array(l_total_m_f).mean()
    CEPS['total_f_f'][r]=np.array(l_total_f_f).mean()
    
    CEPS['cog3pl_m_m'][r]=np.array(l_cog3pl_m_m).mean()
    CEPS['cog3pl_f_m'][r]=np.array(l_cog3pl_f_m).mean()
    CEPS['cog3pl_m_f'][r]=np.array(l_cog3pl_m_f).mean()
    CEPS['cog3pl_f_f'][r]=np.array(l_cog3pl_f_f).mean()
        
    CEPS['b14a_1_2_m_m'][r]=np.array(l_b14a_1_2_m_m).mean()
    CEPS['b14a_1_2_f_m'][r]=np.array(l_b14a_1_2_f_m).mean()
    CEPS['b14a_1_2_m_f'][r]=np.array(l_b14a_1_2_m_f).mean()
    CEPS['b14a_1_2_f_f'][r]=np.array(l_b14a_1_2_f_f).mean()
    
    CEPS['b18_a_b_m_m'][r]=np.array(l_b18_a_b_m_m).mean()
    CEPS['b18_a_b_f_m'][r]=np.array(l_b18_a_b_f_m).mean()
    CEPS['b18_a_b_m_f'][r]=np.array(l_b18_a_b_m_f).mean()
    CEPS['b18_a_b_f_f'][r]=np.array(l_b18_a_b_f_f).mean()
    '''

    
    