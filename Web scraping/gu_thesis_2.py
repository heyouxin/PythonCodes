# -*- coding: utf-8 -*-
"""
Created on Sat May 26 11:19:44 2018

@author: 何友鑫
"""

# -*- coding: utf-8 -*-
"""
Created on Sun May 20 14:42:21 2018

@author: 何友鑫
"""

import pandas as pd
import numpy as np
CEPS=pd.read_csv("C:/Users/heyouxin/Desktop/guting/CEPS.csv",encoding='gbk',usecols=['ids','ids_score','stu_f1','clsids','schids','ctyids','assess','depress','blue','unhappy','pess','sad','fulfill','confident','public','private','b14b1','b14b2'])
#缺失值记为0
where_are_nan = np.isnan(CEPS)  
CEPS[where_are_nan] = 0 

#周末作业总时长，按小时计
CEPS['b14b_1_2']=CEPS['b14b1']+CEPS['b14b2']/60



#CEPS2=CEPS[]
#语文 男对男
CEPS['assess_m_m']=0.0
#女对男
CEPS['assess_f_m']=0.0
CEPS['assess_m_f']=0.0
CEPS['assess_f_f']=0.0
    
    
CEPS['depress_m_m']=0.0
CEPS['depress_f_m']=0.0
CEPS['depress_m_f']=0.0
CEPS['depress_f_f']=0.0
  
CEPS['blue_m_m']=0.0
CEPS['blue_f_m']=0.0
CEPS['blue_m_f']=0.0
CEPS['blue_f_f']=0.0
    
CEPS['unhappy_m_m']=0.0
CEPS['unhappy_f_m']=0.0
CEPS['unhappy_m_f']=0.0
CEPS['unhappy_f_f']=0.0    

CEPS['pess_m_m']=0.0
CEPS['pess_f_m']=0.0
CEPS['pess_m_f']=0.0
CEPS['pess_f_f']=0.0     
    
CEPS['b14b_1_2_m_m']=0.0
CEPS['b14b_1_2_f_m']=0.0
CEPS['b14b_1_2_m_f']=0.0
CEPS['b14b_1_2_f_f']=0.0     

CEPS['sad_m_m']=0.0
CEPS['sad_f_m']=0.0
CEPS['sad_m_f']=0.0
CEPS['sad_f_f']=0.0     

    
CEPS['fulfill_m_m']=0.0
CEPS['fulfill_f_m']=0.0
CEPS['fulfill_m_f']=0.0
CEPS['fulfill_f_f']=0.0
  
CEPS['confident_m_m']=0.0
CEPS['confident_f_m']=0.0
CEPS['confident_m_f']=0.0
CEPS['confident_f_f']=0.0
    
CEPS['public_m_m']=0.0
CEPS['public_f_m']=0.0
CEPS['public_m_f']=0.0
CEPS['public_f_f']=0.0    

CEPS['private_m_m']=0.0
CEPS['private_f_m']=0.0
CEPS['private_m_f']=0.0
CEPS['private_f_f']=0.0    
    
    
for r in range(0,len(CEPS['ids'])):
#for r in range(0,1):
    classmate_set=CEPS[(CEPS.ids!=CEPS['ids'][r])&(CEPS.ids_score==CEPS['ids_score'][r])&(CEPS.clsids==CEPS['clsids'][r])&(CEPS.schids==CEPS['schids'][r])&((CEPS.ctyids==CEPS['ctyids'][r]))]
  
    male=classmate_set[classmate_set['stu_f1']==0]
    female=classmate_set[classmate_set['stu_f1']==1]
    if CEPS['stu_f1'][r]==0:
        CEPS.loc[r,'assess_m_m']=male['assess'].mean()
        CEPS.loc[r,'assess_f_m']=female['assess'].mean()
        
        CEPS.loc[r,'depress_m_m']=male['depress'].mean()
        CEPS.loc[r,'depress_f_m']=female['depress'].mean()

        CEPS.loc[r,'blue_m_m']=male['blue'].mean()
        CEPS.loc[r,'blue_f_m']=female['blue'].mean()
        
        CEPS.loc[r,'unhappy_m_m']=male['unhappy'].mean()
        CEPS.loc[r,'unhappy_f_m']=female['unhappy'].mean()
        
        CEPS.loc[r,'pess_m_m']=male['pess'].mean()
        CEPS.loc[r,'pess_f_m']=female['pess'].mean()

        CEPS.loc[r,'b14b_1_2_m_m']=male['b14b_1_2'].mean()
        CEPS.loc[r,'b14b_1_2_f_m']=female['b14b_1_2'].mean()
        
        CEPS.loc[r,'sad_m_m']=male['sad'].mean()
        CEPS.loc[r,'sad_f_m']=female['sad'].mean()
        
        CEPS.loc[r,'fulfill_m_m']=male['fulfill'].mean()
        CEPS.loc[r,'fulfill_f_m']=female['fulfill'].mean()
        
        CEPS.loc[r,'confident_m_m']=male['confident'].mean()
        CEPS.loc[r,'confident_f_m']=female['confident'].mean()

        CEPS.loc[r,'public_m_m']=male['public'].mean()
        CEPS.loc[r,'public_f_m']=female['public'].mean()
        
        CEPS.loc[r,'private_m_m']=male['private'].mean()
        CEPS.loc[r,'private_f_m']=female['private'].mean()
        

    if CEPS['stu_f1'][r]==1:
        CEPS.loc[r,'assess_m_f']=male['assess'].mean()
        CEPS.loc[r,'assess_f_f']=female['assess'].mean()
        
        CEPS.loc[r,'depress_m_f']=male['depress'].mean()
        CEPS.loc[r,'depress_f_f']=female['depress'].mean()

        CEPS.loc[r,'blue_m_f']=male['blue'].mean()
        CEPS.loc[r,'blue_f_f']=female['blue'].mean()
        
        CEPS.loc[r,'unhappy_m_f']=male['unhappy'].mean()
        CEPS.loc[r,'unhappy_f_f']=female['unhappy'].mean()
        
        CEPS.loc[r,'pess_m_f']=male['pess'].mean()
        CEPS.loc[r,'pess_f_f']=female['pess'].mean()

        CEPS.loc[r,'b14b_1_2_m_f']=male['b14b_1_2'].mean()
        CEPS.loc[r,'b14b_1_2_f_f']=female['b14b_1_2'].mean()
        
        CEPS.loc[r,'sad_m_f']=male['sad'].mean()
        CEPS.loc[r,'sad_f_f']=female['sad'].mean()
        
        CEPS.loc[r,'fulfill_m_f']=male['fulfill'].mean()
        CEPS.loc[r,'fulfill_f_f']=female['fulfill'].mean()
        
        CEPS.loc[r,'confident_m_f']=male['confident'].mean()
        CEPS.loc[r,'confident_f_f']=female['confident'].mean()

        CEPS.loc[r,'public_m_f']=male['public'].mean()
        CEPS.loc[r,'public_f_f']=female['public'].mean()
        
        CEPS.loc[r,'private_m_f']=male['private'].mean()
        CEPS.loc[r,'private_f_f']=female['private'].mean()
        
CEPS.to_excel("CEPS_effect_2.xlsx",index=False)  

CEPS2=pd.read_excel("CEPS_effect_2.xlsx")
CEPS=pd.read_csv("C:/Users/heyouxin/Desktop/guting/updated_CEPS_effect.csv",encoding='gbk')
CEPS_merged=pd.merge(CEPS,CEPS2,how='inner')
CEPS_merged.to_csv("C:/Users/heyouxin/Desktop/guting/updated_CEPS_effect_v2.csv")   
    