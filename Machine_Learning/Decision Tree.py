# -*- coding: utf-8 -*-
"""
Created on Mon Jan  8 19:37:07 2018

@author: 何友鑫
"""
from collections import Counter
Counter(set(D_train[0][1],D_train[1][1]))
A_attribute=['色泽','根蒂','敲声']
x1={'色泽':'绿','根蒂':'卷','敲声':'响亮'}
x2={'色泽':'青','根蒂':'卷','敲声':'响亮'}
x3={'色泽':'绿','根蒂':'直','敲声':'清脆'}
y1=1
y2=1
y3=1
D_train=((x1,y1),(x2,y2),(x3,y3))

D_train[1][1]

def treeGenerate(D_train,A_attribute):
    node=[]
    if D_train[0][1]==D_train[1][1]==D_train[2][1]:
        node.append(D_train[0][1])
        print('case 1')
        return node
    
    if len(A_attribute)<1 or  D_train[0][0]==D_train[1][0]==D_train[2][0]:
        
        node.append(D_train[0][1])
        print('case 2')
        return node
    
    
node=treeGenerate(D_train,A_attribute)   
    




    myTree = ['a',   #root
      ['b',  #left subtree
       ['d', [], []],
       ['e' ,[], []] ],
      ['c',  #right subtree
       ['f', [], []],
       [] ]
     ]
      
      
      myTree[2]