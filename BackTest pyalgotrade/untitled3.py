# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 20:51:02 2017

@author: 何友鑫
"""

from pyalgotrade import strategy
from pyalgotrade.barfeed import yahoofeed
from pyalgotrade.technical import ma

from pyalgotrade import plotter
from pyalgotrade.cn import pandasfeed
from pyalgotrade.stratanalyzer import returns
import sma_crossover
from utils import dataFramefeed
from utils import dataFrameBarfeed
import tushare as ts
import pandas as pd


class MyStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument, smaPeriod):
        super(MyStrategy, self).__init__(feed, 100000)
        self.__position = None
        self.__instrument = instrument
        # We'll use adjusted close values instead of regular close values.
        self.setUseAdjustedValues(True)
        self.__sma = ma.SMA(feed[instrument].getPriceDataSeries(), smaPeriod)

    def onEnterOk(self, position):
        execInfo = position.getEntryOrder().getExecutionInfo()
        self.info("BUY at $%.2f" % (execInfo.getPrice()))

    def onEnterCanceled(self, position):
        self.__position = None

    def onExitOk(self, position):
        execInfo = position.getExitOrder().getExecutionInfo()
        self.info("SELL at $%.2f" % (execInfo.getPrice()))
        self.__position = None

    def onExitCanceled(self, position):
        # If the exit was canceled, re-submit it.
        self.__position.exitMarket()

    def onBars(self, bars):
        # Wait for enough bars to be available to calculate a SMA.
        if self.__sma[-1] is None:
            return

        bar = bars[self.__instrument]
        # If a position was not opened, check if we should enter a long position.
        if self.__position is None:
            if bar.getPrice() > self.__sma[-1]:
                # Enter a buy market order for 10 shares. The order is good till canceled.
                self.__position = self.enterLong(self.__instrument, 10, True)
        # Check if we have to exit the position.
        elif bar.getPrice() < self.__sma[-1] and not self.__position.exitActive():
            self.__position.exitMarket()

'''
def run_strategy(smaPeriod):
    # Load the yahoo feed from the CSV file
    #feed = yahoofeed.Feed()
    #feed.addBarsFromCSV("orcl", "orcl-2000.csv")
    
    #dat = pd.read_csv('orcl-2000.csv',index_col=0,encoding='gbk')
    #print dat
       
    dat=ts.get_hist_data('002768',start='2017-01-01',end='2017-12-27')
    dat['Adj Close']=dat['close']
    #dat.ix[:,5:6]
    feed = dataFramefeed.Feed()
    feed.addBarsFromDataFrame("国恩股份", dat.ix[:,(0,1,2,3,4,14)])
    # Evaluate the strategy with the feed.
    myStrategy = MyStrategy(feed, "国恩股份", smaPeriod)
    myStrategy.run()
    print "Final portfolio value: $%.2f" % myStrategy.getBroker().getEquity()

run_strategy(15)
'''


