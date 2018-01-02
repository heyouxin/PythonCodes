# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 16:47:42 2017

@author: 何友鑫
"""

from selenium import webdriver
browser=webdriver.PhantomJS()
browser.get('https://www.baidu.com')
#browser.implicityly_wait(10)

textElement=browser.find_element_by_class_name('s_ipt')
textElement.send_keys('python selenium')
submitElement=browser.find_element_by_id('su')
submitElement.click()
print(browser.current_url)
