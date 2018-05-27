from pyalgotrade import strategy
from pyalgotrade import plotter
from pyalgotrade.tools import yahoofinance
from pyalgotrade.technical import ma
from pyalgotrade.technical import macd
from pyalgotrade.technical import cumret
from pyalgotrade.stratanalyzer import sharpe
from pyalgotrade.stratanalyzer import returns
import tushare as ts
import pandas as pd
from utils import dataFramefeed
class MarketTiming(strategy.BacktestingStrategy):
    def __init__(self, feed, instrumentsByClass, initialCash):
        #所有的策略类都是继承strategy模块下的BacktestingStrategy类
        #BacktestingStrategy继承BaseStrategy类
        strategy.BacktestingStrategy.__init__(self, feed, initialCash)
        self.setUseAdjustedValues(True)
        #获得所有标的 类型为list  
        self.__instrumentsByClass = instrumentsByClass
        self.__rebalanceMonth = None
        self.__sharesToBuy = {}
        self.__position = {}
        # Initialize indicators for each instrument.
        # 定义sma的一个字典   标的：sma
        self.__sma = {}
        self.__dea = {}
        self.__priceDS={}
        self.__takeprofit={}
        self.__stoploss={}
        self.__order={}
        self.__cost={}
        #self.__oderID=1
        takeprofit=0.1
        stoploss=0.1
        for assetClass in instrumentsByClass:
            for instrument in instrumentsByClass[assetClass]:
                priceDS = feed[instrument].getPriceDataSeries()
                
                self.__priceDS[instrument] = feed[instrument].getPriceDataSeries()
                self.__sma[instrument] = ma.SMA(self.__priceDS[instrument], 26)
                #self.__sma[instrument] = ma.SMA(priceDS, 26)
               
                #获得DEA指标
                #得到一个MACD类的临时实例
                __macd = macd.MACD(self.__priceDS[instrument],12,26,9)
                #__macd = macd.MACD(priceDS,12,26,9)
                self.__dea[instrument]=__macd.getSignal()
                #self.__cost[instrument]=None
                self.__takeprofit[instrument]=takeprofit#设置止盈点
                self.__stoploss[instrument]=stoploss#设置止损点
                self.__cost[instrument]=0
                
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
    def _shouldRebalance(self, dateTime):
        return dateTime.month != self.__rebalanceMonth

  
    #设置下单
    def _placePendingOrders(self):
        #可用资金设置为总资金的90%以防价格变化太快
        remainingCash = self.getBroker().getCash() * 0.9  # Use less chash just in case price changes too much.

        for instrument in self.__sharesToBuy:
            orderSize = self.__sharesToBuy[instrument]
            if orderSize > 0:
                # Adjust the order size based on available cash.
                lastPrice = self.getLastPrice(instrument)
                cost = orderSize * lastPrice
                while cost > remainingCash and orderSize > 0:
                    orderSize -= 1
                    cost = orderSize * lastPrice
                if orderSize > 0:
                    remainingCash -= cost
                    assert(remainingCash >= 0)

            if orderSize != 0:
                self.info("Placing market order for %d %s shares" % (orderSize, instrument))
                self.marketOrder(instrument, orderSize, goodTillCanceled=True)
                self.__cost[instrument]=self.getLastPrice(instrument)
                #记录每个订单号、代码、价格、手数
                #self.__order[str(orderID)]=[instrument,orderSize,]
                self.__sharesToBuy[instrument] -= orderSize

    #打印日志
    def _logPosSize(self):
     
        totalEquity = self.getBroker().getEquity()
        positions = self.getBroker().getPositions()
        for instrument in self.getBroker().getPositions():
            posSize = positions[instrument] * self.getLastPrice(instrument) / totalEquity * 100
            self.info("%s - %0.2f %%" % (instrument, posSize))

    #调仓
    def _rebalance(self):
        #获得最近收盘价
        #self.info(self.getLastPrice('002493'))
        #获得最近DEA
        #self.info(self.__dea['002493'][-1])
        #self.info("Rebalancing")
        '''
        try:
            self.info(self.__dea['002493'][-2])
        except:
            pass
        '''
        # Cancel all active/pending orders.
        for order in self.getBroker().getActiveOrders():
            self.getBroker().cancelOrder(order)

        ##给每个标的等权益权重分配资金
        cashPerAssetClass = self.getBroker().getEquity() / float(len(self.__instrumentsByClass))
        #cashPerAssetClass = self.getBroker().getCash() / float(len(self.__instrumentsByClass))
        
        self.__sharesToBuy = {}
        
        instruments_buy=self.findByDEA()
        ##计算开仓
        for instrument in instruments_buy :
            #self.info("Best for  %s" % ( instrument))
            if instrument is not None  :
                #not in self.getBroker().getPositions()
                #self.info("Best for  %s" % ( instrument))
                lastPrice = self.getLastPrice(instrument)
                ##每个标的应有的资金
           
                if instrument in self.getBroker().getPositions():
                    cashForInstrument = cashPerAssetClass/2 
                    #cashForInstrument =  self.getBroker().getShares(instrument) * lastPrice - cashPerAssetClass
                else:
                    cashForInstrument = cashPerAssetClass 
                #- self.getBroker().getShares(instrument) * lastPrice
                # This may yield a negative value and we have to reduce this
                # position.
                if cashForInstrument>0:
                    self.__sharesToBuy[instrument] = int(cashForInstrument / lastPrice)
        
        ##计算需要卖出的仓位
        for instrument in self.getBroker().getPositions() :
            if instrument not in self.__sharesToBuy:
                #self.info('instrument:%s price:%s  cost:%s'% (instrument,self.getLastPrice(instrument),self.__cost[instrument]))
                rate=(self.getLastPrice(instrument)-self.__cost[instrument])/self.__cost[instrument]
                if rate<= -self.__stoploss[instrument] or rate>=self.__takeprofit[instrument]:
                    currentShares = self.getBroker().getShares(instrument)
                    #assert(instrument not in self.__sharesToBuy)
                    self.__sharesToBuy[instrument] = currentShares * -1
        

    def getSMA(self, instrument):
        return self.__sma[instrument]

    #通过DEA指标找买点
    def findByDEA(self):
        instruments_buy=[]
        lookBack=30
        for instrument in self.__instrumentsByClass:
            priceDS=self.__priceDS[instrument]
            #priceDS = self.getFeed()['002493'].getPriceDataSeries()
            
            #if len(priceDS) >= lookBack and self.__dea['002493'][-1] > 0 and self.__dea['002493'][-1*lookBack] is not None:
        
            if len(self.__priceDS[instrument]) >= lookBack and self.__dea[instrument][-1] > 0 and self.__dea[instrument][-1*lookBack] is not None:
           
                #if self.__dea['002493'][-1]>0:
                for i in range(2,31):
                    if(priceDS[-1*i]==min(priceDS[-1*i:-1])):
                        for j in range(i+1,31):
                            if(priceDS[-1*j]==max(priceDS[(-1*j):(-i)]) and self.__dea[instrument][-1*j]>0 and priceDS[-1*i]==min(priceDS[-1*j:-1])):
                                #self.info('buy!!!')
                                instruments_buy.append(instrument)           
                                #if self.__position is None:
                                '''
                                try:
                                    shares = self.getBroker().getShares(instrument)
                                    if shares==0:
                                        cashForInstrument = self.getBroker().getCash() * 0.1
                                        lastPrice = self.getLastPrice(instrument)
                                        orderSize = int(cashForInstrument / lastPrice)
                                        ##两种下单方式的不同？
                                        #self.marketOrder(instrument, orderSize)
                                        self.__position[instrument] = self.enterLong(instrument, orderSize, True)
                                        self.__cost[instrument]=lastPrice
                                except:
                                    pass
                                '''    

        return list(set(instruments_buy))

    
    def onBars(self, bars):
        '''
        for assetClass in self.__instrumentsByClass:
            for instrument in self.__instrumentsByClass[assetClass]:
                if self.__dea[instrument][-1] is None:
                    return
        '''
        self._rebalance()

        self._placePendingOrders()
        #self.findByDEA()
 
       
        '''
        #测试价格正确性
        for assetClass in self.__instrumentsByClass:
            for instrument in self.__instrumentsByClass[assetClass]:
                bar = bars[instrument]
                self.info('%s: open：%s high:%s low:%s close:%s AdjClose:%s '%(instrument,bar.getOpen(),bar.getHigh(),bar.getLow(),bar.getClose(),bar.getAdjClose()))
        
        '''
        '''
        try:
            self.info(priceDS[-3:-1])
            self.info(priceDS[-1])
            self.info(min(priceDS[-3:-1]))
        except:
            pass
        '''

        '''
        #取当前行情
        #self.info(bars['002493'].getPrice())
        #print bars['002493'].getPrice()
        currentDateTime = bars.getDateTime()
     
        #当前月份是否要重新调整 默认为是  这段代码是说每月调一次仓
        if self._shouldRebalance(currentDateTime):
            #__rebalanceMonth从none 置为当前月份   
            self.__rebalanceMonth = currentDateTime.month
            self._rebalance()

        self._placePendingOrders()
        '''

