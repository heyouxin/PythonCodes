# -*- coding: utf-8 -*-
"""
Created on Mon Aug 27 22:30:27 2018

@author: 何友鑫
"""

from urllib import request
from bs4 import BeautifulSoup as bs
from lxml import etree
import pandas as pd
from pandas import DataFrame


def webScraping(data,part):
    for i in range(0,len(data['用户号'])):
    #for i in range(0,10):
        try:
            #resp = request.urlopen('https://www.federalreserve.gov/releases/H41/20171102/h41.htm')
            url=data.loc[i,'访问页面']
            resp = request.urlopen(url)
            html_data = resp.read().decode('utf-8','ignore')
        except:
            pass
        else:
            #soup = bs(html_data, 'html.parser')  
            selector = etree.HTML(html_data) 
            str1='/html/body/div[3]/div/div[1]/a[2]'
            str2='//text()'
            path=str1+str2
            try:
                data.loc[i,'classify_1'] = selector.xpath(path)[0]
                #print(classify_1)
                str3='/html/body/div[3]/div/div[1]/a[3]'
                path=str3+str2
                data.loc[i,'classify_2'] = selector.xpath(path)[0]
                #print(classify_2)
                str4='/html/body/div[3]/div/div[1]/a[4]'
                path=str4+str2
                data.loc[i,'classify_3'] = selector.xpath(path)[0]
                #print(classify_2)
        
         
                path='/html/body/div[5]/div/div[1]/div[1]/p[2]/span[2]//text()'
                region=selector.xpath(path)
                print(region)
                print(len(region))
                if len(region)==2:
                    data.loc[i,'province']=region[0].strip().replace('-','')          
                    data.loc[i,'city']=region[1].strip()
                else:
                    data.loc[i,'province']=region[0].strip().replace('-','')  
                #print(region)
            except:
                pass
    str1='data_'
    #str1='C:/Users/heyouxin/Documents/PythonCodes/Web scraping/data/data_'
    str2='.xlsx'
    filename=str1+part+str2 
    data.to_excel(filename,index=False,encoding='utf8')
