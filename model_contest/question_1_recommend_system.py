# -*- coding: utf-8 -*-
"""
Created on Wed Aug 29 17:08:26 2018

@author: 何友鑫
"""

import math as m
import pandas as pd
from collections import Counter
import numpy as np
data=pd.read_excel('dataforprob1.xlsx')
data['itemA']=data['itemA'].map(lambda x:set(str(x).replace(')','').replace('(','').split(',')))
data['itemB']=data['itemB'].map(lambda x:set(str(x).replace(')','').replace('(','').split(',')))


df=data.loc[0:3000,:]
#df[df['itemB']=='nan']
#df[df['itemB']=={'nan'}].index


item_K3=[]
item_K5=[]
item_K10=[]

'''
for i in range(0,len(df['id'])):
    df_1=pd.DataFrame()
    simi=[]
    items=[]
    
    df_2=pd.DataFrame()
    df_2['item']=''
    df_2['p_item']=0.0
        
        
    for j in range(0,len(df['id'])):
        if (i!=j) and (df.loc[i,'id']!=df.loc[j,'id'] ) and (df.loc[i,'itemA'].intersection(df.loc[j,'itemA'])!=set()):
            w=len(df.loc[i,'itemA'].intersection(df.loc[j,'itemA']))/m.sqrt(len(df.loc[i,'itemA'])*len(df.loc[j,'itemA']))          
            simi.append(w)
            items.append(df.loc[j,'itemA'])
    d={'simi':simi,'items':items}
    df_1=pd.DataFrame(d)
    df_1=df_1.sort_values('simi',ascending = False)
    df_1=df_1.reset_index()
    leng=len(df_1['simi'])
    if leng<3:
        df_1['items'][0:3]
            #应不应该取差分！
            #item_K3.append(items-df.loc[i,'itemA'])
            if items>5:
               df_item['item']=items
                      
                
            item_K3.append(items)
        
        if k==4:                    
            item_K5.append(items)
        if k==9:
            item_K10.append(items)



df['item_K3']=item_K3
df['item_K5']=item_K5
df['item_K10']=item_K10

'''
#i,j=1,3
for i in range(0,len(df['用户号'])):
#for i in df[df['itemB']!={'nan'}].index:
    #simi=[1,3,5,2]
    #row=[1,3,5,7]
    #i=0
    simi=[]
    row=[]
    item_row=[]
    item_simi=[]
    items=set()
    df_item=pd.DataFrame()
    df_item['item']=''
    df_item['p_item']=0.0
    #temp=[]
    for j in range(0,len(df['用户号'])):
        if (i!=j) and (df.loc[i,'用户号']!=df.loc[j,'用户号'] ) and (df.loc[i,'itemA'].intersection(df.loc[j,'itemA'])!=set()):
            w=len(df.loc[i,'itemA'].intersection(df.loc[j,'itemA']))/m.sqrt(len(df.loc[i,'itemA'])*len(df.loc[j,'itemA']))
            
            #改进的先放一放     
            #*(1/(m.log(1+len(df.loc[i,'itemA'].intersection(df.loc[j,'itemA'])))))
            simi.append(w)
            row.append(j)
    
    for k in range(0,10): 
        try:
            r=row[simi.index(max(simi))]
            #items=items.union(df.loc[r,'itemA'])
            items=list(items)+list(df.loc[r,'itemA'])
            item_row.append(r)
            item_simi.append(max(simi))
            simi.remove(max(simi))
            row.remove(row[simi.index(max(simi))])
        except:
            pass
        temp=[]

        if k==2:
            if len(set(items))>5:
                temp.append(list(Counter(items).most_common(5)[0])[0])
                temp.append(list(Counter(items).most_common(5)[1])[0])
                temp.append(list(Counter(items).most_common(5)[2])[0])
                temp.append(list(Counter(items).most_common(5)[3])[0])
                temp.append(list(Counter(items).most_common(5)[4])[0])   
                item_K3.append(temp)
            else:
                item_K3.append(list(set(items)))
    
            #应不应该取差分！
            #item_K3.append(items-df.loc[i,'itemA']) 

       
        
        if k==4:         
            if len(set(items))>5:
                temp.append(list(Counter(items).most_common(5)[0])[0])
                temp.append(list(Counter(items).most_common(5)[1])[0])
                temp.append(list(Counter(items).most_common(5)[2])[0])
                temp.append(list(Counter(items).most_common(5)[3])[0])
                temp.append(list(Counter(items).most_common(5)[4])[0])   
                item_K5.append(temp)
                #k5=set(list(Counter(items).most_common(5)[0])[0]+list(Counter(items).most_common(5)[1][0])+list(Counter(items).most_common(5)[1][0])+list(Counter(items).most_common(5)[2][0])+list(Counter(items).most_common(5)[3][0])+list(Counter(items).most_common(5)[4][0]))
            else:
                item_K5.append(list(set(items)))

        if k==9:
            if len(set(items))>5:
                temp.append(list(Counter(items).most_common(5)[0])[0])
                temp.append(list(Counter(items).most_common(5)[1])[0])
                temp.append(list(Counter(items).most_common(5)[2])[0])
                temp.append(list(Counter(items).most_common(5)[3])[0])
                temp.append(list(Counter(items).most_common(5)[4])[0])   
                item_K10.append(temp)     
            else:
                item_K10.append(list(set(items)))
     

