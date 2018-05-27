# -*- coding: utf-8 -*-
"""
Created on Mon Mar 26 11:16:15 2018

@author: 何友鑫
"""

from selenium import webdriver  
from selenium.webdriver.common.keys import Keys  
browse = webdriver.Firefox()  


global user_id,password
ID='15320161152320'
password='wskdcqqq'

browser.get('http://event.soe.xmu.edu.cn/')

user_id=browser.find_element_by_name("UserName")
user_id.send_keys(ID)
user_password=browser.find_element_by_name("Password")
user_password.send_keys(password)

submitElement=browser.find_element_by_css_selector('.click-logon')
submitElement.click()

#webElems = browser.find_element_by_tag_name('a')
webElems = browser.find_element_by_xpath("//*[@id='ctl00_MainContent_GridView1_ctl02_btnrefuse']")
print(webElems)