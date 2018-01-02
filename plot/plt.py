# -*- coding: utf-8 -*-
"""
Created on Mon Jan  1 01:02:03 2018

@author: 何友鑫
"""

import pandas as pd
import matplotlib.pyplot as plt


##设置中文字体
from pylab import *  
mpl.rcParams['font.sans-serif'] = ['SimHei']  


data=pd.read_excel("2013_2003_final_6_2.xlsx")

#data.head()


patent_sum=data['patent_num.1'].groupby(data['city_name']).sum()
patent_sum=patent_sum.sort_values(ascending=False)
patent_sum=pd.DataFrame(patent_sum)
patent_sum=patent_sum.rename(columns={'patent_num.1':'patent_sum'})
patent_part_1=patent_sum.ix[0:10,:]
patent_part_2=patent_sum.ix[260:270,:]


#plt.title('2003-2013年医药发明专利数量总和')
fig,axes=plt.subplots(2,1)
patent_part_1.plot(kind='bar',rot=360,ax=axes[0])  
patent_part_2.plot(kind='bar',rot=360,color='r',ax=axes[1])  

