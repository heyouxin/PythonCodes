# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 21:36:38 2017

@author: 何友鑫
"""
from pyalgotrade import plotter
from pyalgotrade.cn import pandasfeed
from pyalgotrade.barfeed import yahoofeed
from pyalgotrade.stratanalyzer import returns
import pyalg_test 
import market_timing


from utils import dataFrameBarfeed

import pandas as pd
from pyalgotrade import broker  


instrument = ["002768", "002493"]
'''
threshold = 0.01
vwapWindowSize = 5
'''

dat=ts.get_hist_data("002768",start='2017-01-01',end='2017-12-27')
dat['Adj Close']=dat['close']
#dat.ix[:,5:6]
feed = dataFramefeed.Feed()
feed.addBarsFromDataFrame("002768", dat.ix[:,(0,1,2,3,4,14)])

#dat.ix[:,(0,1,2,3,4,14)].to_csv('002768.csv')


dat=ts.get_hist_data('002493',start='2017-01-01',end='2017-12-27')
dat['Adj Close']=dat['close']
#dat.ix[:,5:6]

feed.addBarsFromDataFrame("002493", dat.ix[:,(0,1,2,3,4,14)])
#dat.ix[:,(0,1,2,3,4,14)].to_csv('002493.csv')

myStrategy = pyalg_test.MarketTiming(feed, "002768",15)





'''
broker_commission = broker.backtesting.TradePercentage(0.003)  
# 3.2 fill strategy设置  
fill_stra = broker.fillstrategy.DefaultStrategy(volumeLimit=0.1)  
sli_stra = broker.slippage.NoSlippage()  
fill_stra.setSlippageModel(sli_stra)  
# 3.3完善broker类  
brk = broker.backtesting.Broker(1000000, feed, broker_commission)  
brk.setFillStrategy(fill_stra)  
   
'''



# Evaluate the strategy with the feed's bars.
#feed = yahoofeed.Feed()
#feed.addBarsFromCSV("002768", "002768.csv")
#feed.addBarsFromCSV("002493","002493.csv")

#myStrategy = pyalg_test.VWAPMomentum(feed, instrument, vwapWindowSize,threshold)

# Attach a returns analyzers to the strategy.
returnsAnalyzer = returns.Returns()
myStrategy.attachAnalyzer(returnsAnalyzer)

plot=True
if plot:
    plt = plotter.StrategyPlotter(myStrategy, True, True, True)
    # plt.getPortfolioSubplot().addDataSeries("vwap", strat.getVWAP()[instrument[-1]])
ds = pyalg_utils.dataSet(myStrategy)  # 抽取交易数据集语句，若使用系统自带画图功能则不需要该项
myStrategy.run()
print "Sharpe ratio: %.2f" % sharpeRatioAnalyzer.getSharpeRatio(0.05)

if plot:
    plt.plot()

rs = ds.getReturns()  # 获取默认的交易信息，dic格式,可忽略


# Attach the plotter to the strategy.
plt = plotter.StrategyPlotter(myStrategy)
# Include the SMA in the instrument's subplot to get it displayed along with the closing prices.
#plt.getInstrumentSubplot("002768").addDataSeries("SMA", myStrategy.getSMA())
# Plot the simple returns on each bar.
#plt.getOrCreateSubplot("returns").addDataSeries("Simple returns", returnsAnalyzer.getReturns())

# Run the strategy.
myStrategy.run()
myStrategy.info("Final portfolio value: $%.2f" % myStrategy.getResult())

# Plot the strategy.
plt.plot()