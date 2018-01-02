# -*- coding: utf-8 -*-
"""
Created on Sun Dec 10 22:10:17 2017

@author: 何友鑫
"""
from datetime import datetime
import pandas as pd
def getDate():
    date_1=pd.date_range('06/27/1996','12/07/2017',freq='W-THU')
    date_1=list(date_1.strftime('%Y%m%d'))
    date_2=pd.date_range('06/27/1996','12/07/2017',freq='W-FRI')
    date_2=list(date_2.strftime('%Y%m%d'))
    date_3=pd.date_range('06/27/1996','12/07/2017',freq='W-SUN')
    date_3=list(date_3.strftime('%Y%m%d'))
 
    '''
    date_1.extend(date_2)
    date_1.extend(date_3)
    
    date_all=date_1
    '''
    return (date_1,date_2,date_3)