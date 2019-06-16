# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：        model_alert
   Description :
   Author :           何友鑫
   Create date：      2018-07-25
   Latest version:    v1.2.0
-------------------------------------------------
   Change Log:
#-----------------------------------------------#
v1.2.0  hyx    2018.11.02:
1.输出各个指标具体的得分。
#-----------------------------------------------#
v1.1.0  hyx    2018.9.27:
1.解决回归前有无穷大的
2.恢复gy之前的部分改动
3.主程序分离，只保留model_alert类
4.去掉ModelScore_2函数，此为测试函数
#-----------------------------------------------#
v1.0.0  hyx    2018.7.25:
1.建立违约预警模型类 ModelAlert 包括成员函数：DataSplit、BinWoe、Prob2Score、KS、ModifyDf、TestDataMapped
2.功能上，训练样本定性、定量指标woe转换。测试样本分箱、WOE值的映射。
3.架构上，该模块主要负责少数数据处理函数及建模。部分处理函数依赖于功能函数文件function_alert
#-----------------------------------------------#
-------------------------------------------------
"""


import pandas as pd
from sklearn.model_selection import train_test_split
import function_alert
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import roc_auc_score
import statsmodels.api as sm
import datetime
from statsmodels.stats.outliers_influence import variance_inflation_factor
import model_rolling as model_rolling
from sklearn.metrics import classification_report
from sklearn import metrics

'''
#在console里执行 修改后的代码需要reload
from importlib import reload
reload(function_alert)
'''
class ModelAlert():
    ##成员变量初始化
    def __init__(self,data=None, data_train=None, data_test=None, is_rolling=0):
        '''v1.1
        df = data_train
        for num in range(len(df.columns)):
            if df.iloc[:, num].dtype == object:
                df.iloc[:, num] = df.iloc[:, num].astype('category')
        data_train = df
        df = data_test
        for num in range(len(df.columns)):
            if df.iloc[:, num].dtype == object:
                df.iloc[:, num] = df.iloc[:, num].astype('category')
        data_test = df
        data_test.is_default = 0
        '''
        if is_rolling==0:
            #原始数据
            self.data=data
            #训练样本
            self.data_train=pd.DataFrame()
            #测试样本
            self.data_test=pd.DataFrame()
            #特征工程变量
            self.var = ['underwriter_default_number','underwriter_already_number','underwriter_default_ratio','default_history',
                        'already_history','now_history','CPI','ChinaNewsBasedEPU','GDP','alpha','belta','belta_yj','belta_yz','consumption',
                        'creditspread','finance_1','finance_2','finance_3','finance_4','finance_5','finance_6','finance_7','finance_8','finance_9','finance_10','finance_11','finance_12','finance_13','finance_14','finance_15','listed','company_type','exchange','industry','province']
            #定性变量
            self.var_factor = ['listed','company_type','exchange','industry','province']
            #定量变量
            self.var_quant = ['underwriter_default_number','underwriter_already_number','underwriter_default_ratio','default_history','already_history','now_history','CPI','ChinaNewsBasedEPU','GDP','alpha','belta','belta_yj','belta_yz','consumption','creditspread','finance_1','finance_2','finance_3','finance_4','finance_5','finance_6','finance_7','finance_8','finance_9','finance_10','finance_11','finance_12','finance_13','finance_14','finance_15']


        else:
            self.data_train=data_train[['code',\
            'underwriter_default_number','underwriter_already_number',\
            'underwriter_default_ratio','default_history','already_history','now_history','CPI',\
            'ChinaNewsBasedEPU','GDP_growth_rate','alpha','belta','belta_yj','belta_yz','consumption',\
            'finance_1','finance_2','finance_3','finance_4','finance_5','finance_6','finance_7','finance_8',\
            'finance_9','finance_10','finance_11','finance_12','finance_13','finance_14','finance_15',\
            'total_100million','year','has_sponsor','underwriter_number',\
            'listed','bond_type_wind_1','company_type','exchange','industry','province',\
            'is_default']].dropna()

            self.data_test=data_test[['code',\
            'underwriter_default_number','underwriter_already_number',\
            'underwriter_default_ratio','default_history','already_history','now_history','CPI',\
            'ChinaNewsBasedEPU','GDP_growth_rate','alpha','belta','belta_yj','belta_yz','consumption',\
            'finance_1','finance_2','finance_3','finance_4','finance_5','finance_6','finance_7','finance_8',\
            'finance_9','finance_10','finance_11','finance_12','finance_13','finance_14','finance_15',\
            'total_100million','year','has_sponsor','underwriter_number',\
            'listed','bond_type_wind_1','company_type','exchange','industry','province',\
            'is_default']].dropna()

            self.var=['underwriter_default_number','underwriter_already_number','underwriter_default_ratio','default_history','already_history','now_history','total_100million','year','has_sponsor','underwriter_number','listed','bond_type_wind_1','company_type','exchange','industry','province',
            'CPI','ChinaNewsBasedEPU','GDP_growth_rate','consumption'\
            'alpha','belta','belta_yj','belta_yz',\
            'finance_1','finance_2','finance_3','finance_4','finance_5','finance_6','finance_7','finance_8','finance_9','finance_10','finance_11','finance_12','finance_13','finance_14','finance_15']
            self.var_factor=['listed','bond_type_wind_1','company_type','exchange','industry','province']

            self.var_quant=['underwriter_default_number','underwriter_already_number',\
            'underwriter_default_ratio','default_history','already_history','now_history','CPI',\
            'ChinaNewsBasedEPU','GDP_growth_rate','alpha','belta','belta_yj','belta_yz','consumption',\
            'finance_1','finance_2','finance_3','finance_4','finance_5','finance_6','finance_7','finance_8',\
            'finance_9','finance_10','finance_11','finance_12','finance_13','finance_14','finance_15',\
            'total_100million','year','has_sponsor','underwriter_number']
        #连续型变量
        self.continous_merged_dict={}
        #需要合并分箱
        self.merge_bin_dict={}
        #取值大于5的定性指标，先按bad rate编码，当作连续型处理
        self.br_encoding_dict={}
        #变量分箱列表 var+'_Bin'
        self.var_bin_list={}
        #取值个数<5定性变量列表
        self.var_less=[]
        #变量woe值列表   var+'_Bin'+'_WOE'
        self.multi_analysis=[]
        #WOE与分箱对照字典
        self.WOE_dict={}
        #IV值对照字典
        self.IV_dict={}

        #分数储存
        self.score = pd.DataFrame()

    ##确定入模指标及数据划分(分层抽样)    i是划分随机种子   这样封装有利于之后做重复模拟
    def DataSplit(self,i=0):
        '''
        :param data: 需要抽样的数据框
        :param i: 划分随机数种子
        '''
        self.data.loc[self.data['listed']=='是','listed']=1
        self.data.loc[self.data['listed']=='否','listed']=0
        ##选取入模指标
        self.data=self.data.loc[:,['code','underwriter_default_number','underwriter_already_number',\
        'underwriter_default_ratio','default_history','already_history','now_history','CPI',\
        'ChinaNewsBasedEPU','GDP','alpha','belta','belta_yj','belta_yz','consumption','creditspread',\
        'finance_1','finance_2','finance_3','finance_4','finance_5','finance_6','finance_7','finance_8',\
        'finance_9','finance_10','finance_11','finance_12','finance_13','finance_14','finance_15','listed',\
        'company_type','exchange','industry','province','is_default']].dropna()

        ##划分测试集、训练集
        data_not_default=self.data[self.data['is_default']==0]
        data_default=self.data[self.data['is_default']==1]

        X_Ndefault=data_not_default.loc[:,['code','underwriter_default_number','underwriter_already_number','underwriter_default_ratio','default_history','already_history','now_history','CPI','ChinaNewsBasedEPU','GDP','alpha','belta','belta_yj','belta_yz','consumption','creditspread','finance_1','finance_2','finance_3','finance_4','finance_5','finance_6','finance_7','finance_8','finance_9','finance_10','finance_11','finance_12','finance_13','finance_14','finance_15','listed','company_type','exchange','industry','province']]
        y_Ndefault=data_not_default.loc[:,'is_default']
        X_Ndefault_train,X_Ndefault_test,y_Ndefault_train,y_Ndefault_test=train_test_split(X_Ndefault,y_Ndefault,test_size=0.25,random_state=i)

        X_default=data_default.loc[:,['code','underwriter_default_number','underwriter_already_number','underwriter_default_ratio','default_history','already_history','now_history','CPI','ChinaNewsBasedEPU','GDP','alpha','belta','belta_yj','belta_yz','consumption','creditspread','finance_1','finance_2','finance_3','finance_4','finance_5','finance_6','finance_7','finance_8','finance_9','finance_10','finance_11','finance_12','finance_13','finance_14','finance_15','listed','company_type','exchange','industry','province']]
        y_default=data_default.loc[:,'is_default']
        X_default_train,X_default_test,y_default_train,y_default_test=train_test_split(X_default,y_default,test_size=0.25,random_state=i)

        X_train=pd.concat([X_Ndefault_train,X_default_train])
        y_train=pd.concat([y_Ndefault_train,y_default_train])


        X_test=pd.concat([X_Ndefault_test,X_default_test])
        y_test=pd.concat([y_Ndefault_test,y_default_test])

        self.data_train=pd.concat([X_train,pd.DataFrame(y_train)],1)
        self.data_test=pd.concat([X_test,pd.DataFrame(y_test)],1)

        #return (self.data_train,self.data_test)

    ##训练数据集分箱及woe转换，具体实现在辅助函数function_alert中
    def BinWoe(self):

        t_start = datetime.datetime.now()
        (self.data_train,self.continous_merged_dict,self.merge_bin_dict,self.br_encoding_dict,self.var_bin_list,self.var_less) = function_alert.BinVar(self.data_train,self.var_factor,self.var_quant)
        t_end = datetime.datetime.now()
        print('Finish BinVar,time costs:',t_end - t_start)
        t_start = datetime.datetime.now()
        (self.data_train,self.WOE_dict,self.IV_dict)=function_alert.WoeTrans(self.data_train,self.var_bin_list,self.var_less)
        t_end = datetime.datetime.now()
        print('Finish WoeTrans,time costs:',t_end - t_start)
        #return (data_Train,short_list_2,continous_merged_dict,merge_bin_dict,br_encoding_dict,WOE_dict)

    ##单变量分析和多变量分析，均基于WOE编码后的值。比较两两线性相关性。如果相关系数的绝对值高于阈值，剔除IV较低的一个
    def FeatureAnalysis(self):
        # 将变量IV值进行降.,序排列，方便后续挑选变量
        IV_dict_sorted = sorted(self.IV_dict.items(), key=lambda x: x[1], reverse=True)

        IV_values = [i[1] for i in IV_dict_sorted]
        IV_name = [i[0] for i in IV_dict_sorted]
        '''
        plt.title('feature IV')
        plt.bar(range(len(IV_values)), IV_values)
        plt.show()
        '''
        # (1)
        # 选取IV>0.02的变量
        high_IV = {k: v for k, v in self.IV_dict.items() if v >= 0.02}
        high_IV_sorted = sorted(high_IV.items(), key=lambda x: x[1], reverse=True)

        short_list = high_IV.keys()
        short_list_2 = []
        for var in short_list:
            #print(var)
            new_var = var + '_WOE'
            self.data_train[new_var] = self.data_train[var].map(self.WOE_dict[var])
            short_list_2.append(new_var)
        # (2)
        # 两两间的线性相关性检验
        # 1，将候选变量按照IV进行降序排列
        # 2，计算第i和第i+1的变量的线性相关系数
        # 3，对于系数超过阈值的两个变量，剔除IV较低的一个
        deleted_index = []
        cnt_vars = len(high_IV_sorted)
        for i in range(cnt_vars):
            if i in deleted_index:
                continue
            x1 = high_IV_sorted[i][0] + "_WOE"
            for j in range(cnt_vars):
                if i == j or j in deleted_index:
                    continue
                y1 = high_IV_sorted[j][0] + "_WOE"
                roh = np.corrcoef(self.data_train[x1], self.data_train[y1])[0, 1]
                if abs(roh) > 0.7:
                    x1_IV = high_IV_sorted[i][1]
                    y1_IV = high_IV_sorted[j][1]
                    if x1_IV > y1_IV:
                        deleted_index.append(j)
                    else:
                        deleted_index.append(i)

        multi_analysis_vars_1 = [high_IV_sorted[i][0] + "_WOE" for i in range(cnt_vars) if i not in deleted_index]

        '''
        # (3)
        多变量分析：VIF 方差膨胀因子 VIF越大 显示共线性越严重   0< VIF < 10 ,不存在多重共线性
        '''
        #X = np.matrix(self.data_train[multi_analysis_vars_1])
        # VIF_list = [variance_inflation_factor(X, i) for i in range(X.shape[1])]
        # max_VIF = max(VIF_list)
        #print('max_VIF:')
        #print(max_VIF)
        # 最大的VIF是2.7，因此这一步认为没有多重共线性
        self.multi_analysis = multi_analysis_vars_1

    ##测试数据映射分箱及woe
    def TestDataMapped(self):
        for var in self.multi_analysis:
            # 取值<5且不需要合并的指标，不需要查找对应分箱，直接查找WOE  listed_WOE
            if var.find('_Bin_WOE') > -1:
                var1 = var.replace('_Bin_WOE', '')
                # 有些取值个数少、但是需要合并的变量
                if var1 in self.merge_bin_dict.keys():
                    print("{} need to be regrouped".format(var1))
                    self.data_test[var1 + '_Bin'] = self.data_test[var1].map(self.merge_bin_dict[var1])

                else:
                    # 有些变量需要用bad rate进行编码
                    if var1.find('_br_encoding') > -1:
                        var2 = var1.replace('_br_encoding', '')
                        print("{} need to be encoded by bad rate".format(var2))
                        self.data_test[var1] = self.data_test[var2].map(self.br_encoding_dict[var2])
                        # 需要注意的是，有可能在测试样中某些值没有出现在训练样本中，从而无法得出对应的bad rate是多少。故可以用最坏（即最大）的bad rate进行编码
                        try:
                            max_br = max(self.data_test[var1])
                        except:
                            max_br = 0
                        self.data_test[var1] = self.data_test[var1].map(lambda x: self.ModifyDf(x, max_br))

                    # 上述处理后，需要加上连续型变量一起进行分箱
                    if -1 not in set(self.data_test[var1]):
                        self.data_test[var1 + '_Bin'] = self.data_test[var1].map(
                            lambda x: function_alert.AssignBin(x, self.continous_merged_dict[var1]))
                    else:
                        self.data_test[var1 + '_Bin'] = self.data_test[var1].map(
                            lambda x: function_alert.AssignBin(x, self.continous_merged_dict[var1], [-1]))

            # WOE编码
            var3 = var.replace('_WOE', '')
            self.data_test[var] = self.data_test[var3].map(self.WOE_dict[var3])


    ##截面预测计算
    def ModelScore(self, is_sign=1):

        #变量分析
        multi_analysis=self.multi_analysis
        ### (1)将多变量分析的后变量带入LR模型中
        y = self.data_train['is_default']
        X = self.data_train[multi_analysis]
        X['intercept'] = 1.0

        LR = sm.Logit(y, X).fit()
        summary = LR.summary2()
        print(summary)
        print(LR.params[0])
        print(LR.params[1])
        print(LR.params[2:len(LR.params)])

        pvals = LR.pvalues
        pvals = pvals.to_dict()
        print(pvals)
        if is_sign==1:
            # 有些变量不显著，需要逐步剔除,p-value>=0.1
            varLargeP = {k: v for k, v in pvals.items() if v >= 0.1}
            varLargeP = sorted(varLargeP.items(), key=lambda d: d[1], reverse=True)
            while (len(varLargeP) > 0 and len(multi_analysis) > 0):
                # 每次迭代中，剔除最不显著的变量，直到
                # (1) 剩余所有变量均显著
                # (2) 没有特征可选
                varMaxP = varLargeP[0][0]
                print(varMaxP)
                if varMaxP == 'intercept':
                    print('the intercept is not significant!')
                    break
                multi_analysis.remove(varMaxP)
                y = self.data_train['is_default']
                X = self.data_train[multi_analysis]
                X['intercept'] = [1] * X.shape[0]

                LR = sm.Logit(y, X).fit()
                pvals = LR.pvalues
                pvals = pvals.to_dict()
                varLargeP = {k: v for k, v in pvals.items() if v >= 0.1}
                varLargeP = sorted(varLargeP.items(), key=lambda d: d[1], reverse=True)
        else:
            y_test = self.data_test['is_default']
            X_test = self.data_test[multi_analysis]
            X_test['intercept'] = 1.0

            self.data_test['prob'] = LR.predict(X_test)

        #计算KS和AUC
        auc = roc_auc_score(self.data_test['is_default'],self.data_test['prob'])
        ks = self.KS(self.data_test, 'prob', 'is_default')
        print(ks, auc)


        '''
        base_point = 600
        PDO = 20
        '''
        base_point = 60
        PDO = 5

        self.data_test['score'] = self.data_test['prob'].map(lambda x: self.Prob2Score(x, base_point, PDO))
        self.data_test['score'] = self.data_test['prob'].map(lambda x: self.Prob2Score(x, base_point, PDO))




        self.data_test = self.data_test.sort_values(by = 'score')

        self.data_test['y_predit'] = 0
        self.data_test.loc[self.data_test['prob']>0.5,'y_predit'] = 1

        default_score=self.data_test[['code','is_default','score','prob','y_predit']]

        #print(testData['score'])

        '''
        #画出分布图
        plt.hist(self.data_test['score'], 100)
        plt.xlabel('score')
        plt.ylabel('freq')
        plt.title('distribution')
        plt.show()
        '''
        return default_score

    ##时间序列预测计算
    def CalcScore(self):

        data_train = self.data_train
        data_test = self.data_test
        multi_analysis = self.multi_analysis

        var_info = []
        var_macro = []
        var_industry = []
        var_finance = []
        for v in multi_analysis:
            if v in ['underwriter_default_ratio_Bin_WOE', 'already_history_Bin_WOE', 'company_type_br_encoding_Bin_WOE',
                     'province_br_encoding_Bin_WOE', 'now_history_Bin_WOE', 'default_history_Bin_WOE',
                     'industry_br_encoding_Bin_WOE', 'exchange_Bin_WOE',
                     'total_100million_Bin_WOE', 'listed_WOE', 'underwriter_already_number_Bin_WOE', 'has_sponsor_Bin_WOE',
                     'underwriter_number_Bin_WOE']:
                var_info.append(v)

            if v in ['consumption_Bin_WOE', 'ChinaNewsBasedEPU_Bin_WOE', 'CPI_Bin_WOE', 'GDP_growth_Bin_WOE',
                     'GDP_Bin_WOE']:
                var_macro.append(v)

            if v in ['alpha_Bin_WOE', 'belta_yz_Bin_WOE', 'belta_yj_Bin_WOE']:
                var_industry.append(v)

            if v in ['finance_12_Bin_WOE', 'finance_7_Bin_WOE', 'finance_9_Bin_WOE', 'finance_1_Bin_WOE',
                     'finance_14_Bin_WOE', 'finance_10_Bin_WOE', \
                     'finance_11_Bin_WOE', 'finance_13_Bin_WOE', 'finance_3_Bin_WOE', 'finance_5_Bin_WOE',
                     'finance_8_Bin_WOE', 'finance_4_Bin_WOE', \
                     'finance_6_Bin_WOE', 'finance_15_Bin_WOE']:
                var_finance.append(v)

        var_all = []
        var_all.extend(var_info)
        var_all.extend(var_macro)
        var_all.extend(var_industry)
        var_all.extend(var_finance)

        '''
        var_all[0:len(var_info)]
        var_all[len(var_info):(len(var_info)+len(var_macro))]
        var_all[len(var_info) + len(var_macro):len(var_info) + len(var_macro)+len(var_industry)]
        var_all[len(var_info) + len(var_macro)+len(var_industry):len(var_all)]
        '''

        ### (1)将多变量分析的后变量带入LR模型中
        y = data_train['is_default']
        X = data_train[var_all]

        y.to_excel('y_train.xlsx',index=False,encoding='utf8')
        X.to_excel('X_train.xlsx',index=False,encoding='utf8')


        '''v1.1
        #data1 = pd.concat([y,X],axis=1)
        #data1.to_excel('regress_data.xlsx',index=False,encoding='utf8')
        
        data1 = data1.replace(float('inf'),np.NaN)
        data1 = data1.replace(-float('inf'),np.NaN)
        data1 = data1.dropna()
        X = data1[var_all]
        y = data1['is_default']
        '''

        X['intercept'] = 1.0
        LR = sm.Logit(y, X).fit()
        summary = LR.summary2()
        print(summary)

        pvals = LR.pvalues
        pvals = pvals.to_dict()
        #print(pvals)

        # 是否去除非显著变量
        is_sign = 0
        if is_sign == 1:
            # 有些变量不显著，需要逐步剔除,p-value>=0.1
            varLargeP = {k: v for k, v in pvals.items() if v >= 0.1}
            varLargeP = sorted(varLargeP.items(), key=lambda d: d[1], reverse=True)
            while (len(varLargeP) > 0 and len(multi_analysis) > 0):
                # 每次迭代中，剔除最不显著的变量，直到
                # (1) 剩余所有变量均显著
                # (2) 没有特征可选
                varMaxP = varLargeP[0][0]
                print(varMaxP)
                if varMaxP == 'intercept':
                    print('the intercept is not significant!')
                    break
                multi_analysis.remove(varMaxP)
                y = data_train['is_default']
                X = data_train[multi_analysis]
                X['intercept'] = [1] * X.shape[0]

                LR = sm.Logit(y, X).fit()
                pvals = LR.pvalues
                pvals = pvals.to_dict()
                varLargeP = {k: v for k, v in pvals.items() if v >= 0.1}
                varLargeP = sorted(varLargeP.items(), key=lambda d: d[1], reverse=True)

        beta_intercept = LR.params[len(LR.params) - 1]

        PD0 = 20
        A = 600

        '''
        PD0 = 5
        A = 0
        '''
        B = PD0 / np.log(2)
        base_point = int(A - B * beta_intercept)

        data_test['score_basepoint'] = base_point

        beta_info = LR.params[0:len(var_info)]
        woe_info = data_test[var_info]
        data_test['score_info'] = 0.0
        for i in range(len(beta_info)):
            temp = woe_info.iloc[:, i].map(lambda x: x * beta_info[i] * (-B))
            temp=temp.fillna(0.0)
            data_test['score_info'] = data_test['score_info'] + temp

        beta_macro = LR.params[len(var_info):(len(var_info) + len(var_macro))]
        woe_macro = data_test[var_macro]
        data_test['score_macro'] = 0.0
        for i in range(len(beta_macro)):
            temp = woe_macro.iloc[:, i].map(lambda x: x * beta_macro[i] * (-B))
            temp = temp.fillna(0.0)
            data_test['score_macro'] = data_test['score_macro'] + temp

        beta_industry = LR.params[len(var_info) + len(var_macro):len(var_info) + len(var_macro) + len(var_industry)]
        woe_industry = data_test[var_industry]
        data_test['score_industry'] = 0.0
        for i in range(len(beta_industry)):
            temp = woe_industry.iloc[:, i].map(lambda x: x * beta_industry[i] * (-B))
            temp = temp.fillna(0.0)
            data_test['score_industry'] = data_test['score_industry'] + temp

        beta_finance = LR.params[len(var_info) + len(var_macro) + len(var_industry):len(var_all)]
        woe_finance = data_test[var_finance]
        data_test['score_finance'] = 0.0
        for i in range(len(beta_finance)):
            temp = woe_finance.iloc[:, i].map(lambda x: x * beta_finance[i] * (-B))
            temp = temp.fillna(0.0)
            data_test['score_finance'] = data_test['score_finance'] + temp

        y_test = data_test['is_default']
        X_test = data_test[var_all]

        y_test.to_excel('y_test.xlsx', index=False, encoding='utf8')
        X_test.to_excel('X_test.xlsx', index=False, encoding='utf8')

        X_test['intercept'] = 1.0
        data_test['prob'] = LR.predict(X_test)

        # data_test['total_score'] = data_test['prob'].map(lambda x:model_alert.Prob2Score(x, base_point, PD0))

        data_test['y_predit'] = 0
        data_test.loc[data_test['prob'] > 0.5, 'y_predit'] = 1
        data_test['y_log'] = np.log(data_test['prob'] / (1 - data_test['prob']))
        data_test['cal_score'] = A - B * data_test['y_log']

        print(data_test['score_info'])

        '''v1.1
        data2 = data_test[['score_info','score_macro','score_industry','score_finance','cal_score']]
        data2['keep_index'] = data2.index
        data2 = data2.replace(float('inf'),np.NaN)
        data2 = data2.replace(-float('inf'),np.NaN)
        data2 = data2.dropna()
        keep_index = np.array(data2.keep_index)
        data_test2 = data_test.loc[data_test.index.isin(keep_index)]
        data_test = data_test2
        '''

        data_test['score_info'] = data_test['score_info'].map(lambda x: int(x))
        data_test['score_macro'] = data_test['score_macro'].map(lambda x: int(x))
        data_test['score_industry'] = data_test['score_industry'].map(lambda x: int(x))
        data_test['score_finance'] = data_test['score_finance'].map(lambda x: int(x))

        data_test['total_score'] = data_test['score_info'] + data_test['score_macro'] + data_test['score_industry'] + \
                                   data_test['score_finance']

        data_test['cal_score']=data_test['cal_score'].fillna(0.0)
        data_test['cal_score'] = data_test['cal_score'].map(lambda x: int(x))
        data_test = data_test.sort_values(by='total_score')

        col = ['code', 'is_default', 'prob', 'y_predit', 'score_basepoint', 'score_info', 'score_macro', 'score_industry',
             'score_finance', 'total_score', 'y_log', 'cal_score']

        #col.extend(multi_analysis)

        default_score = data_test[col]


        return default_score

    def Prob2Score(self,prob, base_point, PDO):
    #将概率转化成分数且为正整数
        y = np.log(prob/(1-prob))
        return int(base_point+PDO/np.log(2)*(-y))

    def KS(self,df, score, target):
        '''
        :param df: 包含目标变量与预测值的数据集
        :param score: 得分或者概率
        :param target: 目标变量
        :return: KS值
        '''
        total = df.groupby([score])[target].count()
        bad = df.groupby([score])[target].sum()
        all = pd.DataFrame({'total':total, 'bad':bad})
        all['good'] = all['total'] - all['bad']
        all[score] = all.index
        all = all.sort_values(by=score,ascending=False)
        all.index = range(len(all))
        all['badCumRate'] = all['bad'].cumsum() / all['bad'].sum()
        all['goodCumRate'] = all['good'].cumsum() / all['good'].sum()
        KS = all.apply(lambda x: x.badCumRate - x.goodCumRate, axis=1)
        return max(KS)

    def ModifyDf(self,x, new_value):
        if np.isnan(x):
            return new_value
        else:
            return x


    def RunSection(self):
        self.DataSplit(0)
        self.BinWoe()
        self.FeatureAnalysis()
        self.TestDataMapped()
        print(self.multi_analysis)
        # score=ModelScore_2(model_alert,model_alert.multi_analysis,model_alert.data_train,model_alert.data_test)
        score = self.ModelScore()
        score.to_excel("scores_section.xlsx",index=False,encoding='utf8')

    def RunRolling(self,split_date):
        self.BinWoe()
        self.FeatureAnalysis()
        self.TestDataMapped()
        #print(self.multi_analysis)
        score = self.CalcScore()
        score['date']=split_date
        self.score = score
        return score



