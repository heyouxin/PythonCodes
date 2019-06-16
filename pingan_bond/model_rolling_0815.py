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

import datetime
import time
import re
from imblearn.over_sampling import SMOTE
from sklearn.preprocessing import OneHotEncoder

import warnings
import random
warnings.filterwarnings("ignore")
# </editor-fold>


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
    df['orig_index'] = df.index
    for number in range(len(df.columns)):
        df_na = df.loc[df.iloc[:, number].isnull(),]
        df_na.index = range(len(df_na))
        for number in range(len(df_na)):
            l_na_variable = df_na.columns[df_na.iloc[number, :].isnull()].tolist()
            df_ind = df.loc[df.industry == df_na.industry[number], l_na_variable]
            value = df_ind.apply(np.mean, 0)
            if sum(value.isnull()) > 0:
                value = df.loc[:, l_na_variable].apply(np.mean, 0)
            df.loc[df_na.orig_index[number], l_na_variable] = value
    df = df.drop('orig_index', axis=1)
    return df


def check_contain_chinese(contents):
    zhPattern = re.compile(u'[\u4e00-\u9fa5]+')
    match = zhPattern.search(contents)
    if match:
        return True
    else:
        return False


def Calculate_mean(df, date_end_name):
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
    list_use = np.array(df.columns[~df.columns.isin(df_num.columns)]).tolist()
    list_use.append('code')
    df_cat = df.loc[:, list_use]
    df_cat = df_cat.drop_duplicates(subset='code', keep='first')
    # df_num = df_num.dropna()
    df_num = Fill_na(pd.merge(df_cat[['code', 'industry']], df_num, on='code'))
    df_num = df_num.drop('industry', axis=1)
    df = pd.merge(df_num, df_cat, how='left', on='code')
    return df


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
    global list_2
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


def Count_issuer_history(df, number, all_cat, time_now = pd.Timestamp):
    codee = df.code[number]
    end_date = df.loc[df.code == codee, 'date_end'][number]
    issuer = df.loc[df.code == codee, 'issuer'][number]
    All = all_cat.loc[all_cat.issuer == issuer, ['code', 'issuer', 'date_start', 'date_end', 'is_default']]
    default_history = sum((All.date_end < end_date) & (All.is_default == 1))
    already_history = sum((All.date_end < end_date) & (All.is_default == 0))
    now_history = sum((All.date_start < end_date) & (end_date < All.date_end) & (All.is_default == 0))
    cc = [codee, default_history, already_history, now_history]
    return cc


def Create_variable_issuer(df, all_cat, time_now):
    l_use = []
    for number in range(len(df.code)):
        cc = Count_issuer_history(df, number, all_cat, time_now)
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
    end_date = np.array(df.loc[df.code == codee, 'date_end'])[0]
    under_default_number = []
    under_already_number = []
    under_default_ratio = []
    # under_now_number = []
    underwriter = np.array(df.loc[df.code == codee, 'underwriter'])[0]
    unders = Split(underwriter, '，,')
    for under in unders:
        dff = all_cat.loc[
            all_cat.code.isin(under_dict_code[under]), ['is_default', 'date_start', 'date_default', 'date_end']]
        default_number = sum((dff.is_default == 1) & (dff.date_end < end_date))
        already_number = sum((dff.is_default == 0) & (dff.date_end < end_date))
        # now_number = sum((dff.date_start<end_date) & (end_date<dff.date_end))
        default_ratio = default_number / (default_number + already_number)
        under_default_number.append(default_number)
        under_already_number.append(already_number)
        under_default_ratio.append(default_ratio)
        # under_now_number.append(now_number)
    cc = [codee, np.mean(under_default_number), np.mean(under_already_number), np.mean(under_default_ratio)]
    return cc


def Create_variable_underwriter(Bond, all_cat):
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


def Revise_variables(df, all_cat, time_now):
    df = Create_variable_sponsor(df)
    df = Create_variable_issuer(df, all_cat, time_now)
    df = Create_variable_underwriter(df, all_cat)
    df = df.drop(['bond_type_wind_2', 'balance_100million', 'issuer', 'event',
                  'industry_wind', 'rate_history', 'sponsor', 'time_report',
                  'rate_bond_lastest', 'rate_comp_lastest', 'underwriter',
                  'name', 'date_end', 'date_start', 'date_default'], axis=1)
    df = df.replace('-', 'NA')
    df = df.replace('', 'NA')
    df.underwriter_default_number = df.underwriter_default_number.fillna(0)
    df.underwriter_already_number = df.underwriter_already_number.fillna(0)
    df.underwriter_default_ratio = df.underwriter_default_ratio.fillna(0)
    # df.apply(lambda x: sum(x.isnull()),0)
    df = df.fillna('NA')
    for num in range(len(df.columns)):
        if df.iloc[:, num].dtype == object:
            if check_contain_chinese(str(df.iloc[:, 33].astype('category').cat.categories)):
                df.iloc[:, num] = df.iloc[:, num].map(Check_x)
            try:
                df.iloc[:, num] = df.iloc[:, num].astype('category')
            except:
                continue
    return df


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


