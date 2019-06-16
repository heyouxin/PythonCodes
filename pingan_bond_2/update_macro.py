# -*- coding: utf-8 -*-
"""
Created on Wed Sep 19 16:20:14 2018

@author: John
"""
import pandas as pd
import numpy as np
import time
from datetime import datetime
from datetime import timedelta
from WindPy import *

w.start()
df0=pd.read_csv('C:/Users/John/Desktop/result/macro.csv')
df0=pd.DataFrame(df0,columns=['time_report','value','variable'])
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



#央行基准利率
wsd1=w.edb("M0043822", startTime, endTime,"Fill=Previous")
dates1=pd.to_datetime(wsd1.Times)
df1=pd.DataFrame(wsd1.Data).T
df1['time_report']=dates1
df1.rename(columns={0:'value'},inplace=True)
df1['variable']='CPI'
df1=df1[['time_report','value','variable']]

#cpi
wsd2=w.edb("M0000612", startTime, endTime,"Fill=Previous")
dates2=pd.to_datetime(wsd2.Times)
df2=pd.DataFrame(wsd2.Data).T
df2['time_report']=dates2
df2.rename(columns={0:'value'},inplace=True)
df2['variable']='interest_center'
df2=df2[['time_report','value','variable']]

#gdp增长率
wsd3=w.edb("M0039354", startTime, endTime,"Fill=Previous")
dates3=pd.to_datetime(wsd3.Times)
df3=pd.DataFrame(wsd3.Data).T
df3['time_report']=dates3
df3.rename(columns={0:'value'},inplace=True)
df3['variable']='consumptionr'
df3=df3[['time_report','value','variable']]

#居民消费水平
wsd4=w.edb("M0024813", startTime, endTime,"Fill=Previous")
dates4=pd.to_datetime(wsd4.Times)
df4=pd.DataFrame(wsd4.Data).T
df4['time_report']=dates4
df4.rename(columns={0:'value'},inplace=True)
df4['variable']='GDP_growth_rate'
df4=df4[['time_report','value','variable']]

df0=df0.append(df1)
df0=df0.append(df2)
df0=df0.append(df3)
df0=df0.append(df4)

df0=df0.sort_values(by=['variable','time_report'])
df0.to_csv('C:/Users/John/Desktop/result/macro1.csv',index=False)
