# -*- coding: utf-8 -*-
"""
Created on Sat Nov 25 11:19:37 2017

@author: 何友鑫
"""
import numpy as np
import pandas as pd
from pandas import DataFrame
class MyStrategy:
    universe=[]
    profit_data=DataFrame()
    growth_data=DataFrame()
    
    #构造函数
    def __init__(self,profit_data,growth_data):
        self.profit_data=profit_data 
        self.growth_data=growth_data
    
    
    
    def basicFinance(self):     
        #1.找出ROE前5%的股票
        roe_95=np.percentile(self.profit_data['roe'].dropna(),95)
        stock_roe=self.profit_data[self.profit_data.roe>=roe_95]['name']
        #stock_roe
 
        #2.找出净利润增长前5%的股票
  
        growth_95=np.percentile(self.growth_data['nprg'].dropna(),95)
        stock_growth=self.growth_data[self.growth_data.nprg>=growth_95]['name']
        #stock_growth
        
        #3.PB要低于50%
        
        
        #
        stock=list(set(stock_roe).intersection(set(stock_growth)))     
        self.universe=stock
    
    def MACD(self):
        pass
        
        
    def getData(self):
        self.basicFinance()
        self.MACD()
        return self.universe
        
    