def Data_preparation(already, default, time_now):
    print('Begin data preparation')
    cat_already = np.array(already.columns[~already.columns.isin(already.groupby('code').mean().columns)])
    cat_default = np.array(default.columns[~default.columns.isin(default.groupby('code').mean().columns)])
    df1 = already[cat_already].drop_duplicates(subset='code')
    df2 = default[cat_default].drop_duplicates(subset='code')
    df2['date_end'] = df2.date_default
    df2 = df2.drop('date_default', axis=1)
    df1['is_default'] = 0
    df2['is_default'] = 1
    all_cat = pd.concat([df1.set_index('code'), df2.set_index('code')], join='outer', axis=0)
    all_cat = all_cat.reset_index().rename(columns={'index': 'code'})
    global time_default
    train_already = already.loc[already.date_end < time_now,]
    train_default = default.loc[default.date_default < time_now,]
    test = pd.concat([already.loc[(already.date_end > time_now) & (time_now > already.date_start),],
                      default.loc[(default.date_default > time_now) & (time_now > default.date_start),]], axis=0)
    print('  Begin to calculate mean values of train data set')
    train_already1 = Calculate_mean(train_already, 'date_end')
    train_already1['is_default'] = 0
    train_default1 = Calculate_mean(train_default, 'date_default')
    train_default1['is_default'] = 1
    train_default1['date_end'] = train_default1['date_default']
    train = pd.concat([train_already1, train_default1], axis=0)
    train.index = range(len(train))
    print('  Begin to calculate mean values of test data set')
    test = Calculate_mean(test, 'time_report')
    test['is_default'] = -test.date_default.isnull().map(int) + 1
    test['date_end'] = test['time_report']
    print('  Begin to Revise variables of train data set')
    df_train_1 = Revise_variables(train, all_cat, time_now)
    print('  Begin to Revise variables of test data set')
    df_test_1 = Revise_variables(test, all_cat, time_now)
    ## df_train_2,df_test_2 = Get_dummy(df_train_1,df_test_1)
    #print('  Begin to drop category variables')
    #df_train_2 = Drop_category(df_train_1)
    #df_test_2 = Drop_category(df_test_1)
    return df_train_1, df_test_1, all_cat

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

def DataSplit():
    print('Reading raw data.')
    Already = pd.read_excel("data/Already_quarter_0807_1.xlsx")
    Default = pd.read_excel("data/Default_quarter_0807_1.xlsx")

    global T_start, number_start, number_end, time_default, all_cat
    # noinspection PyRedeclaration
    T_start = pd.Timestamp('20170701')
    # sum(Default.drop_duplicates(subset='code',keep='first').date_default<pd.Timestamp('20170101')) = 58
    # 20170101: 55 train_default
    # 20170401: 62 train_default
    # 20170701: 68 train_default
    # noinspection PyRedeclaration
    number_start = 2
    # noinspection PyRedeclaration
    number_end = 0
    seed = 123
    delta_month = 1
    over_ratio = 1 / 1
    split_ratio = 0.8
    time_default = Default[['code', 'date_start', 'date_default']].drop_duplicates('code')

    all_f1, all_recall, all_precision, all_auc, all_acc, all_score = [], [], [], [], [], []
    predict_1_all = dict()
    l_predict_1_all = list()
    valid_score_all = dict()

    t = T_start
    # t_end = T_start + relativedelta(months=9)
    t_end = pd.Timestamp('20180701')  # str(datetime.date.today()))
    num = 0

    Df_train, Df_test_final, all_cat = Data_preparation(Already, Default, t)

    return  (Df_train,Df_test_final,all_cat)
    '''
    # <editor-fold desc="Back test">
    while t < t_end:
        seed = 10 * num
        print("Today is %s" % t)
        Df_train, Df_test_final, all_cat = Data_preparation(Already, Default, t)

        t = t + relativedelta(months=delta_month)
        num += 1
        print('======================================')
    '''


(data_train,data_test,cat_all)=DataSplit()

