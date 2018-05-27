# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 16:47:42 2017

@author: 何友鑫
"""
import pandas as pd
import selenium
from selenium.webdriver.common.keys import Keys 
import time  
from selenium import webdriver





def lecPhantomJS(n,ID,password):
    '''
    global user_id,password
    ID='15320161152320'
    password='wskdcqqq'
    '''
    
    
    
    for times in range(0,9):
        browser=webdriver.PhantomJS()
        browser.get('http://event.soe.xmu.edu.cn')

        user_id=None
        while user_id is None:
            try:
                user_id=browser.find_element_by_name("UserName")
                #print(n)
            except:
                time.sleep(3)
                browser.refresh()

        user_id.send_keys(ID)
        user_password=browser.find_element_by_name("Password")
        user_password.send_keys(password)
        
        submitElement=browser.find_element_by_css_selector('.click-logon').click()
        time.sleep(2)
        
        #ctl00_MainContent_GridView1_ctl04_btnrefuse
        '''
        else:
            js = " window.open('http://event.soe.xmu.edu.cn/LectureOrder.aspx')" #可以看到是打开新的标签页 不是窗口
            browser.execute_script(js)
            time.sleep(3)
        '''    
        token=0
        str1='#ctl00_MainContent_GridView1 > tbody:nth-child(1) > tr:nth-child('
        str2=') > td:nth-child(14)'
        '''
        action=[]
     
        for i in range(2,20):    
            try:    
                webElems=browser.find_element_by_css_selector(str1+str(i)+str2).text
                action.append(webElems)                                              
            except:
                action.append('')
        for j in range(2,20):
            if(action[j]=='Reserve this seminar'):
                token=1                                             
        print(action)
        '''
        try:
            while token==0:
         
                browser.refresh() 
                action=[]
                reservation=[]
                for i in range(2,20):    
                    try:    
                        webElems=browser.find_element_by_css_selector(str1+str(i)+str2).text
                        action.append(webElems)                                              
                    except:
                        action.append('')
                
                for j in range(0,len(action)):
                    
                    if(action[j]=='Reserve this seminar'):
                        reservation.append(j)
                        token=1
                    '''
                    if(action[j]=='Cancel my reservation'): 
                        print(n)
                    '''    
            n=n-1
            if n>len(reservation)-1:
                n=len(reservation)-1
            location="#ctl00_MainContent_GridView1_ctl0"+str(reservation[n]+2)+"_btnreceive"
            make_reservation=browser.find_element_by_css_selector(location).click()
            time.sleep(1)
            print('get a seminar')
            browser.quit()  
            '''
            for m in range(0,len(action)):
                if action[m]=='Reserve this seminar':
                    location="#ctl00_MainContent_GridView1_ctl0"+str(m+1)+"_btnreceive"
                    make_reservation=browser.find_element_by_css_selector(location).click()
                    time.sleep(1)
                    #browser.quit()
     
                #test code
                if action[m]=='Cancel my reservation':
                    print(1)
                    js = " window.open('http://event.soe.xmu.edu.cn/LectureOrder.aspx')" #可以看到是打开新的标签页 不是窗口
                    browser.execute_script(js)
                    time.sleep(10)
                    #browser.quit()
            '''
        except:
            pass

