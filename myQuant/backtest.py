# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 11:22:23 2017

@author: 何友鑫
"""
  
import pytz  
from datetime import datetime  
  
import zipline  
from zipline.algorithm import TradingAlgorithm  
from zipline.finance.trading import TradingEnvironment  
from zipline.api import order, record, symbol, history  
from zipline.finance import trading  
from zipline.utils.factory import create_simulation_parameters  
from zipline.assets.synthetic import make_simple_equity_info  
from zipline.utils.calendars import exchange_calendar_sh  
from zipline.utils.calendars import exchange_calendar_lse  
from zipline.utils.calendars import exchange_calendar_nyse  
import pandas as pd  
import numpy as np  
import matplotlib.pyplot as plt 
import zipline

from zipline.api import order_target, record, symbol

n = 0  
# Define algorithm  
def initialize(context):  
    context.asset = symbol('AAPL')  
    print ("initialization")  
    pass  
  
def handle_data(context, data):  
    global n  
    print ("handle", n)  
    print (data.history(context.asset, 'price', 1, '1d'))#close price  
    # print history(1, '1d', 'price').mean()  
    n += 1  
    order(symbol('AAPL'), 10)  
    record(AAPL=data.current(symbol('AAPL'), 'price'))  
  
def analyze(context=None, results=None):  

    # Plot the portfolio and asset data.  
    ax1 = plt.subplot(211)  
    results.portfolio_value.plot(ax=ax1)  
    ax1.set_ylabel('Portfolio value (USD)')  
    ax2 = plt.subplot(212, sharex=ax1)  
    results.AAPL.plot(ax=ax2)  
    ax2.set_ylabel('AAPL price (USD)')  
  
    # Show the plot.  
    plt.gcf().set_size_inches(18, 8)  
    plt.show()  

def load_t(trading_day, trading_days, bm_symbol):  
    # dates = pd.date_range('2001-01-01 00:00:00', periods=365, tz="Asia/Shanghai")  
    bm = pd.Series(data=np.random.random_sample(len(trading_days)), index=trading_days)  
    tr = pd.DataFrame(data=np.random.random_sample((len(trading_days), 7)), index=trading_days,  
                      columns=['1month', '3month', '6month', '1year', '2year', '3year', '10year'])  
    return (bm, tr)  

trading.environment = TradingEnvironment(load=load_t, bm_symbol='^HSI', exchange_tz='Asia/Shanghai')  
  
# 回测参数设置  
sim_params = create_simulation_parameters(year=2014,  
    start=pd.to_datetime("2001-01-01 00:00:00").tz_localize("Asia/Shanghai"),  
    end=pd.to_datetime("2001-09-21 00:00:00").tz_localize("Asia/Shanghai"),  
    data_frequency="daily", emission_rate="daily")  # 原始版本是上面这样的，代码里面是交易日历，然而，如何产生交易日历呢？  
  
  
# setting the algo parameters  
algor_obj = TradingAlgorithm(initialize=initialize, handle_data=handle_data,  
                             sim_params=sim_params, env=trading.environment, analyze=analyze  
                             )  
parse = lambda x: datetime.date(datetime.strptime(x, '%Y/%m/%d'))  
  
# data generator  
data_s = pd.read_csv('AAPL.csv', parse_dates=['Date'], index_col=0, date_parser=parse)  
print (data_s)  
data_c = pd.Panel({'AAPL': data_s})  
  
perf_manual = algor_obj.run(data_c)  
# Print  
perf_manual.to_csv('myoutput.csv') 





'''
cal = exchange_calendar_sh.SHExchangeCalendar()  


trading.environment = TradingEnvironment(load=load_t, bm_symbol='^HSI', exchange_tz='Asia/Shanghai')  

# 回测参数设置  
sim_params = create_simulation_parameters(year=2014,  
    start=pd.to_datetime("2001-01-01 00:00:00").tz_localize("Asia/Shanghai"),  
    end=pd.to_datetime("2001-09-21 00:00:00").tz_localize("Asia/Shanghai"),  
    data_frequency="daily", emission_rate="daily")  # 原始版本是上面这样的，代码里面是交易日历，然而，如何产生交易日历呢？  

  
# setting the algo parameters  
algor_obj = TradingAlgorithm(initialize=initialize, handle_data=handle_data,  
                             sim_params=sim_params, env=trading.environment, analyze=analyze  
                             )  
# data format definition  
parse = lambda x: datetime.date(datetime.strptime(x, '%Y/%m/%d'))  
  
# data generator  
data_s = pd.read_csv('AAPL.csv', parse_dates=['Date'], index_col=0, date_parser=parse)  
print data_s  
data_c = pd.Panel({'AAPL': data_s})  
  
perf_manual = algor_obj.run(data_c)  
# Print  
perf_manual.to_csv('myoutput.csv')  
 ''' 
