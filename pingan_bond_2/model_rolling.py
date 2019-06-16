# -*- coding: utf-8 -*-
"""
Created on Fri Aug  3 15:22:19 2018

@author: JessicaGAO
"""

# -*- coding: utf-8 -*-



# <editor-fold desc="Import">
from imblearn.over_sampling import ADASYN
import pandas as pd
import sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn import linear_model
from sklearn.metrics import classification_report
from sklearn import metrics
import numpy as np
from sklearn import svm
from dateutil.relativedelta import relativedelta
from industry_index import Calculate_industry


import datetime
import time
import re
from imblearn.over_sampling import SMOTE
from sklearn.preprocessing import OneHotEncoder

import warnings
import random
warnings.filterwarnings("ignore")
# </editor-fold>



class RawData:
    ##成员变量初始化
    def __init__(self, dict_filename=None, dict_var=None,
                 data_finance_info_all=None, data_default=None, all_cat=None):

        self.dict_filename = dict_filename
        self.dict_var = dict_var

        self.data_finance_info_all = pd.DataFrame()
        self.data_default = pd.read_excel(dict_filename['all_default'])
        self.all_cat = pd.DataFrame()


        self.DataInfoFinance()

    def DataInfoFinance(self):

        print('========= Merge info and finance data')
        ### Merge data frames
        all_bond_info = pd.read_excel(self.dict_filename['all_bond_info'])
        all_comp_info = pd.read_excel(self.dict_filename['all_comp_info'])
        all_finance = pd.read_excel(self.dict_filename['all_finance'])
        all_default = pd.read_excel(self.dict_filename['all_default'])

        ## Information
        Df1_1 = pd.merge(all_bond_info, all_comp_info, how='left', on='issuer')
        default_code = np.array(all_default.code)
        Df1_2 = pd.merge(Df1_1, all_default[['code', 'date_default']], on='code', how='left')
        Df1_2['end'] = Df1_2.apply(
            lambda row: row['date_end'] if isinstance(row['date_default'], pd._libs.tslib.NaTType) else row[
                'date_default'],
            axis=1)

        # 去掉有bond基本信息但没有公司finance数据的债券
        finance_issuer = np.array(all_finance.issuer)
        Df1_3 = Df1_2.loc[Df1_2.issuer.isin(finance_issuer),:]
        Df1_3.index = range(len(Df1_3))
        Df1 = Df1_3
        drop_num = len(Df1_2)-len(Df1_3)
        print('%d只债券匹配到了%d个公司的财务与基本信息数据' % (len(Df1_3),len(Df1_3.issuer.drop_duplicates())))
        print('%d只债券未匹配到公司数据' % drop_num)

        ## Finance
        print('===== Fill NaN in Finance 纵向 同公司 向前填充缺失值')
        all_finance_fill = Fill_pad(all_finance, column='issuer')
        Df2_1 = pd.merge(Df1, all_finance_fill, how='left', on='issuer')
        Df2_1['date_start'] = Df2_1['date_start'].map(pd.Timestamp)
        Df2_1['date_end'] = Df2_1['date_end'].map(pd.Timestamp)
        Df2_1['start'] = Df2_1['date_start'].map(lambda x: x - relativedelta(months=3 * self.dict_var['number_start']))
        Df2_2 = Df2_1[Df2_1.start <= Df2_1.time_report]
        Df2_2.end = Df2_2.end.map(pd.Timestamp)
        Df2_2 = Df2_2[Df2_2.time_report <= Df2_2.end]
        Df2 = Df2_2.drop('start', axis=1)


        ## all_cat Data Frame
        df = Df2
        cat = np.array(df.columns[~df.columns.isin(df.groupby('code').mean().columns)])
        df1 = df[cat].drop_duplicates(subset='code')
        df1['is_default'] = df1.code.map(lambda x: 1 if x in default_code else 0)
        df1.index = range(len(df1))
        all_cat = df1

        self.data_finance_info_all = Df2
        self.all_cat = all_cat

    def CalculateMacroMean(self):
        data_macro = pd.read_excel(self.dict_filename['filename_macro'])
        data_macro1 = data_macro.loc[data_macro.time_report < date, :]
        l_macro = []
        for var in data_macro1.variable.drop_duplicates():
            df0 = data_macro1.loc[data_macro1.variable == var, :].sort_values(by='time_report', ascending=True,
                                                                              axis=0)
            df0.index = range(len(df0))
            value = df0.loc[len(df0) - 3:, 'value'].mean()
            l_macro.append(value)
        return l_macro

