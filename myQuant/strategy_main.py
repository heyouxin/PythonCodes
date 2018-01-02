# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 17:33:05 2017

@author: 何友鑫
"""
from WindPy import *
import tushare as ts
import numpy as np
from Mystrategy import MyStrategy
import pandas as pd
from pandas import DataFrame
if __name__ == "__main__":
    #取盈运能力、成长能力的数据
    profit_data=ts.get_profit_data(2017,3) 
    growth_data=ts.get_growth_data(2017,3)
    profit_data.to_excel("profit_data_2017_3.xlsx")
    growth_data.to_excel("growth_data_2017_3.xlsx")
    pd.to_excel(profit_data,)
    s=MyStrategy(profit_data,growth_data)
    stock=s.getData()
    print(stock)
    
    
    w.start()
    MACD_data=w.wsd("000001.SZ,000002.SZ,000004.SZ,000006.SZ,000005.SZ,000007.SZ", "MACD", "2017-10-27", "2017-11-25", "MACD_L=26;MACD_S=12;MACD_N=9;MACD_IO=3")
    MACD_data.Times
    #pd.Series(MACD_data.Times),
    MACD_df=DataFrame(pd.Series(MACD_data.Data))
    
    


'''


df=ts.get_hist_data(code='sh',start='2017-10-01',end='2017-11-23',ktype='D')
ema_26=df.ix[0:25,'close'].mean()
ema_12=df.ix[0:11,'close'].mean()
DIF=ema_12-ema_26
ema_9=df.ix[0:8,'close'].mean()
MACD=(ema_12-ema_26-ema_9)*2


def get_EMA(df,N):  
    for i in range(len(df)):  
        if i==0:  
            df.ix[i,'ema']=df.ix[i,'close']  
        if i>0:  
            df.ix[i,'ema']=(2*df.ix[i,'close']+(N-1)*df.ix[i-1,'ema'])/(N+1)  
    ema=list(df['ema'])  
    return ema  
def get_MACD(df,short=12,long=26,M=9):  
    a=get_EMA(df,short)  
    b=get_EMA(df,long)  
    df['diff']=pd.Series(a)-pd.Series(b)  
    #print(df['diff'])  
    for i in range(len(df)):  
        if i==0:  
            df.ix[i,'dea']=df.ix[i,'diff']  
        if i>0:  
            df.ix[i,'dea']=(2*df.ix[i,'diff']+(M-1)*df.ix[i-1,'dea'])/(M+1)  
    df['macd']=2*(df['diff']-df['dea'])  
    return df  
get_MACD(df,12,26,9)  
df  


today_all=ts.get_today_all()
today_all[today_all.code=='000002']

profit_data=ts.get_profit_data(2017,3) 

profit_data.dropna()                                                                                                                             
'''