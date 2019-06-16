# -*- coding: utf-8 -*-
"""

-------------------------------------------------
   File Name：        main
   Description :
   Author :           何友鑫
   date：             2018-09-15
   latest version:    v1.0.0
-------------------------------------------------
   Change Log:
    v1.0.0            hyx        2018-09-15
    1.
-------------------------------------------------

"""
import pandas as pd
from datetime import datetime
from pandas.tseries.offsets import Minute
import numpy as np

Pucks=pd.read_excel('C:/Users/heyouxin/Documents/PythonCodes/pingan_bond/DP_airport/InputData.xlsx',sheetname='Pucks')
Pucks.columns=Pucks.columns.map(lambda x:x.replace("\n",""))

Pucks['机体类别']=''
for i in range(0,len(Pucks['飞机型号'])):
    if Pucks.loc[i,'飞机型号'] in ['332', '333', '33E', '33H', '33L', '773']:
        Pucks.loc[i, '机体类别']='W'
    else:
        Pucks.loc[i, '机体类别'] = 'N'


#20号出发或到达的所有航班
Pucks_20=Pucks.loc[(Pucks['到达日期']==pd.Timestamp('2018-01-20')) | (Pucks['出发日期']==pd.Timestamp('2018-01-20')),].reset_index().drop('index',1)
Pucks_20['到达时间']=''
Pucks_20['出发时间']=''
for i in range(0,len(Pucks_20['到达日期'])):
    try:
        Pucks_20.loc[i,'到达时间']=datetime.strptime(str(Pucks_20.loc[i,'到达日期']).split(' ')[0]+' '+str(Pucks_20.loc[i,'到达时刻']),"%Y-%m-%d %H:%M:%S")
    except:
        Pucks_20.loc[i, '到达时间'] = datetime.strptime(
            str(Pucks_20.loc[i, '到达日期']).split(' ')[0] + ' ' + str(Pucks_20.loc[i,'到达时刻']),
            "%Y-%m-%d %H:%M")


    try:
        Pucks_20.loc[i,'出发时间']=datetime.strptime(str(Pucks_20.loc[i,'出发日期']).split(' ')[0]+' '+str(Pucks_20.loc[i,'出发时刻']),"%Y-%m-%d %H:%M:%S")
    except:
        Pucks_20.loc[i, '出发时间'] = datetime.strptime(
            str(Pucks_20.loc[i, '出发日期']).split(' ')[0] + ' ' + str(Pucks_20.loc[i,'出发时刻']),
            "%Y-%m-%d %H:%M")
Pucks_20=Pucks_20.sort_values('到达时间',axis = 0,ascending = True).reset_index().drop('index',1)
##----------------------------------------------------

Gates=pd.read_excel('C:/Users/heyouxin/Documents/PythonCodes/pingan_bond/DP_airport/InputData.xlsx',sheetname='Gates')
Gates.columns=Gates.columns.map(lambda x:x.replace("\n",""))


Pucks_20['登机口']=''
for i in range(0,len(Pucks_20['登机口'])):

    Gates1=Gates.loc[Gates['机体类别'] == Pucks_20.loc[i, '机体类别'],]
    Gates1=Gates1.loc[((Pucks_20.loc[i,'到达类型'] ==Gates1['到达类型']) &(Pucks_20.loc[i,'出发类型'] ==Gates1['出发类型'])) |
                      ((Gates1['到达类型']=='D, I') &(Pucks_20.loc[i,'出发类型'] ==Gates1['出发类型'])) |
                      ((Gates1['到达类型'] == Pucks_20.loc[i,'到达类型']) & (Gates1['出发类型']=='D, I')) |
                      ((Gates1['到达类型'] == 'D, I') & (Gates1['出发类型'] == 'D, I')), ]


    Pucks_20.loc[i,'登机口']=','.join(list(Gates1['登机口']))

Pucks_20['释放登机口时间']=Pucks_20['出发时间'].map(lambda x:x+45*Minute())

##-------------生成登机口冲突的航班矩阵---------------------------------------
n=len(Pucks_20['释放登机口时间'])
T_overlap=np.zeros((n,n))
for i in range(1,n):
    for j in range(0,i):
        if Pucks_20.loc[i,'到达时间']<pd.Timestamp(Pucks_20.loc[j,'释放登机口时间']):
            T_overlap[i,j]=-1

T_overlap=T_overlap.T

T_list=[]
for i in range(0,len(T_overlap)):
    j_list = []
    for j in range(i,len(T_overlap[0,])):
        if T_overlap[0,j]<0:
            j_list.append(j)
        else:
            j_list.append(i-2)
    T_list.append(max(j_list)-i+1)
#-----------------------------------------------------------------------------

for i in range(1,29):
    name1='T'+str(1)
    Pucks_20[name1]=0
