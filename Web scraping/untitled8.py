# -*- coding: utf-8 -*-
"""
Created on Mon May 21 21:39:26 2018

@author: 何友鑫
"""

import pandas as pd
import numpy as np
CEPS=pd.read_csv("C:/Users/heyouxin/Desktop/guting/updated_CEPS.csv",encoding='gbk')
CEPS2=pd.read_excel("CEPS_effect2.xlsx")



CEPS_merged=pd.merge(CEPS,CEPS2,how='inner')

CEPS_merged.to_csv("C:/Users/heyouxin/Desktop/guting/updated_CEPS_effect.csv")