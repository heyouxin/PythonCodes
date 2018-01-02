# -*- coding: utf-8 -*-
"""
Created on Mon Dec 11 14:08:24 2017

@author: 何友鑫
"""


from get_date import getDate
from web_scraping import webScraping
import threading 



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
    (date_1,date_2,date_3)=getDate()
    thread1 = MyThread(1, "Thread-1", date_1[0:500])
    thread2 = MyThread(2, "Thread-2", date_1[501:len(date_1)])
    
    thread3 = MyThread(3, "Thread-3", date_2)
    thread4 = MyThread(4, "Thread-4", date_3)
 
    #开启线程
    thread1.start()
    thread2.start() 
    thread3.start()
    thread4.start()

    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()
    
    
 '''
            webScraping(date_1[946:949],"Thread-test")
        thread_test = MyThread(101, "Thread-test", date_1[945:947])
        thread_test.start()
        thread_test.join()
 ''' 
