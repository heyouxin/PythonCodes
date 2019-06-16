# -*- coding: utf-8 -*-
"""
Created on Fri May 25 11:30:44 2018

@author: 何友鑫
"""
import os  
from selenium import webdriver  
from selenium.webdriver.common.keys import Keys 
import time 




 
chromedriver = "C:\chromedriver.exe"  
os.environ["webdriver.chrome.driver"] = chromedriver       
browser = webdriver.Chrome(chromedriver)  
browser.get('https://music.163.com/#/song?id=536099160')
 

webElems=browser.find_element_by_xpath('/html/body/div[3]/div[1]/div/div/div[2]/div/div[2]/div[2]/div[1]/div[2]/div[1]/div').text