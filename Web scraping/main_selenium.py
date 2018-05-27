# -*- coding: utf-8 -*-
"""
Created on Tue Mar 27 15:15:41 2018

@author: 何友鑫
"""

from by_PhantomJS import lecPhantomJS
from _chrome import lecChrome
import threading 



class MyThread(threading.Thread):
    """docstring for MyThread"""
 
    def __init__(self, thread_id, name,password) :
        super(MyThread, self).__init__()  #调用父类的构造函数 
        self.thread_id = thread_id
        self.name = name
        self.password=password

    def run(self) :
  
        lecChrome(self.thread_id,self.name,self.password)
        #lecPhantomJS(self.thread_id,self.name,self.password)

if __name__ == '__main__':

   
    thread1 = MyThread(1, '15420161152166','066547')
    
    
    '''
    thread2 = MyThread(1, '15420161152168','123qwe')
  
    thread3 = MyThread(100, '15420171151968','046600')
    
 
    thread4 = MyThread(2, '15320161152320','wskdcqqq')
  
    thread5 = MyThread(1, '15320161152320','wskdcqqq')
    thread6 = MyThread(2, '15320161152320','wskdcqqq')
    
    thread7 = MyThread(1, '15320161152320','wskdcqqq')
    thread8 = MyThread(2, '15320161152320','wskdcqqq')
    '''
    
    #开启线程
    thread1.start()
    '''
    thread2.start()
    
    thread3.start()
  
    thread4.start()
  
    thread5.start()
    thread6.start() 
    thread7.start()
    thread8.start()
    '''


    thread1.join()
    '''
    thread2.join()
    
   
    thread3.join()
    
    thread4.join()
     
    thread5.join()
    thread6.join()
    thread7.join()
    thread8.join()
    '''