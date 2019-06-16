# -*- coding: utf-8 -*-
"""

-------------------------------------------------
   File Name：        scores_trans
   Description :
   Author :           何友鑫
   Create date：      2018-10-23
   Latest version:    v1.0.0
-------------------------------------------------
   Change Log:
#-----------------------------------------------#
    v1.0.0            hyx        2018-10-23
    1.
#-----------------------------------------------#
-------------------------------------------------

"""
import pandas as pd
import math as m


if __name__ == '__main__':
    score = pd.read_excel('data_result/20181010_scores_20181010.xlsx')
    score['info_sigmoid'] = score['score_info'].map(lamboda x:1/(1+m.exp(-x)))