# -*- coding: utf-8 -*-
"""
Created on Wed Sep 19 14:04:21 2018

@author: John
"""

import pandas as pd
import numpy as np
import time
from datetime import datetime
from WindPy import *

w.start()
df0=pd.read_csv('C:/Users/John/Desktop/result/industry2.csv')
df0['time_report']=pd.to_datetime(df0['time_report'],format='%Y-%m-%d')

startTime=df0.iloc[-1,0]
oneday=timedelta(days=1)
startTime=startTime+oneday
startTime=datetime.strftime(startTime,"%Y-%m-%d")
#endTime=time.strftime("%Y-%m-%d",time.localtime())
endTime=datetime.now().strftime('%Y-%m-%d')
endTime=datetime.strptime(endTime,'%Y-%m-%d');
oneday=timedelta(days=1)
endTime=endTime-oneday
endTime=datetime.strftime(endTime,"%Y-%m-%d")

name=['能源指数','材料指数','工业指数','可选消费指数','日常消费指数','医疗保健指数','金融指数','信息技术指数','电信服务指数','公用事业指数','房地产指数']
code=['882001.WI','882002.WI','882003.WI','882004.WI','882005.WI','882006.WI','882007.WI','882008.WI','882009.WI','882010.WI','882011.WI']
for i in range(11):
    wsd1=w.wsd(code[i], "pct_chg", startTime, endTime, "Period=M")
    dates1=pd.to_datetime(wsd1.Times)
    df1=pd.DataFrame(wsd1.Data).T
    df1['time_report']=dates1
    df1.rename(columns={0:'ret'},inplace=True)
    df1['SEC_NAME']=name[i]
    df1['Codes']=code[i]
    
    wsd2=w.edb("M0041339,M0041340", "2017-08-10", endTime, "Fill=Previous")
    df2=pd.DataFrame(wsd2.Data).T
    df2.rename(columns={0:'yj_index',1:'yz_index'},inplace=True)
    df2['time_report']=df1['time_report']
    
    df3=pd.merge(df1,df2,on='time_report',how="left")
    
    df3=df3[['time_report','SEC_NAME','ret','Codes','yj_index','yz_index']]
    df3=df3.dropna()
    df0=df0.append(df3)

df0=df0.sort_values(by=['Codes','time_report'])
#df0=df0.dropna()
df0=df0[['time_report','SEC_NAME','ret','Codes','yj_index','yz_index']]
df0.to_csv('C:/Users/John/Desktop/result/industry3.csv',index=False)