class CleanData:
    ##成员变量初始化
    def __init__(self, Raw_data=None, dict_var=None, date_split=None,
                 Clean_data=None, Train_data=None, Test_data=None):
        self.Raw_data = Raw_data
        self.dict_var = dict_var
        self.date_split = date_split

        self.data_clean = pd.DataFrame()
        self.data_train = pd.DataFrame()
        self.data_test = pd.DataFrame()

    def DataPreparation(self):

        Raw_data = self.Raw_data
        Df_info_finance = Raw_data.data_finance_info_all
        Df2 = Df_info_finance
        date_split = self.date_split
        time_now = pd.Timestamp(date_split)

        print('========= Data Preparation')
        print('========= date:', date_split)

        ## Train Test Split
        df = Df2
        train_1 = df.loc[df.end < time_now,]
        test_1 = df.loc[(df.end > time_now) & (time_now > df.date_start),]
        test_1['end'] = time_now

        ## Calculate mean values
        print('===== Calculate mean Finance')
        self.data_train = self.Calculate_mean_finance(train_1)
        self.data_test = self.Calculate_mean_finance(test_1)

        default_code1 = np.array(pd.read_excel(Raw_data.dict_filename['all_default']).code)
        self.data_train['is_default'] = self.data_train.code.map(lambda x: 1 if x in default_code1 else 0)
        self.data_test['is_default'] = np.NaN

        ## Macro
        print('===== Macro')
        self.CalculateMacroMean()

        ## Industry
        print('===== Industry')
        self.Merge_industry()

        ## 特征工程创建变量，并删除部分不用的变量
        print('===== Revise Variables')
        self.Revise_variables()

        df = self.data_clean
        self.data_train = df.loc[df.is_default.isin([0, 1]),]
        self.data_test = df.loc[~df.is_default.isin([0, 1]),]


    def Calculate_mean_finance(self,df):
        number_start = self.dict_var['number_start']
        number_end = self.dict_var['number_end']

        date_end_name = 'end'
        df['calculate_start'] = df[date_end_name].map(lambda x: x - relativedelta(months=3 * number_start))
        df = df[df.calculate_start <= df.time_report]
        df['calculate_end'] = df[date_end_name].map(lambda x: x - relativedelta(months=3 * number_end))
        df.index = range(len(df))
        list_use = []
        for number in range(len(df)):
            if int(str(df.loc[number, date_end_name].month)) in [3, 6, 9, 12]:
                end_day = pd.to_datetime(getDateByTime(df.loc[number, date_end_name]))
                if int(str(df.loc[number, date_end_name].month) + str(df.loc[number, date_end_name].day)) == int(
                        str(end_day.month) + str(end_day.day)):
                    if df.loc[number, 'time_report'] <= df.loc[number, 'calculate_end']: list_use.append(number)
                else:
                    if df.loc[number, 'time_report'] < df.loc[number, 'calculate_end']: list_use.append(number)
            else:
                if df.loc[number, 'time_report'] < df.loc[number, 'calculate_end']: list_use.append(number)
        df = df.iloc[list_use,]
        df = df.drop(['calculate_start', 'calculate_end'], axis=1)
        df_num = df.groupby('code').mean().reset_index().rename(columns={'index': 'code'})

        list_cat = np.array(df.columns[~df.columns.isin(df_num.columns)]).tolist()
        list_cat.append('code')
        df_cat = df.loc[:, list_cat]
        df_cat = df_cat.drop_duplicates(subset='code', keep='first')

        df_num_1 = pd.merge(df_num, df_cat[['code','industry','end']], how='inner', on='code')
        df_num_2 = Fill_na(df_num_1)

        df = pd.merge(df_num_2, df_cat, how='left', on='code')

        return df

    def CalculateMacroMean(self):
        data_macro1 = pd.read_excel(self.Raw_data.dict_filename['filename_macro'])

        # test data
        df = self.data_test
        data_macro2 = data_macro1.loc[data_macro1.time_report < self.date_split, :]
        l_macro = []
        for var in data_macro1.variable.drop_duplicates():
            df0 = data_macro2.loc[data_macro2.variable == var, :].sort_values(by='time_report', ascending=True,axis=0)
            df0.index = range(len(df0))
            value = df0.loc[len(df0) - 3:, 'value'].mean()
            l_macro.append(value)
        l_macro_key = data_macro1.variable.drop_duplicates().tolist()
        for i in range(len(l_macro)):
            df[l_macro_key[i]] = l_macro[i]
        self.data_test = df
        # train_data
        df = self.data_train
        time_report = df.time_report.drop_duplicates()
        d = dict()
        for date1 in time_report:
            data_macro2 = data_macro1.loc[data_macro1.time_report < date1, :]
            l_macro = []
            for var in data_macro1.variable.drop_duplicates():
                df0 = data_macro2.loc[data_macro2.variable == var, :].sort_values(by='time_report', ascending=True,
                                                                                  axis=0)
                df0.index = range(len(df0))
                value = df0.loc[len(df0) - 3:, 'value'].mean()
                l_macro.append(value)
            d[date1] = l_macro
        df1 = pd.DataFrame(d,index=data_macro1.variable.drop_duplicates()
                           ).T.reset_index().rename(columns={'index': 'time_report'})
        df2 = pd.merge(df, df1, on='time_report', how='left')
        self.data_train = df2

    def Merge_industry(self):
        df_all = pd.concat([self.data_test, self.data_train], axis=0)
        bond = df_all[['date_start', 'end', 'code', 'industry']]
        Hangye = Calculate_industry(bond, 'date_start', 'end',
                                    self.Raw_data.dict_filename['filename_capm'],
                                    self.Raw_data.dict_filename['filename_zs'],
                                    self.Raw_data.dict_var['number_start'],
                                    self.Raw_data.dict_var['number_end'])
        Hangye = Hangye.reset_index().rename(columns={'index': 'code'})
        Hangye1 = pd.merge(Hangye, bond[['code', 'industry','end']], on='code', how='right')
        Hangye2 = Fill_na(Hangye1)
        bond1 = pd.merge(df_all, Hangye2, how='inner', on='code')
        self.data_clean = bond1

    def Revise_variables(self):
        df = self.data_clean

        df = Create_variable_sponsor(df)
        df = Create_variable_issuer(df, self.Raw_data.all_cat)
        df = Create_variable_underwriter(df, self.Raw_data.all_cat)
        df.underwriter_default_number = df.underwriter_default_number.fillna(0)
        df.underwriter_already_number = df.underwriter_already_number.fillna(0)
        df.underwriter_default_ratio = df.underwriter_default_ratio.fillna(0)

        # 去除部分不入模的变量
        l_drop = ['bond_type_wind_2', 'balance_100million', 'issuer',
                  'sponsor', 'time_report', 'underwriter',
                  'name', 'date_end', 'date_start', 'date_default', 'end']
        l_drop = pd.Series(l_drop)[pd.Series(l_drop).isin(np.array(df.columns))].tolist()
        df = df.drop(l_drop, axis=1)

        # 填充缺失值、替换部分指标的值
        df = df.replace('-', 'NA')
        df = df.replace('', 'NA')

        df.is_default = df.is_default.fillna(-1)

        print('缺失值情况：')
        for i in range(len(df.columns)):
            print(df.columns[i],df[df.columns[i]].dtype,sum(df[df.columns[i]].isnull()))
        #print(pd.concat([df.apply(lambda x: sum(x.isnull()),0),)

        #l_quant_na = []
        #for x in df.columns:
        #    if df[x].dtype in (np.int, np.float) and sum(df[x].isnull())>0:
        #        print(x)

        df = df.fillna('NA')
        for num in range(len(df.columns)):
            if df.iloc[:, num].dtype not in [np.int,np.float]: #== object:
                #if check_contain_chinese(str(df.iloc[:, 33].astype('category').cat.categories)):
                #    df.iloc[:, num] = df.iloc[:, num].map(Check_x)
                try:
                    df.iloc[:, num] = df.iloc[:, num].astype('category')
                except:
                    continue
        self.data_clean = df

