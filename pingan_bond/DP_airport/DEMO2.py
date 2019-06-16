# -*- coding: utf-8 -*-
"""
Created on Mon Sep 17 10:22:32 2018

@author: TYY
"""

import pandas as pd
import numpy as np

Pucks_20_demo=pd.read_excel('data_demo.xlsx')
#-----------------------------------------------
P_df=Pucks_20_demo.iloc[:,17:len(Pucks_20.columns)]
P_df['dummy']=0
P_df=P_df.T
P=P_df.reset_index().drop('index',1)

#-------------------------------------------

##-------------生成登机口冲突的航班矩阵---------------------------------------
n=len(Pucks_20_demo['释放登机口时间'])
T_overlap=np.zeros((n,n))
for i in range(1,n):
    for j in range(0,i):
        if Pucks_20_demo.loc[i,'到达时间']<pd.Timestamp(Pucks_20_demo.loc[j,'释放登机口时间']):
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


# gate-----------------------------------
gates_order=Pucks_20_demo.columns[17:len(Pucks_20_demo.columns)]

keys=[]
for i in range(0,5):
    keys.append(str(i))
gate=dict(zip(keys,list(gates_order)))
gate['5']='dummy'

#------------------------------------

# T ------------------------------------
T_list=[]
for i in range(0,len(T_overlap)):
    j_list = []
    for j in range(i,len(T_overlap[0,])):
        if T_overlap[0,j]<0:
            j_list.append(j)
        else:
            j_list.append(i-2)
    T_list.append(max(j_list)-i+1)

# M ------------------------------------

col_name=[]
M_value=[]
M_2={}
for i in range(0,len(Pucks_20_demo['登机口'])):
    col_name.append('M'+str(i+1))
    M_value.append(Pucks_20_demo.loc[i,'登机口'].split(','))


for i in range(0,len(M_value)):
    M_value[i]=list(pd.Series(M_value[i]).map(lambda x:int(list(gate.keys())[list(gate.values()).index(x)])))
    M_value[i].sort()
    M_value[i].append(5)
M_2=dict(zip(col_name,M_value))
#M_2['M_dummy']=[i + 1 for i in range(0, 68)]
M_value.append([i  for i in range(0, 6)])
M=M_value


#------------------------------------------------------------


