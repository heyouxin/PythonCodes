# -*- coding: utf-8 -*-
"""

-------------------------------------------------
   File Name：        recommend_system
   Description :
   Author :           何友鑫
   date：             2018-08-27
   latest version:    v1.0.0
-------------------------------------------------
   Change Log:
    v1.0.0            hyx        2018-08-27
    1.
-------------------------------------------------

"""

import math as m
import pandas as pd
from collections import Counter
import numpy as np
from itertools import chain


def trans_set(elem):
    return set(str(elem).strip().replace(')', '').replace('(', '').split(','))

def trans_set2(elem):
    return set(str(elem).strip().replace('{', '').replace('}', '').replace("'",'').split(','))


def trans_str(elem):
    return str(elem).strip().replace(' ','').replace(')', '').replace('(', '').split(',')

##计算用户目标资源相似度
def clac_similar(df_itemA,x):
    w = len(trans_set(df_itemA).intersection(trans_set(x))) / m.sqrt(
        len(trans_set(df_itemA)) * len(trans_set(x)))
    #print(w)
    return w

##获得用户最感兴趣目标资源
def get_item(df2,K=3,N=5):
    df2 =df2.reset_index()
    L=list(df2.loc[0:K, 'itemA'].map(lambda x: trans_str(x)))
    lst = list(chain(*L))
    while '\n' in lst:
        lst.remove('\n')
    #print(lst)
    item=[]
    if len(set(lst))>5:
        for i in range(0,N):
            item.append(Counter(lst).most_common(5)[i][0])
    else:
        item=lst
    #str(set(item))
    return str(set(item))


if __name__ == "__main__":
    data = pd.read_excel('dataforprob1.xlsx')
    data=data[~data['itemA'].isin([np.nan])].reset_index()
    data['用户号'] = data['用户号'].map(lambda x:str(x).strip())
    #data['itemA'] = data['itemA'].map(lambda x: str(x).strip())
    #data['itemB'] = data['itemB'].map(lambda x: str(x).strip())
    #data['itemA'] = data['itemA'].map(lambda x: set(str(x).replace(')', '').replace('(', '').split(',')))
    #data['itemB'] = data['itemB'].map(lambda x: set(str(x).replace(')', '').replace('(', '').split(',')))


    #df = data.loc[0:3000, :]
    df=data

    test_index=df[~df['itemB'].isin([np.nan])].index

    df['item_K3'] = ''
    df['item_K5'] = ''
    df['item_K10'] = ''
    '''
    item_K3=[]
    item_K5=[]
    item_K10=[]
    '''
    for i in test_index:

        #print(i)
        #df2 = data.loc[0:3000, :]
        df2=data
        df2['w']=0.0
        df2['w']=df2['itemA'].map(lambda x: clac_similar(df.loc[i, 'itemA'],x))
        khh=df.loc[i,'用户号']
        df2.loc[df2['用户号']==khh,'w']=np.NaN
        df2=df2.sort_values('w',ascending = False)

        df.loc[i,'item_K3']=get_item(df2,K=3)
        df.loc[i,'item_K5'] =get_item(df2, K=5)
        df.loc[i, 'item_K10'] = get_item(df2, K=10)
        '''
        item_K3.append(get_item(df2,K=3))
        item_K5.append(get_item(df2, K=5))
        item_K10.append(get_item(df2, K=10))
        '''


df.to_excel('question1___result.xlsx',index=False,encoding='utf8')








'''
# i,j=1,3
for i in range(0, len(df['用户号'])):
    # for i in df[df['itemB']!={'nan'}].index:
    # simi=[1,3,5,2]
    # row=[1,3,5,7]
    # i=0
    simi = []
    row = []
    item_row = []
    item_simi = []
    items = set()
    df_item = pd.DataFrame()
    df_item['item'] = ''
    df_item['p_item'] = 0.0
    # temp=[]
    for j in range(0, len(df['用户号'])):
        if (i != j) and (df.loc[i, '用户号'] != df.loc[j, '用户号']) and (
                df.loc[i, 'itemA'].intersection(df.loc[j, 'itemA']) != set()):
            w = len(df.loc[i, 'itemA'].intersection(df.loc[j, 'itemA'])) / m.sqrt(
                len(df.loc[i, 'itemA']) * len(df.loc[j, 'itemA']))

            # 改进的先放一放
            # *(1/(m.log(1+len(df.loc[i,'itemA'].intersection(df.loc[j,'itemA'])))))
            simi.append(w)
            row.append(j)

    for k in range(0, 10):
        try:
            r = row[simi.index(max(simi))]
            # items=items.union(df.loc[r,'itemA'])
            items = list(items) + list(df.loc[r, 'itemA'])
            item_row.append(r)
            item_simi.append(max(simi))
            simi.remove(max(simi))
            row.remove(row[simi.index(max(simi))])
        except:
            pass
        temp = []

        if k == 2:
            if len(set(items)) > 5:
                temp.append(list(Counter(items).most_common(5)[0])[0])
                temp.append(list(Counter(items).most_common(5)[1])[0])
                temp.append(list(Counter(items).most_common(5)[2])[0])
                temp.append(list(Counter(items).most_common(5)[3])[0])
                temp.append(list(Counter(items).most_common(5)[4])[0])
                item_K3.append(temp)
            else:
                item_K3.append(list(set(items)))

            # 应不应该取差分！
            # item_K3.append(items-df.loc[i,'itemA'])

        if k == 4:
            if len(set(items)) > 5:
                temp.append(list(Counter(items).most_common(5)[0])[0])
                temp.append(list(Counter(items).most_common(5)[1])[0])
                temp.append(list(Counter(items).most_common(5)[2])[0])
                temp.append(list(Counter(items).most_common(5)[3])[0])
                temp.append(list(Counter(items).most_common(5)[4])[0])
                item_K5.append(temp)
                # k5=set(list(Counter(items).most_common(5)[0])[0]+list(Counter(items).most_common(5)[1][0])+list(Counter(items).most_common(5)[1][0])+list(Counter(items).most_common(5)[2][0])+list(Counter(items).most_common(5)[3][0])+list(Counter(items).most_common(5)[4][0]))
            else:
                item_K5.append(list(set(items)))

        if k == 9:
            if len(set(items)) > 5:
                temp.append(list(Counter(items).most_common(5)[0])[0])
                temp.append(list(Counter(items).most_common(5)[1])[0])
                temp.append(list(Counter(items).most_common(5)[2])[0])
                temp.append(list(Counter(items).most_common(5)[3])[0])
                temp.append(list(Counter(items).most_common(5)[4])[0])
                item_K10.append(temp)
            else:
                item_K10.append(list(set(items)))

df['item_K3'] = item_K3

df['item_K5'] = item_K5

df['item_K10'] = item_K10

df.loc[df[df['itemB'] == {'nan'}].index, 'item_K3'] = np.nan
df.loc[df[df['itemB'] == {'nan'}].index, 'item_K5'] = np.nan
df.loc[df[df['itemB'] == {'nan'}].index, 'item_K10'] = np.nan

df.to_excel('demo.xlsx', index=False, encoding='utf8')
'''