def main(plot,sz50,HQ,HQ_hs300):
    initialCash = 10000000
    sz50_code=sz50['code']
    feed = dataFramefeed.Feed()
    feed.addBarsFromDataFrame("hs300", HQ_hs300)
    instrumentsByClass={}
    
    for i in range(0,len(sz50_code)):
        l=[]
        l.append(sz50_code[i])
        instrumentsByClass[sz50_code[i]]=l
        feed.addBarsFromDataFrame(sz50_code[i], HQ[sz50_code[i]])
    HQ['600000']
    '''    
    instrumentsByClass = {
        "002768": ["002768"],
        "002493": ["002493"]
    }
    # 这里instruments暂时没用 instrumentsByClass是portfolio  
    instruments = ['hs300']
    for assetClass in instrumentsByClass:
        instruments.extend(instrumentsByClass[assetClass])
   
    ##feed 是dataFramefeed模块Feed类的一个实例，Feed继承DataFrameBarfeed.BarFeed，BarFeed继承membf.BarFeed
    feed = dataFramefeed.Feed()
    dat=ts.get_hist_data("hs300",start='2017-01-01',end='2017-12-27')
    dat['Adj Close']=dat['close']
    feed.addBarsFromDataFrame("hs300", dat.ix[:,(0,1,2,3,4,13)])
  

    
    dat=ts.get_hist_data("002768",start='2017-01-01',end='2017-12-27')
    dat['Adj Close']=dat['close']  
    feed.addBarsFromDataFrame("002768", dat.ix[:,(0,1,2,3,4,14)])

    dat=ts.get_hist_data('002493',start='2017-01-01',end='2017-12-27')
    dat['Adj Close']=dat['close']
    feed.addBarsFromDataFrame("002493", dat.ix[:,(0,1,2,3,4,14)])
    '''
    
    
    strat = MarketTiming(feed, instrumentsByClass, initialCash)
    sharpeRatioAnalyzer = sharpe.SharpeRatio()
    strat.attachAnalyzer(sharpeRatioAnalyzer)
    returnsAnalyzer = returns.Returns()
    strat.attachAnalyzer(returnsAnalyzer)

    if plot:
        plt = plotter.StrategyPlotter(strat, False, False, True)
        plt.getOrCreateSubplot("cash").addCallback("Cash", lambda x: strat.getBroker().getCash())
        #plt.getOrCreateSubplot("cash").addCallback("Cash", strat.getBroker().getCash())
        # Plot strategy vs. benchmark HS300 cumulative returns.
        plt.getOrCreateSubplot("returns").addDataSeries("hs300", cumret.CumulativeReturn(feed["hs300"].getPriceDataSeries()))
        plt.getOrCreateSubplot("returns").addDataSeries("Strategy", returnsAnalyzer.getCumulativeReturns())

    strat.run()
    print "Sharpe ratio: %.2f" % sharpeRatioAnalyzer.getSharpeRatio(0.05)
    print "Returns: %.2f %%" % (returnsAnalyzer.getCumulativeReturns()[-1] * 100)

    if plot:
        plt.plot()


