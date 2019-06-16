# -*- coding: utf-8 -*-
"""
Created on Tue Aug 28 10:05:59 2018

@author: 何友鑫
"""
from urllib import request
import requests
from bs4 import BeautifulSoup as bs
from lxml import etree
import pandas as pd
from pandas import DataFrame
from lxml.cssselect import CSSSelector
url='http://www.lawtime.cn/ask/question_6216448.html'



'''
resp=requests.get(url).text
selector=etree.HTML(resp)
'''


#/html/body/div[4]/div/div[1]/div[1]/p[2]/span[2]



resp = request.urlopen(url)
html_data = resp.read().decode('utf-8','ignore')
selector = etree.HTML(html_data)

path='/html/body/div[4]/div/div[1]/div[1]/p[2]/span[2]//text()'
#path='.consult-question-msg > span:nth-child(2)/text()'
region=selector.xpath(path)
print(region)
print(len(region))




TEST=pd.read_excel('TEST.xlsx')
a=set(TEST['A'][0])
a.remove(',')
