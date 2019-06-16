# -*- coding: utf-8 -*-
"""
Created on Tue Aug 28 08:55:11 2018

@author: 何友鑫
"""


from web_scraping import webScraping
import threading 
import pandas as pd


class MyThread(threading.Thread):
    """docstring for MyThread"""
 
    def __init__(self, thread_id, name, data_range) :
        super(MyThread, self).__init__()  #调用父类的构造函数 
        self.thread_id = thread_id
        self.name = name
        self.data_range = data_range
 
    def run(self) :

        webScraping(self.data_range,self.name)
 


if __name__ == '__main__':
    
    data=pd.read_excel('清洗后数据.xlsx',encoding='utf8')
    #data.loc[5,'访问页面']
    data['classify_1']=''
    data['classify_2']=''
    data['classify_3']=''
    data['province']=''
    data['city']=''
    '''
    thread1 = MyThread(1, "Thread-1", data[0:10])
    
    thread2 = MyThread(2, "Thread-2", data[10000:20000].reset_index())
    
    thread3 = MyThread(3, "Thread-3", data[20000:30000].reset_index())
    thread4 = MyThread(4, "Thread-4", data[30000:40000].reset_index())
    thread5 = MyThread(5, "Thread-5", data[40000:50000].reset_index())
    
    thread6 = MyThread(6, "Thread-6", data[50000:len(data['用户号'])].reset_index())
    
    '''
    thread6 = MyThread(6, "Thread-6", data[50050:50060].reset_index())
    
    #开启线程
    '''
    thread1.start()
    thread2.start() 
    thread3.start()
    thread4.start()
    thread5.start()
    '''
    thread6.start()
    '''
    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()
    thread5.join()
    '''
    thread6.join()