if __name__ == "__main__":
       
    HQ={}
    
    sz50=ts.get_sz50s()
    sz50_code=sz50['code']
    '''
    sz50.to_csv('sz50.csv',encoding='utf8',index_label =False)
    sz50_2=pd.read_csv("sz50.csv")
    '''
    dat=ts.get_hist_data("hs300",start='2017-01-01',end='2017-12-31')
    dat['Adj Close']=dat['close']
    HQ_hs300=dat.ix[:,(0,1,2,3,4,13)]
    '''
    HQ_hs300.to_csv('HQ_hs300.csv',encoding='utf8',index_label =False)
    HQ_hs300_2=pd.read_csv("HQ_hs300.csv")
    '''

    for i in range(0,len(sz50_code)):
        dat=ts.get_hist_data(sz50_code[i],start='2017-01-01',end='2017-12-31')
        dat['Adj Close']=dat['close']
        HQ[sz50_code[i]]=dat.ix[:,(0,1,2,3,4,14)]
        
    #sz50=pd.read_csv("sz50.csv")
    #HQ=pd.read_csv("HQ_hs300.csv")
    #HQ=pd.read_csv()
    main(True,sz50,HQ,HQ_hs300)





'''
break_flag=False
for i in range(10):
    print("爷爷层")
    for j in range(10):
        print("爸爸层")
        for k in range(10):
            print("孙子层")
            if k==3:
                break_flag=True
                break                    #跳出孙子层循环，继续向下运行
        if break_flag==True:
            break                        #满足条件，运行break跳出爸爸层循环，向下运行
    if break_flag==True:
        break                            #满足条件，运行break跳出爷爷层循环，结束全部循环，向下运行
print("keep going...")


'''



