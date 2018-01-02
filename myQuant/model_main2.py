# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 12:16:54 2017

@author: 何友鑫
"""
from fama_model import Model_Fama 
import numpy as np
import pandas as pd
if __name__ == "__main__":

    mod=Model_Fama()
    (R_25_group,SMB,HML,Rm_Rf,UMD)=mod.calc_factors()

    Er=pd.DataFrame(R_25_group.mean().values.reshape(5,5))
    columns=['Low_BE/ME','2','3','4','High_BE/ME']
    index=['Small_Size','2','3','4','Big_Size']
    Er.columns=columns
    Er.index=index
    Er
    
    (alpha_CAPM,t_alpha_CAPM,belta_mkt_CAPM,R2_CAPM)=mod.do_regression_CAPM(R_25_group,Rm_Rf)
    alpha_CAPM
    t_alpha_CAPM
    belta_mkt_CAPM
    R2_CAPM
    
    
    (alpha_2factors,t_alpha_2factors,belta_mkt_2factors,belta_hml_2factors,R2_2factors)=mod.do_regression_2factors(R_25_group,Rm_Rf,HML)
    alpha_2factors
    t_alpha_2factors
    belta_mkt_2factors
    belta_hml_2factors
    R2_2factors
    
    (alpha_3factors,t_alpha_3factors,belta_mkt_3factors,belta_hml_3factors,belta_smb_3factors,R2_3factors)=mod.do_regression_3factors(R_25_group,Rm_Rf,HML,SMB)
    alpha_3factors
    t_alpha_3factors
    belta_mkt_3factors
    belta_hml_3factors
    belta_smb_3factors
    R2_3factors
    
    
    (alpha_4factors,t_alpha_4factors,belta_mkt_4factors,belta_hml_4factors,belta_smb_4factors,belta_umd_4factors,R2_4factors)=mod.do_regression_4factors(R_25_group,Rm_Rf,HML,SMB,UMD)
    alpha_4factors
    t_alpha_4factors
    belta_mkt_4factors
    belta_hml_4factors
    belta_smb_4factors
    belta_umd_4factors
    R2_4factors

    
    
    ####以下将样本分为两部分重复step 2 的过程 直接用封装的函数重复这个过程
    
    mod.display(R_25_group[0:72],SMB[0:72],HML[0:72],Rm_Rf[0:72],UMD[0:72])
    
    mod.display(R_25_group[72:144],SMB[72:144],HML[72:144],Rm_Rf[72:144],UMD[72:144])
    
        
    
    
    
    
    
    
    
    
    
    
    '''
     alpha1=[]
    t_alpha1=[]
    belta_mkt=[]    
    for i in range(1,6):
        for j in range(1,6):
            colname='size'+str(i)+'_bm'+str(j)        
            fit=sm.OLS(np.array(R_25_group[colname]),sm.add_constant(Rm_Rf)).fit()
            alpha1=np.append(alpha1,fit.params[0])
            t_alpha1=np.append(t_alpha1,fit.tvalues[0])
            belta_mkt=np.append(belta_mkt,fit.params[1])
            
    alpha_CAPM=pd.DataFrame(DataFrame(alpha1).values.reshape(5,5))
    alpha_CAPM.columns=columns
    alpha_CAPM.index=index
  
    t_alpha_CAPM=pd.DataFrame(t_alpha1.values.reshape(5,5))
    t_alpha_CAPM.columns=columns
    t_alpha_CAPM.index=index
    
    belta_mkt_CAPM=pd.DataFrame(belta_mkt.values.reshape(5,5))
    belta_mkt_CAPM.columns=columns
    belta_mkt_CAPM.index=index
    '''
    
    