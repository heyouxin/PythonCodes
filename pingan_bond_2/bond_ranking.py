# -*- coding: utf-8 -*-
"""

-------------------------------------------------
   File Name：        bond_ranking
   Description :      从模型结果为负分的债券数据挑出违约机率大的债券
   Author :           何友鑫
   Create date：      2018-10-12
   Latest version:    v1.1.0
-------------------------------------------------
   Change Log:
#-----------------------------------------------#
    v1.1.0            hyx        2018-10-24
    1.基础分除以6，分配到各个纬度。作为各纬度的基准分。
    v1.0.0            hyx        2018-10-12
    1.先把模型结果的小于0，存在于违约案例库的取出来。
    2.再把这些公司名称在Pg库舆情中查看它最近10条记录的情感评分。为负数的取出来

#-----------------------------------------------#
-------------------------------------------------

"""

import pandas as pd

import datetime



def bondRanking(file_model_result):
       bond_default = pd.read_excel('raw_data/违约债券报表.xlsx')
       issuer_default = bond_default['发行人'].drop_duplicates()
       model_result = pd.read_excel(file_model_result)

       #step 1: 得分小于0 且 发行主体在违约案例库里的公司 且 到期日在2020年之前的  标记为1 展示前十条记录
       model_result['predict_default'] = 0
       model_result['date_end']=model_result['date_end'].map(lambda x:str(x))
       model_result.loc[(model_result['total_score']<0) & (model_result['issuer'].isin(issuer_default)) & (model_result['date_end'] < '2020-01-01')
       ,'predict_default'] = 1

       #step 2: 得分小于0 风险等级为高
       model_result['rating'] = '中'
       model_result.loc[model_result['total_score'] < 0,'rating']='高'
       low_start = int(len(model_result[model_result['rating'] == '高'])+(len(model_result)-len(model_result[model_result['rating'] == '高']))/2)
       model_result.loc[low_start:len(model_result)-1,'rating'] = '低'

       #step3: 标记健康债券 风险等级为低 且 到期日在2020年之前的  标记为2 展示最后十条记录
       model_result.loc[(model_result['rating'] == '低') & (model_result['date_end'] < '2020-01-01'),'predict_default'] = 2

       #step4: 取部分展示列
       #model_result.columns

       model_result_2 = model_result

       #v1.1
       base_point = int(model_result_2.score_basepoint[0]/6)

       model_result_2['score_info'] = model_result_2['score_info']+base_point
       model_result_2['score_macro'] = model_result_2['score_macro']+base_point
       model_result_2['score_industry'] = model_result_2['score_industry']+base_point
       model_result_2['score_finance'] = model_result_2['score_finance']+base_point
       model_result_2['score_emotion'] = base_point
       model_result_2['score_law'] = base_point


       model_result_2['total_score'] = model_result_2['score_info']+model_result_2['score_macro']+\
                                       model_result_2['score_industry']+model_result_2['score_finance']+model_result_2['score_emotion']+\
                                       model_result_2['score_law']




       model_result_2 = model_result_2[['code', 'is_default','score_basepoint',
              'score_info', 'score_macro', 'score_industry', 'score_finance','score_finance','score_emotion',
              'score_law',
              'total_score',  'date', 'bond_type_wind_1',
              'bond_type_wind_2', 'coupon_rate', 'date_end', 'date_start', 'exchange',
              'issuer', 'name', 'rate_bond_issue', 'rate_comp_issue', 'sponsor',
              'total_100million', 'underwriter', 'year', 'predict_default', 'rating']]


       model_result_2.to_excel('data_result/scores_rolling.xlsx',index=False,encoding='utf8')

if __name__ == '__main__':
       file_model_result = 'data_result/20181010_scores_20181010.xlsx'
       bondRanking(file_model_result)
