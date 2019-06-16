# -*- coding: utf-8 -*-
"""

-------------------------------------------------
   File Name：        function_alert
   Description :
   Author :           何友鑫
   Create date：      2018-07-30
   Latest version:    v1.1.0
-------------------------------------------------
   Change Log:
#-----------------------------------------------#
    v1.1.0  hyx    2018.9.27:
    1.修复bad_rate计算bug ——'float division by zero'
#-----------------------------------------------#
    v1.0.0  hyx    2018.7.30:
    1.功能函数 BinBadRate
    2.定性分箱，采用ChiMerge,要求分箱完之后：
    （1）不超过5箱
    （2）Bad Rate单调
    （3）每箱同时包含好坏样本
    （4）特殊值如－1，单独成一箱
    3.定量变量可直接分箱
    类别型变量：
    （a）当取值较多时，先用bad rate编码，再用连续型分箱的方式进行分箱
    （b）当取值较少时：
    （b1）如果每种类别同时包含好坏样本，无需分箱
    （b2）如果有类别只包含好坏样本的一种，需要合并
#-----------------------------------------------#

-------------------------------------------------


"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def BinVar(data_train,var_factor,var_quant):
     ##（1）对定性指标进行分箱：
    #第一步，检查定性变量，取值超过5的变量，需要bad rate编码,再用卡方分箱法进行分箱
    var_more=[]
    var_less=[]

    for v in var_factor:
        value_count=len(set(data_train[v]))
    
        if value_count>5:
            var_more.append(v)
        else:
            if value_count>0:
                var_less.append(v)
        
    # （i）当取值<5时：如果每种类别同时包含好坏样本，无需分箱；如果有类别只包含好坏样本的一种，需要合并
    merge_bin_dict = {}  # 存放需要合并的变量，以及合并方法
    var_bin_list = []  # 由于某个取值没有好或者坏样本而需要合并的变量
    for col in var_less:
   
        binBadRate = BinBadRate(data_train, col, 'is_default')[0]
        if min(binBadRate.values()) == 0:  # 由于某个取值没有坏样本而进行合并
            print('{} need to be combined due to 0 bad rate'.format(col))
            combine_bin = MergeBad0(data_train, col, 'is_default')
            merge_bin_dict[col] = combine_bin
            new_var = col + '_Bin'
            data_train[new_var] = data_train[col].map(combine_bin)
            var_bin_list.append(new_var)
        if max(binBadRate.values()) == 1:  # 由于某个取值没有好样本而进行合并
            print('{} need to be combined due to 0 good rate'.format(col))
            combine_bin = MergeBad0(data_train, col, 'is_default', direction='good')
            merge_bin_dict[col] = combine_bin
            new_var = col + '_Bin'
            data_train[new_var] = data_train[col].map(combine_bin)
            var_bin_list.append(new_var)
    
    # less_value_features里剩下不需要合并的变量
    var_less = [i for i in var_less if i + '_Bin' not in var_bin_list]
    
    # （ii）当取值>5时：用bad rate进行编码，放入连续型变量里
    br_encoding_dict = {}  # 记录按照bad rate进行编码的变量，及编码方式
    for col in var_more:
        br_encoding = BadRateEncoding(data_train, col, 'is_default')
        data_train[col + '_br_encoding'] = br_encoding['encoding']
        br_encoding_dict[col] = br_encoding['bad_rate']
        var_quant.append(col + '_br_encoding')
    

    
    # （iii）对连续型变量进行分箱，包括（ii）中的变量
    continous_merged_dict = {}
    for col in var_quant:
        print("{} is in processing".format(col))
        if -1 not in set(data_train[col]):  # －1会当成特殊值处理。如果没有－1，则所有取值都参与分箱
            max_interval = 5  # 分箱后的最多的箱数
            cutOff = ChiMerge(data_train, col, 'is_default', max_interval=max_interval, special_attribute=[],
                                                 minBinPcnt=0)
            data_train[col + '_Bin'] = data_train[col].map(
                lambda x: AssignBin(x, cutOff, special_attribute=[]))
            monotone = BadRateMonotone(data_train, col + '_Bin', 'is_default')  # 检验分箱后的单调性是否满足
            while (not monotone):
                # 检验分箱后的单调性是否满足。如果不满足，则缩减分箱的个数。
                max_interval -= 1
                cutOff = ChiMerge(data_train, col, 'is_default', max_interval=max_interval, special_attribute=[],
                                                     minBinPcnt=0)
                data_train[col + '_Bin'] = data_train[col].map(
                    lambda x: AssignBin(x, cutOff, special_attribute=[]))
                if max_interval == 2:
                    # 当分箱数为2时，必然单调
                    break
                monotone = BadRateMonotone(data_train, col + '_Bin', 'is_default')
            new_var = col + '_Bin'
            data_train[new_var] = data_train[col].map(lambda x: AssignBin(x, cutOff, special_attribute=[]))
            var_bin_list.append(new_var)
        else:
            max_interval = 5
            # 如果有－1，则除去－1后，其他取值参与分箱
            cutOff = ChiMerge(data_train, col, 'is_default', max_interval=max_interval, special_attribute=[-1],
                                                 minBinPcnt=0)
            data_train[col + '_Bin'] = data_train[col].map(
                lambda x: AssignBin(x, cutOff, special_attribute=[-1]))
            monotone = BadRateMonotone(data_train, col + '_Bin', 'is_default', ['Bin -1'])
            while (not monotone):
                max_interval -= 1
                # 如果有－1，－1的bad rate不参与单调性检验
                cutOff = ChiMerge(data_train, col, 'is_default', max_interval=max_interval, special_attribute=[-1],
                                                     minBinPcnt=0)
                data_train[col + '_Bin'] = data_train[col].map(
                    lambda x: AssignBin(x, cutOff, special_attribute=[-1]))
                if max_interval == 3:
                    # 当分箱数为3-1=2时，必然单调
                    break
                monotone = BadRateMonotone(data_train, col + '_Bin', 'is_default', ['Bin -1'])
            new_var = col + '_Bin'
            data_train[new_var] = data_train[col].map(
                lambda x: AssignBin(x, cutOff, special_attribute=[-1]))
            var_bin_list.append(new_var)
        continous_merged_dict[col] = cutOff
                             
    return (data_train,continous_merged_dict,merge_bin_dict,br_encoding_dict,var_bin_list,var_less)                       



def WoeTrans(data_train,var_bin_list,var_less): 
    WOE_dict = {}
    IV_dict = {}
    # 分箱后的变量进行编码，包括：
    # 1，初始取值个数小于5，且不需要合并的类别型变量。存放在var_less中
    # 2，初始取值个数小于5，需要合并的类别型变量。合并后新的变量存放在var_bin_list中
    # 3，初始取值个数超过5，需要合并的类别型变量。合并后新的变量存放在var_bin_list中
    # 4，连续变量。分箱后新的变量存放在var_bin_list中
    all_var = var_bin_list + var_less
    for var in all_var:
        woe_iv = CalcWOE(data_train, var, 'is_default')
        WOE_dict[var] = woe_iv['WOE']
        IV_dict[var] = woe_iv['IV']
    
   



    return (data_train,WOE_dict,IV_dict)



def BinBadRate(df, col, target, grantRateIndicator=0):
    '''
    :param df: 需要计算好坏比率的数据集
    :param col: 需要计算好坏比率的特征
    :param target: 好坏标签
    :param grantRateIndicator: 1返回总体的坏样本率，0不返回
    :return: 每箱的坏样本率，以及总体的坏样本率（当grantRateIndicator＝＝1时）
    '''
    #print(col)

    total = df.groupby([col])[target].count()
    total = pd.DataFrame({'total': total})
    total.to_excel('total.xlsx')
    bad = df.groupby([col])[target].sum()
    bad = pd.DataFrame({'bad': bad})
    regroup = total.merge(bad, left_index=True, right_index=True, how='left') # 每箱的坏样本数，总样本数
    regroup.reset_index(level=0, inplace=True)
    '''
    try:
        regroup['bad_rate'] = regroup.apply(lambda x: x.bad * 1.0 / x.total, axis=1) # 加上一列坏样本率
    except:
        print(col)
        df.to_excel('error_df.xlsx')
        regroup.to_excel('err_group.xlsx')
    '''
    #v1.1.0 hyx
    #print('v1.1')
    #regroup['bad_rate'] = regroup.apply(lambda x: x.bad * 1.0 / x.total, axis=1)  # 加上一列坏样本率
    regroup['bad_rate'] = regroup.apply(lambda x: 0.00001 if (x.total == 0 or x.bad==0) else x.bad * 1.0 / x.total, axis=1)  # 加上一列坏样本率
    dicts = dict(zip(regroup[col],regroup['bad_rate'])) # 每箱对应的坏样本率组成的字典
    if grantRateIndicator==0:
        return (dicts, regroup)
    N = sum(regroup['total'])
    B = sum(regroup['bad'])
    overallRate = B * 1.0 / N
    return (dicts, regroup, overallRate)



def MergeBad0(df,col,target, direction='bad'):
    '''
     :param df: 包含检验0％或者100%坏样本率
     :param col: 分箱后的变量或者类别型变量。检验其中是否有一组或者多组没有坏样本或者没有好样本。如果是，则需要进行合并
     :param target: 目标变量，0、1表示好、坏
     :return: 合并方案，使得每个组里同时包含好坏样本
     '''
    regroup = BinBadRate(df, col, target)[1]
    if direction == 'bad':
        # 如果是合并0坏样本率的组，则跟最小的非0坏样本率的组进行合并
        regroup = regroup.sort_values(by = 'bad_rate')
    else:
        # 如果是合并0好样本样本率的组，则跟最小的非0好样本率的组进行合并
        regroup = regroup.sort_values(by='bad_rate',ascending=False)
    regroup.index = range(regroup.shape[0])
    col_regroup = [[i] for i in regroup[col]]
    del_index = []
    for i in range(regroup.shape[0]-1):
        col_regroup[i+1] = col_regroup[i] + col_regroup[i+1]
        del_index.append(i)
        if direction == 'bad':
            if regroup['bad_rate'][i+1] > 0:
                break
        else:
            if regroup['bad_rate'][i+1] < 1:
                break
    col_regroup2 = [col_regroup[i] for i in range(len(col_regroup)) if i not in del_index]
    newGroup = {}
    for i in range(len(col_regroup2)):
        for g2 in col_regroup2[i]:
            newGroup[g2] = 'Bin '+str(i)
    return newGroup



def BadRateEncoding(df, col, target):
    '''
    :param df: dataframe containing feature and target
    :param col: the feature that needs to be encoded with bad rate, usually categorical type
    :param target: good/bad indicator
    :return: the assigned bad rate to encode the categorical feature
    '''
    regroup = BinBadRate(df, col, target, grantRateIndicator=0)[1]
    br_dict = regroup[[col,'bad_rate']].set_index([col]).to_dict(orient='index')
    for k, v in br_dict.items():
        br_dict[k] = v['bad_rate']
    badRateEnconding = df[col].map(lambda x: br_dict[x])
    return {'encoding':badRateEnconding, 'bad_rate':br_dict}


def ChiMerge(df, col, target, max_interval=5,special_attribute=[],minBinPcnt=0):
    '''
    :param df: 包含目标变量与分箱属性的数据框
    :param col: 需要分箱的属性
    :param target: 目标变量，取值0或1
    :param max_interval: 最大分箱数。如果原始属性的取值个数低于该参数，不执行这段函数
    :param special_attribute: 不参与分箱的属性取值
    :param minBinPcnt：最小箱的占比，默认为0
    :return: 分箱结果
    '''
    colLevels = sorted(list(set(df[col])))
    N_distinct = len(colLevels)
    if N_distinct <= max_interval:  #如果原始属性的取值个数低于max_interval，不执行这段函数
        print("The number of original levels for {} is less than or equal to max intervals".format(col))
        return colLevels[:-1]
    else:
        if len(special_attribute) >= 1:
            df1 = df.loc[df[col].isin(special_attribute)]
            df2 = df.loc[~df[col].isin(special_attribute)]
        else:
            df2 = df.copy() # 去掉special_attribute后的df
        N_distinct = len(list(set(df2[col])))

        # 步骤一: 通过col对数据集进行分组，求出每组的总样本数与坏样本数
        if N_distinct > 100:
            split_x = SplitData(df2, col, 100)
            df2['temp'] = df2[col].map(lambda x: AssignGroup(x, split_x))
            # Assgingroup函数：每一行的数值和切分点做对比，返回原值在切分后的映射，
            # 经过map以后，生成该特征的值对象的“分箱”后的值
        else:
            df2['temp'] = df2[col]
        # 总体bad rate将被用来计算expected bad count
        (binBadRate, regroup, overallRate) = BinBadRate(df2, 'temp', target, grantRateIndicator=1)

        # 首先，每个单独的属性值将被分为单独的一组
        # 对属性值进行排序，然后两两组别进行合并
        colLevels = sorted(list(set(df2['temp'])))
        groupIntervals = [[i] for i in colLevels] #把每个箱的值打包成[[],[]]的形式

        # 步骤二：建立循环，不断合并最优的相邻两个组别，直到：
        # 1，最终分裂出来的分箱数<＝预设的最大分箱数
        # 2，每箱的占比不低于预设值（可选）
        # 3，每箱同时包含好坏样本
        # 如果有特殊属性，那么最终分裂出来的分箱数＝预设的最大分箱数－特殊属性的个数
        split_intervals = max_interval - len(special_attribute)
        while (len(groupIntervals) > split_intervals):  # 终止条件: 当前分箱数＝预设的分箱数
            # 每次循环时, 计算合并相邻组别后的卡方值。具有最小卡方值的合并方案，是最优方案
            chisqList = []
            for k in range(len(groupIntervals)-1):
                temp_group = groupIntervals[k] + groupIntervals[k+1]
                df2b = regroup.loc[regroup['temp'].isin(temp_group)]
                #chisq = Chi2(df2b, 'total', 'bad', overallRate)
                chisq = Chi2(df2b, 'total', 'bad')
                chisqList.append(chisq)
            best_comnbined = chisqList.index(min(chisqList))
            # 把groupIntervals的值改成类似的值改成类似从[[1][2],[3]]到[[1,2],[3]]
            groupIntervals[best_comnbined] = groupIntervals[best_comnbined] + groupIntervals[best_comnbined+1]
            groupIntervals.remove(groupIntervals[best_comnbined+1])
        groupIntervals = [sorted(i) for i in groupIntervals]
        cutOffPoints = [max(i) for i in groupIntervals[:-1]] #

        # 检查是否有箱没有好或者坏样本。如果有，需要跟相邻的箱进行合并，直到每箱同时包含好坏样本
        groupedvalues = df2['temp'].apply(lambda x: AssignBin(x, cutOffPoints)) #每个原始箱对应卡方分箱后的箱号
        df2['temp_Bin'] = groupedvalues
        (binBadRate,regroup) = BinBadRate(df2, 'temp_Bin', target)
        #返回（每箱坏样本率字典，和包含“列名、坏样本数、总样本数、坏样本率的数据框”）
        [minBadRate, maxBadRate] = [min(binBadRate.values()),max(binBadRate.values())]
        while minBadRate ==0 or maxBadRate == 1:
            # 找出全部为好／坏样本的箱
            indexForBad01 = regroup[regroup['bad_rate'].isin([0,1])].temp_Bin.tolist()
            bin=indexForBad01[0]
            # 如果是最后一箱，则需要和上一个箱进行合并，也就意味着分裂点cutOffPoints中的最后一个需要移除
            if bin == max(regroup.temp_Bin):
                cutOffPoints = cutOffPoints[:-1]
            # 如果是第一箱，则需要和下一个箱进行合并，也就意味着分裂点cutOffPoints中的第一个需要移除
            elif bin == min(regroup.temp_Bin):
                cutOffPoints = cutOffPoints[1:]
            # 如果是中间的某一箱，则需要和前后中的一个箱进行合并，依据是较小的卡方值
            else:
                # 和前一箱进行合并，并且计算卡方值
                currentIndex = list(regroup.temp_Bin).index(bin)
                prevIndex = list(regroup.temp_Bin)[currentIndex - 1]
                df3 = df2.loc[df2['temp_Bin'].isin([prevIndex, bin])]
                (binBadRate, df2b) = BinBadRate(df3, 'temp_Bin', target)
                #chisq1 = Chi2(df2b, 'total', 'bad', overallRate)
                chisq1 = Chi2(df2b, 'total', 'bad')
                # 和后一箱进行合并，并且计算卡方值
                laterIndex = list(regroup.temp_Bin)[currentIndex + 1]
                df3b = df2.loc[df2['temp_Bin'].isin([laterIndex, bin])]
                (binBadRate, df2b) = BinBadRate(df3b, 'temp_Bin', target)
                #chisq2 = Chi2(df2b, 'total', 'bad', overallRate)
                chisq2 = Chi2(df2b, 'total', 'bad')
                if chisq1 < chisq2:
                    cutOffPoints.remove(cutOffPoints[currentIndex - 1])
                else:
                    cutOffPoints.remove(cutOffPoints[currentIndex])
            # 完成合并之后，需要再次计算新的分箱准则下，每箱是否同时包含好坏样本
            groupedvalues = df2['temp'].apply(lambda x: AssignBin(x, cutOffPoints))
            df2['temp_Bin'] = groupedvalues
            (binBadRate, regroup) = BinBadRate(df2, 'temp_Bin', target)
            [minBadRate, maxBadRate] = [min(binBadRate.values()), max(binBadRate.values())]
        # 需要检查分箱后的最小占比
        if minBinPcnt > 0:
            groupedvalues = df2['temp'].apply(lambda x: AssignBin(x, cutOffPoints))
            df2['temp_Bin'] = groupedvalues
            valueCounts = groupedvalues.value_counts().to_frame()
            valueCounts['pcnt'] = valueCounts['temp'].apply(lambda x: x * 1.0 / sum(valueCounts['temp']))
            valueCounts = valueCounts.sort_index()
            minPcnt = min(valueCounts['pcnt'])
            while minPcnt < minBinPcnt and len(cutOffPoints) > 2:
                # 找出占比最小的箱
                indexForMinPcnt = valueCounts[valueCounts['pcnt'] == minPcnt].index.tolist()[0]
                # 如果占比最小的箱是最后一箱，则需要和上一个箱进行合并，也就意味着分裂点cutOffPoints中的最后一个需要移除
                if indexForMinPcnt == max(valueCounts.index):
                    cutOffPoints = cutOffPoints[:-1]
                # 如果占比最小的箱是第一箱，则需要和下一个箱进行合并，也就意味着分裂点cutOffPoints中的第一个需要移除
                elif indexForMinPcnt == min(valueCounts.index):
                    cutOffPoints = cutOffPoints[1:]
                # 如果占比最小的箱是中间的某一箱，则需要和前后中的一个箱进行合并，依据是较小的卡方值
                else:
                    # 和前一箱进行合并，并且计算卡方值
                    currentIndex = list(valueCounts.index).index(indexForMinPcnt)
                    prevIndex = list(valueCounts.index)[currentIndex - 1]
                    df3 = df2.loc[df2['temp_Bin'].isin([prevIndex, indexForMinPcnt])]
                    (binBadRate, df2b) = BinBadRate(df3, 'temp_Bin', target)
                    #chisq1 = Chi2(df2b, 'total', 'bad', overallRate)
                    chisq1 = Chi2(df2b, 'total', 'bad')
                    # 和后一箱进行合并，并且计算卡方值
                    laterIndex = list(valueCounts.index)[currentIndex + 1]
                    df3b = df2.loc[df2['temp_Bin'].isin([laterIndex, indexForMinPcnt])]
                    (binBadRate, df2b) = BinBadRate(df3b, 'temp_Bin', target)
                    #chisq2 = Chi2(df2b, 'total', 'bad', overallRate)
                    chisq2 = Chi2(df2b, 'total', 'bad')
                    if chisq1 < chisq2:
                        cutOffPoints.remove(cutOffPoints[currentIndex - 1])
                    else:
                        cutOffPoints.remove(cutOffPoints[currentIndex])
                groupedvalues = df2['temp'].apply(lambda x: AssignBin(x, cutOffPoints))
                df2['temp_Bin'] = groupedvalues
                valueCounts = groupedvalues.value_counts().to_frame()
                valueCounts['pcnt'] = valueCounts['temp'].apply(lambda x: x * 1.0 / sum(valueCounts['temp']))
                valueCounts = valueCounts.sort_index()
                minPcnt = min(valueCounts['pcnt'])
        cutOffPoints = special_attribute + cutOffPoints
        return cutOffPoints

def AssignBin(x, cutOffPoints,special_attribute=[]):
    '''
    :param x: 某个变量的某个取值
    :param cutOffPoints: 上述变量的分箱结果，用切分点表示
    :param special_attribute:  不参与分箱的特殊取值
    :return: 分箱后的对应的第几个箱，从0开始
    for example, if cutOffPoints = [10,20,30], if x = 7, return Bin 0. If x = 35, return Bin 3
    '''
    numBin = len(cutOffPoints) + 1 + len(special_attribute)
    if x in special_attribute:
        i = special_attribute.index(x)+1
        return 'Bin {}'.format(0-i)
    if x<=cutOffPoints[0]:
        return 'Bin 0'
    elif x > cutOffPoints[-1]:
        return 'Bin {}'.format(numBin-1)
    else:
        for i in range(0,numBin-1):
            if cutOffPoints[i] < x <=  cutOffPoints[i+1]:
                return 'Bin {}'.format(i+1)


## 判断某变量的坏样本率是否单调
def BadRateMonotone(df, sortByVar, target,special_attribute = []):
    '''
    :param df: 包含检验坏样本率的变量，和目标变量
    :param sortByVar: 需要检验坏样本率的变量
    :param target: 目标变量，0、1表示好、坏
    :param special_attribute: 不参与检验的特殊值
    :return: 坏样本率单调与否
    '''
    df2 = df.loc[~df[sortByVar].isin(special_attribute)]
    if len(set(df2[sortByVar])) <= 2:
        return True
    regroup = BinBadRate(df2, sortByVar, target)[1]
    combined = zip(regroup['total'],regroup['bad'])
    badRate = [x[1]*1.0/x[0] for x in combined]
    badRateNotMonotone = [badRate[i]<badRate[i+1] and badRate[i] < badRate[i-1] or badRate[i]>badRate[i+1] and badRate[i] > badRate[i-1]
                       for i in range(1,len(badRate)-1)]
    if True in badRateNotMonotone:
        return False
    else:
        return True



def Chi2(df, total_col, bad_col):
    '''
    :param df: 包含全部样本总计与坏样本总计的数据框
    :param total_col: 全部样本的个数
    :param bad_col: 坏样本的个数
    :return: 卡方值
    '''
    df2 = df.copy()
    # 求出df中，总体的坏样本率和好样本率
    badRate = sum(df2[bad_col])*1.0/sum(df2[total_col])
    # 当全部样本只有好或者坏样本时，卡方值为0
    if badRate in [0,1]:
        return 0
    df2['good'] = df2.apply(lambda x: x[total_col] - x[bad_col], axis = 1)
    goodRate = sum(df2['good']) * 1.0 / sum(df2[total_col])
    # 期望坏（好）样本个数＝全部样本个数*平均坏（好）样本占比
    df2['badExpected'] = df[total_col].apply(lambda x: x*badRate)
    df2['goodExpected'] = df[total_col].apply(lambda x: x * goodRate)
    badCombined = zip(df2['badExpected'], df2[bad_col])
    goodCombined = zip(df2['goodExpected'], df2['good'])
    badChi = [(i[0]-i[1])**2/i[0] for i in badCombined]
    goodChi = [(i[0] - i[1]) ** 2 / i[0] for i in goodCombined]
    chi2 = sum(badChi) + sum(goodChi)
    return chi2


def SplitData(df, col, numOfSplit, special_attribute=[]):
    '''
    :param df: 按照col排序后的数据集
    :param col: 待分箱的变量
    :param numOfSplit: 切分的组别数
    :param special_attribute: 在切分数据集的时候，某些特殊值需要排除在外
    :return: 在原数据集上增加一列，把原始细粒度的col重新划分成粗粒度的值，便于分箱中的合并处理
    '''
    df2 = df.copy()
    if special_attribute != []:
        df2 = df.loc[~df[col].isin(special_attribute)]
    N = df2.shape[0]
    n = int(N/numOfSplit)
    splitPointIndex = [i*n for i in range(1,numOfSplit)]
    rawValues = sorted(list(df2[col]))
    splitPoint = [rawValues[i] for i in splitPointIndex]
    splitPoint = sorted(list(set(splitPoint)))
    return splitPoint # col中“切分点“右边第一个值



def AssignGroup(x, bin):
    '''
    :param x: 某个变量的某个取值
    :param bin: 上述变量的分箱结果
    :return: x在分箱结果下的映射
    '''
    N = len(bin)
    if x<=min(bin):
        return min(bin)
    elif x>max(bin):
        return 10e10
    else:
        for i in range(N-1):
            if bin[i] < x <= bin[i+1]:
                return bin[i+1]
            
            

def CalcWOE(df, col, target):
    '''
    :param df: 包含需要计算WOE的变量和目标变量
    :param col: 需要计算WOE、IV的变量，必须是分箱后的变量，或者不需要分箱的类别型变量
    :param target: 目标变量，0、1表示好、坏
    :return: 返回WOE和IV
    '''

    total = df.groupby([col])[target].count()
    total = pd.DataFrame({'total': total})
    bad = df.groupby([col])[target].sum()
    bad = pd.DataFrame({'bad': bad})
    regroup = total.merge(bad, left_index=True, right_index=True, how='left')
    regroup.reset_index(level=0, inplace=True)

    #bad为0，设为1
    regroup.loc[regroup.loc[:,'bad'] == 0, 'bad'] = 1
    '''
    regroup.to_excel('regroup.xlsx')
    import pandas as pd
    regroup=pd.read_excel('regroup.xlsx')
    '''
    N = sum(regroup['total'])
    B = sum(regroup['bad'])
    regroup['good'] = regroup['total'] - regroup['bad']
    G = N - B
    regroup['bad_pcnt'] = regroup['bad'].map(lambda x: x*1.0/B)
    regroup['good_pcnt'] = regroup['good'].map(lambda x: x * 1.0 / G)
    regroup['WOE'] = regroup.apply(lambda x: np.log(x.good_pcnt*1.0/x.bad_pcnt),axis = 1)
    WOE_dict = regroup[[col,'WOE']].set_index(col).to_dict(orient='index')
    for k, v in WOE_dict.items():
        WOE_dict[k] = v['WOE']
    IV = regroup.apply(lambda x: (x.good_pcnt-x.bad_pcnt)*np.log(x.good_pcnt*1.0/x.bad_pcnt),axis = 1)
    IV = sum(IV)
    return {"WOE": WOE_dict, 'IV':IV}