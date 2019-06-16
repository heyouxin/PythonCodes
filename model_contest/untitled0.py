# -*- coding: utf-8 -*-
"""
Created on Thu Aug 30 00:47:56 2018

@author: 何友鑫
"""

import math as m
import pandas as pd
from collections import Counter
data=pd.read_excel('dataforprob1.xlsx')
data['itemA']=data['itemA'].map(lambda x:set(x.replace(')','').replace('(','').split(',')))
data['itemB']=data['itemB'].map(lambda x:set(str(x).replace(')','').replace('(','').split(',')))


df=data.loc[0:40,:]
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
#for i in range(0,len(df['id'])):
for i in df[df['itemB']!={'nan'}].index:
    #simi=[1,3,5,2]
    #row=[1,3,5,7]
    simi=[]
    row=[]
    item_row=[]
    item_simi=[]
    items=set()
    df_item=pd.DataFrame()
    df_item['item']=''
    df_item['p_item']=0.0
    for j in range(0,len(df['id'])):
        if (i!=j) and (df.loc[i,'id']!=df.loc[j,'id'] ) and (df.loc[i,'itemA'].intersection(df.loc[j,'itemA'])!=set()):
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
        
        if k==2:
            if len(items)>5:
                k3=set(list(Counter(items).most_common(5)[0][0])+list(Counter(items).most_common(5)[1][0])+list(Counter(items).most_common(5)[2][0])+list(Counter(items).most_common(5)[3][0])+list(Counter(items).most_common(5)[4][0]))
            else:
                k3=set(items)
            item_K3.append(k3)
            #应不应该取差分！
            #item_K3.append(items-df.loc[i,'itemA']) 
            
       
        
        if k==4:         
            if len(items)>5:
                k5=set(list(Counter(items).most_common(5)[0][0])+list(Counter(items).most_common(5)[1][0])+list(Counter(items).most_common(5)[2][0])+list(Counter(items).most_common(5)[3][0])+list(Counter(items).most_common(5)[4][0]))
            else:
                k5=set(items)
            item_K5.append(k5)

        if k==9:
            if len(items)>5:
                k10=set(list(Counter(items).most_common(5)[0][0])+list(Counter(items).most_common(5)[1][0])+list(Counter(items).most_common(5)[2][0])+list(Counter(items).most_common(5)[3][0])+list(Counter(items).most_common(5)[4][0]))
            else:
                k10=set(items)
     
            item_K10.append(k10)
