# -*- coding: utf-8 -*-
"""
Created on Tue May  8 18:52:13 2018

@author: 何友鑫
"""
import os  
from selenium import webdriver  
from selenium.webdriver.common.keys import Keys 
import time   

import re
last_name='静萱' 
f = open("中国所有姓.txt")  
lines = f.readlines() 
f.close()  
lines.remove('\n')

#for line in lines:
chromedriver = "C:\chromedriver.exe"  
os.environ["webdriver.chrome.driver"] = chromedriver       
browser = webdriver.Chrome(chromedriver)     
browser.get('https://770308740.qzone.qq.com/')
time.sleep(2)
for n in range(0,len(lines)):
    lines[n]=lines[n].replace('\n','')
    temp=re.split(' ',lines[n])
    for i in range(0,len(temp)):
        name=temp[i]+last_name
        question=browser.find_element_by_css_selector("#question_value")
        question.send_keys(name)       
        submitElement=browser.find_element_by_css_selector('#question_submit').click()
        question.clear()
        time.sleep(1)
    
3//2

s="abcda"
#s[0:2]
longestPalindrome(s)
def longestPalindrome( s):
    """
    :type s: str
    :rtype: str
    """
    length=0
    max_len=0
    sub_str=''

    
    if len(s)==1:
        sub_str=s
    else:
        for i in range(0,len(s)-1):
            for j in range(i+1,len(s)):
                if s[i:(((j+i)//2)+1)]==s[((j+i)//2):(j+1)]:
                    length=j-i+1                 
                    max_len=max(length,max_len)
                    if length==max_len:
                        sub_str=s[i:j+1]
                
                
        
    return sub_str       