# -*- coding: utf-8 -*-
"""
Created on Mon Mar 26 11:18:39 2018

@author: 何友鑫
"""

import os  
from selenium import webdriver  
from selenium.webdriver.common.keys import Keys 
import time   


def lecChrome(n,ID,password):
    '''
    global user_id,password
    ID='15320161152320'
    password='wskdcqqq'
    n=1
   
    chromedriver = "C:\chromedriver.exe"  
    os.environ["webdriver.chrome.driver"] = chromedriver       
    browser = webdriver.Chrome(chromedriver)  
    '''   

    
    for times in range(0,9):
        #if i==0:
        chromedriver = "C:\chromedriver.exe"  
        os.environ["webdriver.chrome.driver"] = chromedriver       
        browser = webdriver.Chrome(chromedriver)  
        
        
        if n!=100:
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
        #n=100时作为特殊情况，从主页入口登录
        else:
            browser.get('http://open.xmu.edu.cn/Login?returnUrl=http%3A%2F%2Fopen.xmu.edu.cn%2Foauth2%2Fauthorize%3Fclient_id%3D1085%26response_type%3Dcode')
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
            
            submitElement=browser.find_element_by_css_selector('#LoginButton').click()
            time.sleep(2)
            submitElement=browser.find_element_by_css_selector('.show-view > ul:nth-child(4) > li:nth-child(3) > a:nth-child(1)').click()
            time.sleep(5)
            browser.get('http://event.soe.xmu.edu.cn/LectureOrder.aspx')
            browser.refresh()
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
   
        while token==0:
     
            browser.refresh() 
            action=[]
            reservation=[]
            for i in range(2,20):  
                #ctl00_MainContent_GridView1 > tbody:nth-child(1) > tr:nth-child(10) > td:nth-child(14)
                #if i!=11:
                try:    
                    webElems=browser.find_element_by_css_selector(str1+str(i)+str2).text
                    action.append(webElems)                                              
                except:
                    action.append('')
                
            for j in range(0,len(action)):
                
                if(action[j]=='Reserve this seminar' ):
                    reservation.append(j)
                    token=1
                '''
                if(action[j]=='Cancel my reservation'): 
                    print(n)
                '''    
        n=n-1
        if n>len(reservation)-1:
            n=len(reservation)-1
        '''
        try:
            
            location="#ctl00_MainContent_GridView1_ctl10_btnreceive"
            #location="//*[@id='ctl00_MainContent_GridView1_ctl10_btnreceive']"
            make_reservation=browser.find_element_by_css_selector(location).click()
            time.sleep(1)
            print('get a seminar')
            browser.quit() 
        except:
            pass
       
        try:
            location="#ctl00_MainContent_GridView1_ctl0"+str(reservation[n]+2)+"_btnreceive"
            make_reservation=browser.find_element_by_css_selector(location).click()
            time.sleep(1)
            print('get a seminar')
            browser.quit() 
        except:
            pass
        '''
        #if reservation[n]+2 <10:
        try:
            location="#ctl00_MainContent_GridView1_ctl0"+str(reservation[n]+2)+"_btnreceive"
            make_reservation=browser.find_element_by_css_selector(location).click()
            time.sleep(1)
            print('get a seminar')
            browser.quit()
        except:
            pass
        '''
        try:
            location="#ctl00_MainContent_GridView1_ctl0"+str(reservation[n]+1)+"_btnreceive"
            make_reservation=browser.find_element_by_css_selector(location).click()
            time.sleep(1)
            print('get a seminar')
            browser.quit()
        except:
            pass
        
        try:
            location="#ctl00_MainContent_GridView1_ctl0"+str(reservation[n])+"_btnreceive"
            make_reservation=browser.find_element_by_css_selector(location).click()
            time.sleep(1)
            print('get a seminar')
            browser.quit()
        except:
            pass
        #else: 
        '''
        try:
            location="#ctl00_MainContent_GridView1_ctl"+str(reservation[n]+2)+"_btnreceive"
            make_reservation=browser.find_element_by_css_selector(location).click()
            time.sleep(1)
            print('get a seminar')
            browser.quit()
        except:
            pass
        '''
        try:
            location="#ctl00_MainContent_GridView1_ctl0"+str(reservation[n]+4)+"_btnreceive"
        except:
            pass
        try:
            location="#ctl00_MainContent_GridView1_ctl0"+str(reservation[n]+5)+"_btnreceive"
        except:
            pass
        #make_reservation=browser.find_element_by_css_selector(location).click()
        #make_reservation=browser.find_element_by_xpath(location).click()
        '''
 
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
    

#ctl00_MainContent_GridView1_ctl10_btnreceive
#webElems.text

'''
Action <- unlist(lapply(webElems, function(x){x$getElementText()}))
  while(!any(Action[]=="Reserve this seminar"))
  {
    #Sys.sleep(1)
    remDr$refresh() 
    webElems <- remDr$findElements(using = 'css selector', "td:nth-child(14)")
    Action <- unlist(lapply(webElems, function(x){x$getElementText()}))
    
  }

  n <- length(Action)
  for (i in 1:n) 
  {
    if(Action[i]=="Reserve this seminar")
    {
      location <- paste0("#ctl00_MainContent_GridView1_ctl0",i+1,"_btnreceive")
      make_reservation <- remDr$findElement(using = 'css selector', location)
      make_reservation$clickElement()
      #Sys.sleep(3)
      Sys.sleep(1)
    }
  }


print(browser.current_url)
print(browser.title)
'''