# <editor-fold desc="Define Functions">
def getDateByTime(ts):
    ts = str(ts)
    year = int(ts[:4])
    month = int(ts[5:7])
    day = int(ts[8:10])
    my_date = []
    time_now = str(time.strftime('%Y-%m-', (year, month, day, 0, 0, 0, 0, 0, 0)))
    for number in range(1, 32):
        time_str = time_now + str(number)
        try:
            # 字符串转换为规定格式的时间
            tmp = time.strptime(time_str, '%Y-%m-%d')
            # 判断是否为周六、周日
            if (tmp.tm_wday != 6) and (tmp.tm_wday != 5):
                my_date.append(time.strftime('%Y-%m-%d', tmp))
        except:
            continue
    return my_date[-1]


def datetime_timestamp(dt, type='ms'):
    if isinstance(dt, str):
        try:
            if len(dt) == 10:
                dt = datetime.strptime(dt.replace('/', '-'), '%Y-%m-%d')
            elif len(dt) == 19:
                dt = datetime.strptime(dt.replace('/', '-'), '%Y-%m-%d %H:%M:%S')
            else:
                raise ValueError()
        except ValueError as e:
            raise ValueError(
                "{0} is not supported datetime format."
                "dt Format example: 'yyyy-mm-dd' or yyyy-mm-dd HH:MM:SS".format(dt)
            )

    if isinstance(dt, time.struct_time):
        dt = datetime.strptime(time.stftime('%Y-%m-%d %H:%M:%S', dt), '%Y-%m-%d %H:%M:%S')

    if isinstance(dt, datetime):
        if type == 'ms':
            ts = int(dt.timestamp()) * 1000
        else:
            ts = int(dt.timestamp())
    else:
        raise ValueError(
            "dt type not supported. dt Format example: 'yyyy-mm-dd' or yyyy-mm-dd HH:MM:SS"
        )
    return ts