df['item_K3']=item_K3

df['item_K5']=item_K5
  
df['item_K10']=item_K10


  
  

df.loc[df[df['itemB']=={'nan'}].index,'item_K3']=np.nan
df.loc[df[df['itemB']=={'nan'}].index,'item_K5']=np.nan
df.loc[df[df['itemB']=={'nan'}].index,'item_K10']=np.nan

      
      
df.to_excel('demo.xlsx',index=False,encoding='utf8')














df.loc[df[df['itemB']!={'nan'}].index,'item_K3']=item_K3
df.loc[df[df['itemB']!={'nan'}].index,'item_K5']=item_K5
df.loc[df[df['itemB']!={'nan'}].index,'item_K10']=item_K10

      

      

  
  
  
df['item_K3']=df['item_K3'].map(lambda x:list(set(x))))
  
  
  
  
  
  
  
  
  
  
  
  
  
set(data['itemA'][0])



#相似度计算
A_set=set(['ad','b','dc'])
B_set=set(['g','b','ff','dc'])
arr=list(A_set)+list(B_set)
arr_appear = dict((a, arr.count(a)) for a in arr)
set(list(Counter(arr).most_common(2)[0][0])+list(Counter(arr).most_common(2)[1][0]))Counter(arr).most_common(2)[2][0]
sorted(arr_appear.items(), lambda x, y: cmp(x[1], y[1]), reverse=True) 

sorted(arr_appear.items())
arr_appear.items()
arr_appear=sorted(arr_appear.values())
[ v for v in sorted(arr_appear.values())] 

A_set.intersection(B_set)
A_set & B_set
(A_set & B_set)==set()
train={'A':A_set,'B':B_set}
type(train.keys())
UserSimilarity(train)
train.items()
for u, items in train.items():
    print(u)
    print(items)

def UserSimilarity(train):  
    # build inverse table for item_users  
    item_users = dict()  
    for u, items in train.items():   
        #for i in items.keys():
        for i in items:   
       
            if i not in item_users:     
                item_users[i] = set()   
            item_users[i].add(u)    
    #calculate co-rated items between users  
    C = dict()  
    N = dict()  
    for i, users in item_users.items():   
        for u in users:    
            N[u] += 1    
            for v in users:     
                if u == v:      
                    continue     
                C[u][v] += 1 
 
    #calculate finial similarity matrix W  
    W = dict()  
    for u, related_users in C.items():   
        for v, cuv in related_users.items():    
            W[u][v] = cuv / math.sqrt(N[u] * N[v])  
            return W 