# 函数
def Statefai(s, fai0, T_list, M, P):
    ################step 1 计算 fai_s,mat_fai_s,N_1

    N_1 = []  ##给各个顶点（即状态）编号
    n = 1  # 第一个编号
    fai_s = []  # 状态 i 的列表

    mat_fai_s = np.zeros((len(fai0), len(M[s]) + 1))  # 需要更新的状态矩阵，列数为需要fai0的可能分配集合长度 加1 。表示由fai0 转化到 fai_s 的连线以及 顶点编号

    for k in range(len(fai0)):  # 生成fai_i  step1
        sub_fai_s = []  # 由 i-1 的每一个状态，得到 i 的状态
        for i in range(len(fai0[k])):
            m = max(fai0[k][i] - 1, 0)

            # if m == 0 and i+1 not in list(M.iloc[:,s+1][:-1]):   #更新fai_i  step2
            if m == 0 and i not in M[s + 1][:-1]:  # 从第一步得到的 状态是为0 即可以选择 gate i， 但gate i 不在i可以选择的范围内，故需要将之更新为 1，即不可取状态
                m = 1
            sub_fai_s.append(m)  # 此步得到一个 sub_fai_s

        if sub_fai_s not in fai_s:  # 若上步得到的sub_fai_s 不在fai_s中，则将之添入
            fai_s.append(sub_fai_s)
            N_1.append(n)  # 给每个sub_fai_s编号
            n += 1
        # print(sub_fai_s)

        for l in range(len(M[s])):  # 更新fai_i  step2
            if l != len(M[s]) - 1:  # 非最后一列的处理过程

                g = M[s][l]  # fai0 的可能集合的第一个元素（gate),不包含dummy

                if fai0[k][g] > 0:  # 判断前一状态下，该gate是否被占用
                    mat_fai_s[k, l] = -1  # 存为 -1 表示此条线不存在
                elif T_list[s] < 0:  # 判断是否有overlap的情况
                    mat_fai_s[k, l] = N_1[fai_s.index(sub_fai_s)]  # 更新为第一个sub_fai_s的对应编号
                else:
                    sub_fai_s_update = sub_fai_s[:]  # 更新第一个sub_fai_s
                    sub_fai_s_update[g] = T_list[s]

                    if sub_fai_s_update not in fai_s:  # 如果更新的状态不在fai_s中，那么就将之添加到fai_s中，并对之进行编号
                        fai_s.append(sub_fai_s_update)
                        N_1.append(n)
                        n += 1
                        mat_fai_s[k, l] = N_1[fai_s.index(sub_fai_s_update)]
                    else:
                        mat_fai_s[k, l] = N_1[fai_s.index(sub_fai_s_update)]
            else:  # 最后一列的处理过程
                mat_fai_s[k, l] = N_1[fai_s.index(sub_fai_s)]  # 直接加入

    ################step 2 计算对应的最佳指派矩阵
    value = list(P.iloc[:, s])

    # 初始化
    mat_value_s = np.ones([mat_fai_s.shape[0], len(fai_s)], dtype=int) * (-10000)  # 最大长度矩阵，-100000表示无法到达
    mat_value_loc_s = np.zeros([mat_fai_s.shape[0], len(fai_s)], dtype=str)  # 对应的指派矩阵， ，''表示该点无法指派

    # 更新 mat_value_s 和 mat_value_loc_s
    for i in range(mat_fai_s.shape[0]):
        for j in range(len(fai_s)):
            value_list = []
            num_list = []
            sub_num_list = []

            k = mat_fai_s[i] == N_1[j]
            m = np.where(k != False)[0]  # 不为false的那些元素位置 ——array格式

            if m.size > 0:
                for nn in range(len(m)):
                    mm = M[s][m[nn]]  # 得到fai0 的可能gate
                    #print(mm)
                    value_list.append(value[mm])  # 该gate对应的效用值
                    num_list.append(mm)  # 保存该gate

                # 从上一步得到的效用值列表，取出最大的效用 和 对应的gate
                for p in num_list:
                    if value[p] == max(value_list):
                        mat_value_s[i, j] = max(value_list)  # 得到a点到b点的多条直接连线中的最大value数值
                        sub_num_list.append(p)

                # 将最大效用值对应的 gate 得到的list————sub_num_list 转为 str格式
                if sub_num_list:
                    mat_value_loc_s[i, j] = str(sub_num_list).replace('[', '').replace(']', '')

    ############# step3 点到点的最长路径及其值
    # 初始化一个矩阵  表示 前一阶段的各个状态 到本阶段的各个状态的最大效用
    D0 = np.ones([len(fai0), len(fai_s)]) * (-10000)  # 为 -100000表示到不了该点

    for i in range(len(fai0)):
        for j in range(len(fai_s)):
            # D0[i,j] = G0[i] + mat_value_s[i,j] #G0为传入的参数，表示由第一个点到达前一阶段各个状态的最大效用
            D0[i, j] = mat_value_s[i, j]
    #G_s = np.max(D0, axis=0)  # 取D0 的各列最大值，即到达该列对应编号状态的最大效用
    return fai_s,  D0, mat_value_loc_s


# 运行函数
s = 0  # 第一阶段
fai0 = []  # 第一阶段的状态列表
fai0.append(list(P.iloc[:,0]))
#G0 = np.array([0])  # 第一阶段： 第一个顶点到下一阶段的初始最大值
T_list = T_list
M = M
P = P
# (fai_s,G_s,D0,mat_value_loc_s) = Statefai(s,fai0,T_list,M,P,G0)


D = []
#G = [G0]
fai = [fai0]
mat_value_loc = []

for s in range(5):
    (fai_s,  D0, mat_value_loc_s) = Statefai(s, fai[s], T_list, M, P)







    fai.append(fai_s)
    #G.append(G_s)
    D.append(D0)
    mat_value_loc.append(mat_value_loc_s)




import random

from deap import base
from deap import creator
from deap import tools