def Fill_na(df):
    print('=== 补充缺失值 横向 同行业、时间')
    df['end_year'] = df.end.map(lambda x:x.year)
    df['end_month'] = df.end.map(lambda x:x.month)
    df['end_day'] = df.end.map(lambda x:x.day)
    df = df.dropna(subset=['end','industry'],axis=0)
    df.index=range(len(df))
    df['orig_index'] = df.index
    for number1 in range(len(df.columns)):
        df_na = df.loc[df.iloc[:, number1].isnull(),]
        if len(df_na)==0:
            continue
        df_na.index=range(len(df_na))
        for number2 in range(len(df_na)):
            l_na_variable = df_na.columns[df_na.iloc[number2, :].isnull()].tolist()
            df_ind = df.loc[(df.industry == df_na.industry[number2]) & (df.end_month == df_na.end_month[number2])&(df.end_year == df_na.end_year[number2]), l_na_variable]
            value = df_ind.apply(np.mean, 0)
            if sum(value.isnull()) > 0:
                value = df.loc[:, l_na_variable].apply(np.mean, 0)
            df.loc[df_na.orig_index[number2], l_na_variable] = np.array(value)
    df = df.drop(['orig_index','end_year','end_month','end_day','end','industry'], axis=1)
    return df


def check_contain_chinese(contents):
    zhPattern = re.compile(u'[\u4e00-\u9fa5]+')
    match = zhPattern.search(contents)
    if match:
        return True
    else:
        return False


def Check_x(xx):
    if type(xx) == str:
        if check_contain_chinese(xx):
            return xx
        else:
            return np.NaN
    elif type(xx) == float:
        return xx
    else:
        print('type of x ???')


def Create_variable_sponsor(Bond):
    Bond['has_sponsor'] = Bond.sponsor.map(lambda x: 0 if isinstance(x,float) else 1)
    return Bond

    '''
    list_1 = []
    for element in Bond.sponsor:
        
        if type(element) == str or float:
            list_1.append(Check_x(element))
        elif type(element) == pd.core.series.Series:
            if len(element) > 1:
                list_2 = []
                for xx in element:
                    if type(Check_x(xx)) == str:
                        list_2.append(Check_x(xx))
                if len(list_2) == 0:
                    list_1.append(np.NaN)
                elif len(list_2) == 1:
                    list_1.append(list_2[0])
                else:
                    print('Too much!')
            else:
                list_2.append(Check_x(element[0]))
        else:
            print('TYPE of x ???')
    Bond.sponsor = pd.Series(list_1)
    Bond['has_sponsor'] = -Bond.sponsor.isnull().map(int) + 1
    return Bond
    '''


def Count_issuer_history(df, number, all_cat):
    codee = df.code[number]
    end_date = df.loc[df.code == codee, 'end'][number]
    issuer = df.loc[df.code == codee, 'issuer'][number]
    All = all_cat.loc[all_cat.issuer == issuer, ['code', 'issuer', 'date_start', 'end', 'is_default']]
    default_history = sum((All.end < end_date) & (All.is_default == 1))
    already_history = sum((All.end < end_date) & (All.is_default == 0))
    now_history = sum((All.date_start < end_date) & (end_date < All.end) & (All.is_default == 0))
    cc = [codee, default_history, already_history, now_history]
    return cc


def Create_variable_issuer(df, all_cat):
    l_use = []
    for number in range(len(df.code)):
        cc = Count_issuer_history(df, number, all_cat)
        l_use.append(cc)
    df1 = pd.DataFrame(l_use)
    df1.columns = ['code', 'default_history', 'already_history', 'now_history']
    df2 = pd.merge(df1, df, on='code')
    return df2


def Split(s, symbol):
    result = [s]
    for i in symbol:
        median = []
        for z in map(lambda x: x.split(i), result):
            median.extend(z)
        result = median
    # 去除空字符串
    return [x for x in result if x]