for j in range(1,42):
    name1='S'+str(1)
    Pucks_20[name1]=0
for i in range(0,len(Pucks_20['释放登机口时间'])):

    for g in Pucks_20.loc[i, '登机口'].split(','):
        '''
        if Pucks_20.loc[i,'到达航班'].strip()==Pucks_20.loc[i,'出发航班'].strip():
            Pucks_20.loc[i,g]= 1
        else:
            Pucks_20.loc[i,g] = 2
        '''
        if Pucks_20.loc[i,'到达时间'].day==Pucks_20.loc[i,'出发时间'].day:
            Pucks_20.loc[i, g] = 2
        else:
            Pucks_20.loc[i, g] = 1
Pucks_20=Pucks_20.fillna(0)
gates_order=Pucks_20.columns[17:len(Pucks_20.columns)]
##----------------------------------------------------------------------------
##初始化fai1

fai=[]
fai11=[]
fai1=[]

#gates_order[0]
for i in list(Pucks_20.ix[0,17:len(Pucks_20.columns)]):
    if i>0:
        fai11.append(0)
    else:
        fai11.append(1)
#fai11[0]=2
fai1.append(fai11)
fai.append(fai1)


for i in range(1,2):
    fai_i=[]
    #mat_fai_i=np.zeros((len(fai[i-1]),70))
    #for s_fai in fai[i-1]:
    fai_i_list=[]
    df_all=pd.DataFrame()
    for j in range(0,len(fai[i-1])):
        s_fai=fai[i-1][j]
        s_fai_i=[]
        for e in range(0,len(s_fai)):
            elem=max(s_fai[e]-1,0)
            ##step2:
            if elem==0 and gates_order[e] in Pucks_20.loc[i,'登机口'].split(','):
                elem=1

            s_fai_i.append(elem)

        value_replace=T_list[i-1]
        #mat_fai_j=np.zeros((len(s_fai_i),70))

        mat_fai_i=pd.DataFrame(s_fai_i,columns=['fai_i_70'])

        for i in range(1, 68):
        #for i range(1,70):
            name1 = 'fai_i_' + str(i)
            mat_fai_i[name1] = mat_fai_i['fai_i_70']
            if mat_fai_i.ix[i-1,i]==0:
                mat_fai_i.ix[i-1, i]=value_replace

        del mat_fai_i['fai_i_70']
        mat_fai_i['fai_i_70']=mat_fai_i['fai_i_1']

        mat_fai_i=mat_fai_i.T
        df_all=pd.concat([df_all,mat_fai_i])



        #fai_i_list.append(mat_fai_j)
    df_all = df_all.drop_duplicates()
    fai_i=df_all.T
        #fai_i.append(s_fai_i)



    #fai.append(fai_i)




##-----------------------------------------------------------------
##登机口分类：
group=Gates.groupby(by=['到达类型','出发类型','机体类别'])
l_name_1=[]
l_name_2=[]
l_name_3=[]

l_gate=[]
for name,g in group:
    #print(name[0])
    print(g)
    l_name_1.append(name[0])
    l_name_2.append(name[1])
    l_name_3.append(name[2])

    l_gate.append(','.join(list(g['登机口'])))

#d={'登机口类别':l_name,'登机口':l_gate}
gate_classify=pd.DataFrame({'到达类型':l_name_1,'出发类型':l_name_2,'机体类别':l_name_3,'登机口':l_gate})


##-----------------------------------------------------------------
Tickets=pd.read_excel('C:/Users/heyouxin/Documents/PythonCodes/pingan_bond/DP_airport/InputData.xlsx',sheetname='Tickets')
Tickets.columns=Tickets.columns.map(lambda x:x.replace("\n",""))
Tickets_20=Tickets.loc[(Tickets['到达日期']==pd.Timestamp('2018-01-20')) | (Tickets['出发日期']==pd.Timestamp('2018-01-20')),].reset_index().drop('index',1)


for i in range(0,Tickets_20['旅客记录号']):




##满足条件，需要考虑的转场—乘客数据
df1=pd.merge(Pucks_20,Tickets_20)

df2=pd.DataFrame()
Tickets_20.columns
df2=['旅客记录号']=''
df2=['乘客数']=''


Tickets_trans=pd.DataFrame()
for i in range(0,len(Tickets_20['旅客记录号'])):
    for j in range(0,len(Tickets_20['到达航班'])):
    #i=0
        if Tickets_20.loc[i,'到达航班']==Pucks_20.loc[j,'到达航班'] and Tickets_20.loc[i,'出发航班']!=Pucks_20.loc[j,'出发航班']:
            #Pucks_20[j,'Gate']
            Tickets_trans=pd.concat([Tickets_trans,Pucks_20[Pucks_20['出发航班']==Tickets_20.loc[i,'出发航班']]])


##-----------------------------------------------------------------

