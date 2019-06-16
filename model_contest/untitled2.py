# -*- coding: utf-8 -*-
"""
Created on Tue Aug 28 17:35:53 2018

@author: 何友鑫
"""


from urllib import request
from bs4 import BeautifulSoup as bs
from lxml import etree
import pandas as pd
from pandas import DataFrame
import numpy as np

data=pd.read_excel('data_final.xlsx')

def webScraping(data,part):
    #for i in range(0,len(data['用户号'])):
    data=data_all
    for i in range(0,20):
        try:
            #resp = request.urlopen('https://www.federalreserve.gov/releases/H41/20171102/h41.htm')
            #url=data.loc[i,'访问页面']
            url='http://www.lawtime.cn/ask/exp/11901.html'
            #url='http://www.lawtime.cn/info/hunyin/jiehun/hunjia/201312182875578.html'
            resp = request.urlopen(url)
            html_data = resp.read().decode('utf-8','ignore')
        except:
            pass
        else:
            #soup = bs(html_data, 'html.parser')  
            selector = etree.HTML(html_data) 

            try:
                #法律咨询              
                path='/html/body/div[4]/div/div[1]/div[1]/p[2]/span[3]//text()'    
                data.loc[i,'网页时间'] = selector.xpath(path) 
   
            except:
             
                try:
                    #知识类
                    str1='/html/body/div[5]/div[1]/div[1]/div/p/span[3]//text()'
                    data.loc[i,'网页时间'] = selector.xpath(str1).strip()
                except:
                    try:
                        #法律法规
                        str1='/html/body/div[3]/div/div[1]/div/div[1]/p[2]/span[2]//text()'
                        data.loc[i,'网页时间'] = selector.xpath(str1).strip()
                    except:
                        try:
                            #访谈
                            str1='/html/body/div[3]/div[1]/div[1]/div/text()[4]'
                            data.loc[i,'网页时间'] = selector.xpath(str1).strip() 
                        except:
                            try:
                                #法律经验
                                str1='/html/body/div[4]/div[3]/div[1]/div[1]/div[1]/div[1]//text()[2]'
                                data.loc[i,'网页时间'] = selector.xpath(str1).strip() 
                            except:
                                pass
                        
                        
    str1='data_'
    #str1='C:/Users/heyouxin/Documents/PythonCodes/Web scraping/data/data_'
    str2='.xlsx'
    filename=str1+part+str2 
    data.to_excel(filename,index=False,encoding='utf8')