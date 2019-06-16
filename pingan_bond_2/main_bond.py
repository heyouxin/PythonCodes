# -*- coding: utf-8 -*-
"""

-------------------------------------------------
   File Name：        main_bond
   Description :      债券违约预警主程序
   Author :           何友鑫
   Create date：      2018-10-10
   Latest version:    v1.0.0
-------------------------------------------------
   Change Log:
#-----------------------------------------------#
    v1.0.0            hyx        2018-10-10
    1.把入口主程序从model_alert类 单独分离出来
    2.def runModel 分为测试和非测试，测试条件下，直接读data_train data_test,不需要执行model_rolling
#-----------------------------------------------#
-------------------------------------------------

"""



import pandas as pd
import model_rolling
from model_alert import ModelAlert
import datetime
from  bond_ranking import  bondRanking

def runModel(is_test=0):
    if is_test == 0:
        # date_list=['20170401','20170701','20171001','20180101','20180401','20180701']
        dict_filename = {'all_code': 'data_sql/code_0919.xlsx',
                         'all_issuer': 'data_sql/issuer_0919.xlsx',
                         'all_bond_info': 'data_sql/bond_info.xlsx',
                         'all_comp_info': 'data_sql/comp_info.xlsx',
                         'all_finance': 'data_sql/finance.xlsx',
                         'all_default': 'data_sql/default.xlsx',
                         'filename_macro': 'data_sql/macro.xlsx',
                         'filename_capm': 'data_sql/industry_capm.xlsx',
                         'filename_zs': 'data_sql/industry_yz_yjzs.xlsx'}

        dict_var = {'number_start': 2, 'number_end': 0}
        date_list = ['20181024']

        # date_list = ['20180101','20180401', '20180701']
        Raw_data = model_rolling.RawData(dict_filename=dict_filename, dict_var=dict_var)

        for date in date_list:
            print(date)
            Clean_data = model_rolling.CleanData(Raw_data=Raw_data, date_split=date, dict_var=dict_var)
            Clean_data.DataPreparation()
            t_end = datetime.datetime.now()

            # Clean_data.data_train.to_excel('data_train.xlsx',index=False,encoding='utf8')

            # Clean_data.data_test.to_excel('data_test.xlsx',index=False,encoding='utf8')

            model_alert = ModelAlert(data_train=Clean_data.data_train, data_test=Clean_data.data_test, is_rolling=1)
            score = model_alert.RunRolling(date)

            info = pd.read_excel(Raw_data.dict_filename['all_bond_info'])
            df_score = pd.merge(score, info, how='left', on='code')

            today = str(datetime.datetime.now())[:10].replace('-', '')
            filename = 'data_result/' + today + '_scores_' + date + '.xlsx'
            df_score.to_excel(filename, index=False, encoding='utf8')

    else:
        dict_filename = {'all_code': 'data_sql/code_0919.xlsx',
                         'all_issuer': 'data_sql/issuer_0919.xlsx',
                         'all_bond_info': 'data_sql/bond_info.xlsx',
                         'all_comp_info': 'data_sql/comp_info.xlsx',
                         'all_finance': 'data_sql/finance.xlsx',
                         'all_default': 'data_sql/default.xlsx',
                         'filename_macro': 'data_sql/macro.xlsx',
                         'filename_capm': 'data_sql/industry_capm_0919.xlsx',
                         'filename_zs': 'data_sql/industry_yz_yjzs_0919.xlsx'}
        data_train = pd.read_excel('data_train.xlsx')
        data_test = pd.read_excel('data_test.xlsx')
        model_alert = ModelAlert(data_train=data_train, data_test=data_test, is_rolling=1)
        date = '20180701'
        score = model_alert.RunRolling(date)
        info = pd.read_excel(dict_filename['all_bond_info'])
        df_score = pd.merge(score, info, how='left', on='code')
        today = str(datetime.datetime.now())[:10].replace('-', '')
        filename = 'data_result/' + today + '_scores_' + date + '.xlsx'
        df_score.to_excel(filename, index=False, encoding='utf8')


    bondRanking(filename)


if __name__ == "__main__":
    t_start = datetime.datetime.now()
    runModel(1)
    t_end = datetime.datetime.now()
    print('总耗时：',t_end-t_start)