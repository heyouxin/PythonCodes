from pyalgotrade import strategy
from pyalgotrade import plotter
from pyalgotrade.tools import yahoofinance
from pyalgotrade.technical import ma
from pyalgotrade.technical import macd
from pyalgotrade.technical import cumret
from pyalgotrade.stratanalyzer import sharpe
from pyalgotrade.stratanalyzer import returns
import tushare as ts
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
        self.__position = None
        # Initialize indicators for each instrument.
        # 定义sma的一个字典   标的：sma
        self.__sma = {}
        self.__dea = {}
        self.__priceDS={}
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

    def _getRank(self, instrument):
        # If the price is below the SMA, then this instrument doesn't rank at
        # all.
        smas = self.__sma[instrument]
        price = self.getLastPrice(instrument)
        if len(smas) == 0 or smas[-1] is None or price < smas[-1]:
            return None

        # Rank based on 20 day returns.
        ret = None
        lookBack = 20
        priceDS = self.getFeed()[instrument].getPriceDataSeries()
        if len(priceDS) >= lookBack and smas[-1] is not None and smas[-1*lookBack] is not None:
            ret = (priceDS[-1] - priceDS[-1*lookBack]) / float(priceDS[-1*lookBack])
        return ret

    def _getTopByClass(self, assetClass):
        # Find the instrument with the highest rank.
        ret = None
        highestRank = None
        for instrument in self.__instrumentsByClass[assetClass]:
            rank = self._getRank(instrument)
            if rank is not None and (highestRank is None or rank > highestRank):
                highestRank = rank
                ret = instrument
        return ret

    #get the Ret of the highest instrument
    def _getTop(self):
        ret = {}
        for assetClass in self.__instrumentsByClass:
            ret[assetClass] = self._getTopByClass(assetClass)
        return ret

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
        self.info("Rebalancing")
        '''
        try:
            self.info(self.__dea['002493'][-2])
        except:
            pass
        '''
        # Cancel all active/pending orders.
        for order in self.getBroker().getActiveOrders():
            self.getBroker().cancelOrder(order)

        cashPerAssetClass = self.getBroker().getEquity() / float(len(self.__instrumentsByClass))
        self.__sharesToBuy = {}

        # Calculate which positions should be open during the next period.
        topByClass = self._getTop()
        for assetClass in topByClass:
            instrument = topByClass[assetClass]
            self.info("Best for class %s: %s" % (assetClass, instrument))
            if instrument is not None:
                lastPrice = self.getLastPrice(instrument)
                cashForInstrument = cashPerAssetClass - self.getBroker().getShares(instrument) * lastPrice
                # This may yield a negative value and we have to reduce this
                # position.
                self.__sharesToBuy[instrument] = int(cashForInstrument / lastPrice)

        # Calculate which positions should be closed.
        for instrument in self.getBroker().getPositions():
            if instrument not in topByClass.values():
                currentShares = self.getBroker().getShares(instrument)
                assert(instrument not in self.__sharesToBuy)
                self.__sharesToBuy[instrument] = currentShares * -1

    def getSMA(self, instrument):
        return self.__sma[instrument]

    #找买点
    def findByDEA(self):
        lookBack=30
        priceDS=self.__priceDS['002493']
        #priceDS = self.getFeed()['002493'].getPriceDataSeries()
        
        #if len(priceDS) >= lookBack and self.__dea['002493'][-1] > 0 and self.__dea['002493'][-1*lookBack] is not None:
    
        if len(self.__priceDS['002493']) >= lookBack and self.__dea['002493'][-1] > 0 and self.__dea['002493'][-1*lookBack] is not None:
       
            #if self.__dea['002493'][-1]>0:
            for i in range(2,31):
                if(priceDS[-1*i]==min(priceDS[-1*i:-1])):
                    for j in range(i+1,31):
                        if(priceDS[-1*j]==max(priceDS[(-1*j):(-i)]) and self.__dea['002493'][-1*j]>0 and priceDS[-1*i]==min(priceDS[-1*j:-1])):
                            self.info('buy!!!')
                            if self.__position is None:
                                self.__position = self.enterLong('002493', 10, True)
                            # Check if we have to exit the position.
                            '''
                            elif bar.getPrice() < self.__sma[-1] and not self.__position.exitActive():
                                self.__position.exitMarket()
                            '''
                            return
                    #if self.__dea['002493'][-1*i]<0:

    
    def onBars(self, bars):
        for assetClass in instrumentsByClass:
            for instrument in instrumentsByClass[assetClass]:
                if self.__dea[instrument][-1] is None:
                    return
        self.findByDEA()
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

def main(plot):
    initialCash = 10000
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
    
    
    
    strat = MarketTiming(feed, instrumentsByClass, initialCash)
    sharpeRatioAnalyzer = sharpe.SharpeRatio()
    strat.attachAnalyzer(sharpeRatioAnalyzer)
    returnsAnalyzer = returns.Returns()
    strat.attachAnalyzer(returnsAnalyzer)

    if plot:
        plt = plotter.StrategyPlotter(strat, False, False, True)
        plt.getOrCreateSubplot("cash").addCallback("Cash", lambda x: strat.getBroker().getCash())
        # Plot strategy vs. benchmark HS300 cumulative returns.
        plt.getOrCreateSubplot("returns").addDataSeries("hs300", cumret.CumulativeReturn(feed["hs300"].getPriceDataSeries()))
        plt.getOrCreateSubplot("returns").addDataSeries("Strategy", returnsAnalyzer.getCumulativeReturns())

    strat.run()
    print "Sharpe ratio: %.2f" % sharpeRatioAnalyzer.getSharpeRatio(0.05)
    print "Returns: %.2f %%" % (returnsAnalyzer.getCumulativeReturns()[-1] * 100)

    if plot:
        plt.plot()


if __name__ == "__main__":
    main(True)
