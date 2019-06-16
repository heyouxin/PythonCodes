# -*- coding: utf-8 -*-
"""
Created on Wed Sep 19 13:35:52 2018

@author: John
"""

import pandas as pd
import numpy as np
import time
from datetime import datetime
from datetime import timedelta
from WindPy import *

w.start()
df0=pd.read_csv('C:/Users/John/Desktop/result/industry.csv')
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
    wsd1=w.wsd(code[i], "close,pct_chg", startTime, endTime, "")
    dates1=pd.to_datetime(wsd1.Times)
    df1=pd.DataFrame(wsd1.Data).T
    df1['time_report']=dates1
    df1['time_report'] = pd.to_datetime(df1['time_report'],format='%Y-%m-%d')#将读取的日期转为datatime格式
    df1.rename(columns={0:'CLOSE',1:'ret'},inplace=True)
    #df1['ret']=df1['CLOSE'].pct_change() #求增长率
    #df1['ret']=df1['ret']*100
    df1['SEC_NAME']=name[i]
    df1['Codes']=code[i]
    
    wsd2=w.edb("S0059741", "2018-09-10", endTime,"Fill=Previous")
    df1['rf']=pd.DataFrame(wsd2.Data).T
    df1['rf'] = df1['rf'].map(lambda x: ((1+x/100)**(1/250)-1)*100)
    wsd1=w.wsd("000300.SH", "pct_chg", "2018-09-10", endTime, "")
    df1['hs300']=pd.DataFrame(wsd1.Data).T
    df1['Ri_Rf']=df1['ret']-df1['rf']
    df1['Rm_Rf']=df1['hs300']-df1['rf']
    df1=df1.drop(['hs300'],axis=1)
    df1=df1[['time_report','CLOSE','ret','Codes','SEC_NAME','rf','Ri_Rf','Rm_Rf']]
    df0=df0.append(df1)

df0=df0.sort_values(by=['Codes','time_report'])
#df0=df0.dropna()
df0=df0[['time_report','CLOSE','ret','Codes','SEC_NAME','rf','Ri_Rf','Rm_Rf']]
df0.to_csv('C:/Users/John/Desktop/result/industry1.csv',index=False)