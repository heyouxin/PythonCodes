# -*- coding: utf-8 -*-
"""

-------------------------------------------------
   File Name：        energy
   Description :
   Author :           何友鑫
   Create date：      2018-12-11
   Latest version:    v1.0.0
-------------------------------------------------
   Change Log:
#-----------------------------------------------#
    v1.0.0            hyx        2018-12-11
    1.
#-----------------------------------------------#
-------------------------------------------------

"""
import pandas as pd


if __name__ == '__main__':

    #40个子行业分类 单位产值能耗   单位：吨标准煤/亿元
    intensity = pd.read_excel('Intensity.xlsx')
    indust = intensity.loc[:,'行业']
    intensity = intensity.drop(['行业','行业.1'],1)
    #round(float(str(x).strip().replace(' ', '')), 1)
    try:
        intensity = intensity.applymap(lambda x: float(str(x).strip().replace('．','.').replace(' ','')))
    except:
        pass

    for i in range(0,7):
        #单位：吨/亿元
        intensity['inten_'+str(intensity.columns[i])] = intensity.iloc[:,i+7]/intensity.iloc[:,i]

    intensity_df = intensity.iloc[:,14:intensity.shape[1]]
    intensity_df = pd.concat([indust,intensity_df],1)


    #========================================================================

    '''
    right_classify = []
    indust_claaify_map.ix[860:867,4]
    #农、林、牧、渔、水利业
    right_classify.append(','.join(list(indust_claaify_map.ix[0:824,4].dropna().map(lambda x: "'"+str(x)+"'"))))
    #煤炭开采和洗选业
    right_classify.append(','.join(list(indust_claaify_map.ix[824:859,4].dropna().map(lambda x: "'" + str(x) + "'"))))
    #石油和天然气开采业
    right_classify.append(','.join(list(indust_claaify_map.ix[860:867, 4].dropna().map(lambda x: "'" + str(x) + "'"))))
    #黑色金属矿采选业
    right_classify.append(','.join(list(indust_claaify_map.ix[867:900, 4].dropna().map(lambda x: "'" + str(x) + "'"))))
    '''

    # 国民行业对应国际专利分类
    indust_claaify_map = pd.read_excel('国际专利分类与国民行业分类对照表.xlsx')

    #批发和零售业  交通运输、仓储和邮政业 专利匹配不到  专利数为0#

    indust_index = list(indust_claaify_map.loc[indust_claaify_map['国民经济行业名称'].isin(indust[0:len(indust)]), :].index)
    right_classify = []
    for i in range(len(indust_index)-1):
        cat_1 = set(indust_claaify_map.ix[indust_index[i]:indust_index[i+1], 4].dropna().map(lambda x: "'" + str(x) + "'"))
        cat_2 = set(indust_claaify_map.ix[indust_index[i]:indust_index[i + 1], 3].dropna().map(lambda x: "'" + str(x) + "'"))
        right_classify.append(','.join(list(cat_1 | cat_2)))

    intensity_right = pd.concat([intensity_df,pd.DataFrame(right_classify)],1)

    intensity_right = intensity_right.rename(columns={0:'category'})

    intensity_right.to_excel('intensity_right.xlsx',index=False,encoding='utf8')


    #=======================================================

    intensity_right = pd.read_excel('intensity_right.xlsx')
