# -*- coding: utf-8 -*-
"""
Created on Sun Dec 17 17:16:18 2017

@author: 何友鑫
"""

import pandas as pd
from statsmodels.tsa import stattools
from statsmodels.graphics.tsaplots import *

import matplotlib.pyplot as plt
from arch.unitroot import ADF

from statsmodels.tsa import arima_model

HS300_data=pd.read_csv("./data/HS300.csv")
HS300_data.index=pd.to_datetime(HS300_data['date'])
SH_ret=HS300_data['ret_cur']
SH_close=HS300_data['close']
type(SH_ret)
SH_ret.head()

##自相关系数
acfs=stattools.acf(SH_ret)

##偏自相关系数
pacfs=stattools.pacf(SH_ret)

plot_acf(SH_ret,use_vlines=True,lags=30)

SH_ret.plot()
plt.title('return')

SH_close.plot()
plt.title('close price')


adfSH_ret=ADF(SH_ret)
print(adfSH_ret)

adfSH_close=ADF(SH_close)
print(adfSH_close)

 LjungBox_ret=stattools.q_stat(acfs,len(SH_ret))
 LjungBox_ret[1][-1]

HS300_data['close']['2010-01-01':'2016-12-31']
HS300_data['2010-01-01':'2016-12-31']

model1=arima_model.ARIMA(SH_ret,order=(2,0,1)).fit()
model1.summary()

stattools.arma_order_select_ic(SH_ret,max_ma=4)