def Calculate_underwiter_number(underwriter):
    if type(underwriter) == float:
        z = 0
    else:
        unders = Split(underwriter, '，,')
        z = len(unders)
    return z


def Count_history_underwirter(df, codee, all_cat, under_dict_code):
    end_date = np.array(df.loc[df.code == codee, 'end'])[0]
    under_default_number = []
    under_already_number = []
    under_default_ratio = []
    # under_now_number = []
    underwriter = np.array(df.loc[df.code == codee, 'underwriter'])[0]
    unders = Split(underwriter, '，,')
    for under in unders:
        dff = all_cat.loc[
            all_cat.code.isin(under_dict_code[under]), ['is_default', 'date_start', 'date_default', 'end']]
        default_number = sum((dff.is_default == 1) & (dff.end < end_date))
        already_number = sum((dff.is_default == 0) & (dff.end < end_date))
        # now_number = sum((dff.date_start<end_date) & (end_date<dff.date_end))
        default_ratio = default_number / (default_number + already_number)
        under_default_number.append(default_number)
        under_already_number.append(already_number)
        under_default_ratio.append(default_ratio)
        # under_now_number.append(now_number)
    cc = [codee, np.mean(under_default_number), np.mean(under_already_number), np.mean(under_default_ratio)]
    return cc


def Create_variable_underwriter(Bond, all_cat):
    Bond = Bond.dropna(subset=['underwriter'])
    under_dict_code = dict()
    for i in range(len(all_cat)):
        x = all_cat.underwriter[i]
        codee = all_cat.code[i]
        if type(x) == float: continue
        if '，' in x:
            unders = x.split('，')
        elif ',' in x:
            unders = x.split(',')
        else:
            unders = [x]
        for under in unders:
            if under not in under_dict_code.keys():
                under_dict_code[under] = list()
                under_dict_code[under].append(codee)
            else:
                under_dict_code[under].append(codee)

    issuer_history = []
    for codee in Bond.code:
        cc = Count_history_underwirter(Bond, codee, all_cat, under_dict_code)
        issuer_history.append(cc)
    df1 = pd.DataFrame(issuer_history)
    df1.columns = ['code', 'underwriter_default_number', 'underwriter_already_number', 'underwriter_default_ratio']
    df2 = pd.merge(df1, Bond, on='code')
    df2['underwriter_number'] = df2['underwriter'].map(Calculate_underwiter_number)
    return df2


def Get_dummy(train, test):
    train['id'] = range(len(train))
    test['id'] = range(len(train), len(train) + len(test))
    df_code = pd.concat([train[['id', 'code']], test[['id', 'code']]])
    train.drop('code', axis=1, inplace=True)
    test.drop('code', axis=1, inplace=True)
    test['is_test'] = 1
    train['is_test'] = 0
    df_all = pd.concat([train, test], axis=0)
    df_all1 = pd.get_dummies(df_all)
    df_all2 = pd.merge(df_all1, df_code, how='left', on='id')
    df_all3 = df_all2.drop(['id', 'is_test'], axis=1)
    train = df_all3.loc[df_all2.is_test == 0, :]
    test = df_all3.loc[df_all2.is_test == 1, :]
    return train, test


def Drop_category(df):
    l_use = []
    for num in range(len(df.columns)):
        if df.iloc[:, num].dtype not in [float, int, np.int64, np.float64]:
            l_use.append(df.columns[num])
    l_use.remove('code')
    df1 = df.drop(l_use, axis=1)
    return df1


def Fill_pad(df,column):
    df_fill = pd.DataFrame()
    df1 = df.dropna(subset=['time_report'])
    print('rows: ',len(np.array(df1[column].drop_duplicates())))
    for x in np.array(df1[column].drop_duplicates()):
        df0 = df1.loc[df1[column] == x, :].sort_values(axis=0, ascending=True, by='time_report').fillna(method='pad')
        df_fill = pd.concat([df_fill, df0], axis=0)
    return df_fill


def Get_result_dataframe(predict_1_all):
    df = pd.Series(predict_1_all)
    d = dict()
    for num in range(len(df)):
        prediction = df[num]
        if len(prediction) == 0:
            print('abc')
            continue
        date = df.index[num]
        for x in prediction:
            if x not in d.keys():
                d[x] = [date,1,[date]]
            else:
                date_0 = d[x][0]
                n = d[x][1]+1
                l = d[x][2]
                l.append(date)
                if date<date_0:
                    d[x] = [date, n, l]
                else:
                    d[x] = [date_0, n, l]
    df1 = pd.DataFrame(d)
    df2 = df1.T.reset_index()
    df2.columns = ['code','date_pred','pred_times','pred_history']
    return df2






# </editor-fold>

