# -*- coding: utf-8 -*-
"""
Created on Sun Jun 25 17:12:03 2017

@author: 何友鑫
"""
def muPri():
    print ("hello")


class Time:
    def __init__(self):
        self.hour=0
        self.minute=0
        self.second=0
    def printMilitary(self):
        print(self.hour)
    
    
    
class oPair:
    def __init__(self,obj1,obj2):
        self.data=(obj1,obj2)
    def __str__(self):
        return str(self.data)
    
    
myPair=oPair(3,-1)
print (myPair)