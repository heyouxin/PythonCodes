# -*- coding: utf-8 -*-
"""
Created on Fri Jul 13 09:11:48 2018

@author: 何友鑫
"""


import pandas as pd
import os
import datetime
import numpy as np
import csv
import math
import matplotlib.pyplot as plt
class Woefordf(object):
    os.environ['NLS_LANG']='SIMPLIFIED CHINESE_CHINA.UTF8'
    #类初始化
    def __init__(self,df,group_csv):
        self.col_no=df.shape[1]
        self.get_group_csv(group_csv)
        self.group_dict=self.get_group_dict()
        self.df=df.copy()
        self.df=self.group_woe()
        self.iv=self.create_woe_attr(self.df)
        self.sorteddiv=sorted(self.iv.items,key=lambda d:d[1],reverse=True)
    #生成类的全部变量的woe和iv属性    
    def create_woe_attr(self,df):
        iv_all={}
        for i in range(self.col_no,df.shape[1]):
            woe_matrix,iv=self.get_woe_matrix(df,i)
            attrname=df.columns[i].split('_')[0]
            setattr(self,str(attrname+'_woe'),woe_matrix)
            setattr(self,str(attrname+'_iv'),iv)
            iv_all[str(attrname)]=iv
        return iv_all
    #读取csv生成字典和列表
    def get_group_csv(self,gcsv):
        self.Group=pd.read_csv(gcsv)
        self.group_type=dict([item.split('_') for item in self.Group.columns.tolist()])
        self.group_dict=dict.fromkeys(list(self.group_type.keys()))
    #获取字典和列表并生成python格式
    def get_group_dict(self):
        for i in range(self.Group.shape[1]):
            group_name=self.Group.iloc[:,i].name.split('_')[0]
            if self.Group.iloc[:,1].name.split('_')[1]=='int':
                branch_group=[]
                for item in self.Group.iloc[:,i]:
                    if pd.isnull(item) is not True:
                        branch_group.append(item)
                self.group_dict[group_name]=branch_group
            elif self.Group.iloc[:,i].name.split('_')[1]=='str':
                branch_group_dict={}
                for item in self.Group.iloc[:,i]:
                    if pd.isnull(item) is not True:
                        branch_group_name=item.split(':')[0]
                        branch_classfy=item.split(':')[1].split(',')
                        branch_group=[]
                        for classfy in branch_classfy:
                            branch_group.append(str(classfy))
                        branch_group_dict[branch_group_name]=branch_group
                self.group_dict[group_name]=branch_group_dict
            elif self.Group.iloc[:,i].name.split('_')[1]=='time':
                branch_group=[]
                for item in self.Group.iloc[:,i]:
                    if pd.isnull(item) is not True:
                        time_object=datetime.datetime.strptime(item,'%Y/%m/%d')
                        branch_group.append(time_object)
                self.group_dict[group_name]=branch_group
        return self.group_dict
    #对int变量返回分组结果
    def get_int_group(self,item,lt):
        for lt_item in lt:
            if item<=lt_item:
                return str(int(lt_item))+'-'
            elif lt_item==lt[-1]:
                return str(int(lt_item))+'+'
            else:
                continue
    #对str型变量返回分组结果
    def get_str_group(self,item,dt):
        for key in dt:
            if item in dt[key]:
                return key
        return '其他'
    #对time型变量返回分组结果
    def get_time_group(self,item,lt):
        for lt_item in lt:
            if item<=lt_item:
                return lt_item.strftime("%Y-%m-%d")+'以前'
            elif lt_item==lt[-1]:
                return lt_item.strftime("%Y-%m-%d")+'以后'
            else:
                continue
            
    #输入df矩阵，返回包含分组结果的df
    def group_woe(self):
        col_no=self.df.shape[1]
        for i in range(1,col_no):
            col=self.df.iloc[:,i]
            if self.group_type[col.name]=='int':
                self.df[col.name+'_Grouped']=[self.get_int_group(item,self.group_dict[col.name]) for item in self.df[col.name]]
            elif self.group_type[col.name]=='str':
                self.df[col.name+'_Grouped']=[self.get_str_group(item,self.group_dict[col.name]) for item in self.df[col.name]]                
            elif self.group_type[col.name]=='time':
                self.df[col.name+'_Grouped']=[self.get_time_group(item,self.group_dict[col.name]) for item in self.df[col.name]]    
        return self.df
    
    #返回单个woe值，假如分组里面有一个类别数量为0个，则改为1个
    def woe_equal(self,x):
        if x[1]>0 and x[0]>0:
            return math.log(x[1]/x[0])
        elif x[1]==0:
            return math.log(1/x[0])
        else:
            return math.log(x[1])
        
    #返回woe矩阵
    def get_woe_matrix(self,df,col_no):
        woe_matrix=pd.crosstab(df.iloc[:,0],df.iloc[:,col_no])
        woe_matrix_mid=woe_matrix.apply(lambda x:x/np.where(x.sum()>0,x.sum(),1),axis=1)
        woe_col=woe_matrix_mid.apply(lambda x:self.woe_equal(x))
        iv_mid=woe_matrix_mid.apply(lambda x:x[1]-x[0])
        iv=iv_mid*woe_col
        woe_matrix=woe_matrix.append(woe_col,ignore_index=True)
        woe_matrix=woe_matrix.append(iv,ignore_index=True)
        woe_matrix=woe_matrix.rename({2:'WOE值',3:'IV值'})
        #总的IV值
        iv_sum=sum(iv)
        #重新对woe值排序
        col_type=self.group_type[df.iloc[:,col_no].name.split('_')[0]]
        if col_type=='str':
            new_order=sorted(list(self.group_dict[df.iloc[:,col_no].name.split('_')[0]].keys()))
        elif col_type=='int':
            new_order=list(woe_matrix.columns)
            for i in range(len(new_order)):
                for j in range(i+1,len(new_order)):
                    if int(new_order[i].strip('-+'))>int(new_order[j].strip('-+')):
                        tmp=new_order[i]
                        new_order[i]=new_order[j]
                        new_order[j]=tmp
                        continue
            for i in range(len(new_order)-1,-1,-1):
                if '+' in new_order[i]:
                    tmp=new_order[len(new_order)-1]
                    new_order[len(new_order)-1]=new_order[i]
                    new_order[i]=tmp
                    continue
        else:
            new_order=list(woe_matrix.columns)
            for i in range(len(new_order)-1,-1,-1):
                if '以后' in new_order[i]:
                    tmp=new_order[len(new_order)-1]
                    new_order[len(new_order)-1]=new_order[i]
                    new_order[i]=tmp
                    continue
        woe_matrix=woe_matrix.reindex_axis(new_order,axis=1)
        return woe_matrix,iv_sum
    #绘制全部变量的woe图
    def get_woe_figure(self):
        fig_rowno=int((len(list(self.group_dict.keys()))+1)/2)
        i=1
        plt.figure(figsize=(16,7*fig_rowno))
        for item in self.group_dict.keys():
            woe_v=getattr(self,item+'woe')
            woe_v=woe_v.iloc[2,:]
            plt.subplot(fig_rowno,2,i)
            i=i+1
            woe_v.plot.bar()
            plt.xlabel(woe_v.index.name)
            plt.ylabel('WOE Value')
            ax=plt.gca()
            ax.spines['bottom'].set_position(('data',0))
            for tick in ax.get_xticklabels():
                tick.set_rotation(90)
        plt.show()