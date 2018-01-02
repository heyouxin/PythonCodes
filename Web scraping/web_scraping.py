# -*- coding: utf-8 -*-
"""
Created on Sun Dec 10 17:51:29 2017

@author: 何友鑫
"""


from urllib import request
from bs4 import BeautifulSoup as bs
from lxml import etree
import pandas as pd
from pandas import DataFrame
#from get_date import getDate
#(date_1,date_2,date_3)=getDate()

def webScraping(date,part):
    data_all=[]
    for d in range(0,len(date)):
        str1='https://www.federalreserve.gov/releases/H41/'
        str2='/h41.htm'
        url=str1+date[d]+str2
        try:
            #resp = request.urlopen('https://www.federalreserve.gov/releases/H41/20171102/h41.htm')
            resp = request.urlopen(url)
            html_data = resp.read().decode('utf-8','ignore')
        except:
            pass
        else:
            #soup = bs(html_data, 'html.parser')  
            selector = etree.HTML(html_data)  
            #table_index=['2','5','11','14','16']
            
            #for n in range(0,len(table_index)):
            for n in range(1,40):
                try:                  
                    finder_flag=0
                    str1='/html/body/table['
                    str2=']//text()'
                    #path_str=str1+table_index[n]+str2
                    path_str=str1+str(n)+str2
                    #table_data = selector.xpath('/html/body/table[14]//text()')
                    table_data = selector.xpath(path_str)
            
                    for i in range(0,len(table_data)):
                        move = dict.fromkeys((ord(c) for c in '\xa0\n'))
                        table_data[i] = table_data[i].translate(move)
                        table_data[i]=table_data[i].replace(' ','')
                        #table_data[i]=table_data[i].replace('\xa0','')
                        if(table_data[i].upper()=='TOTALASSETS'):
                            finder_flag=1
                            #print(i)          
                            try:
                                total_assets=int(str(table_data[i+2]).replace(',',''))
                            except:
                                total_assets=int(str(table_data[i+4]).replace(',',''))
                            break
                            #print(total_assets)                      
                    finder=1/finder_flag 
                except:
                    pass
                else:
                    asset_data=[date[d],total_assets]
                    data_all.append(asset_data)
                    #成功就不要进行下次遍历了
                    break

    str1='./data/data_'
    #str1='C:/Users/heyouxin/Documents/PythonCodes/Web scraping/data/data_'
    str2='.csv'
    filename=str1+part+str2 
    DataFrame(data_all).to_csv(filename)        















'''
##test code:

links.xpath(“./child::*”)
  
  
  
  for link in links:
      print (link)
  selector = etree.HTML(html_data)
  links = selector.xpath('/html/body/table[14]/tbody/tr[28]/td[2]/text()')


selector = etree.HTML(html_data)
links = selector.xpath('/html/body/table[14]')



a=soup.find_all('td')
a

#t11r28

a=soup.find_all(text="Total assets")
a.next_sibling

b=soup.find_parents(text='Total assets')

element = soup.find(text='Total assets')
element.parent


c=soup.find_next('td',text='Total assets')

print(soup.find(text='Total assets').__dict__)


a[1]
a.pop()

import re
for tag in soup.find_all(re.compile("^b")):
    print(tag.name)

#t11r28 > b

<b>Total assets</b>
soup.select('Total assets')
  body > table:nth-child(80) > tbody > tr:nth-child(28) > td:nth-child(3) > p
nowplaying_movie = soup.find_all('div', id='nowplaying')
nowplaying_movie_list = nowplaying_movie[0].find_all('li', class_='list-item')
print(soup.p.find_all(text="Total assets"))

for i in range(0,5):
    try:
        c=1/(i-2)
        print(i)
    except:
        pass
    else:
        break
        



'''