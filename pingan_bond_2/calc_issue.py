# -*- coding: utf-8 -*-
"""

-------------------------------------------------
   File Name：        calc_issue
   Description :
   Author :           何友鑫
   Create date：      2018-11-01
   Latest version:    v1.0.0
-------------------------------------------------
   Change Log:
#-----------------------------------------------#
    v1.0.0            hyx        2018-11-01
    1.
#-----------------------------------------------#
-------------------------------------------------

"""
from datetime import datetime
import pandas as pd


def getDate():
    date = pd.date_range('03/08/2018', '26/10/2018', freq='W-FRI')
    date_Fri = list(date.strftime('%Y-%m-%d'))
    return (date_Fri)

if __name__ == '__main__':
    bond_all = pd.read_excel('data_sql/bond_info.xlsx')
    comp_all = pd.read_excel('data_sql/comp_info.xlsx')

    bond_all = pd.merge(bond_all,comp_all,how='left',left_on='issuer',right_on='issuer')

    date_list = getDate()

    bond_all.date_start = bond_all.date_start.map(lambda x:str(x))

    amount = []
    aver_term = []
    aver_rate = []
    calc_date = []
    group_name = []
    classify_name = []

    for i in range(1,len(date_list)):
        #i = 1
        bond_temp = bond_all.loc[(bond_all['date_start'] > date_list[i-1]) & (bond_all['date_start']<=date_list[i]),:]
        for g_name in ['industry','province']:
            for name,group in bond_temp.groupby(g_name):
                #print(industry_name)
                classify_name.append(g_name)

                group['total_year'] = 0.0
                group['total_year'] = group.total_100million * group.year

                group['total_rate'] = 0.0
                group['total_rate'] = group.total_100million * group.coupon_rate

                group = group.fillna(0.0)
                group_name.append(name)
                try:
                    aver_t = sum(group['total_year']) / sum(group['total_100million'])
                    aver_term.append(aver_t)
                    aver_r = sum(group['total_rate']) / sum(group['total_100million'])
                    aver_rate.append(aver_r)
                    amount.append(sum(group['total_100million']))
                    calc_date.append(date_list[i])
                except:
                    continue



'''
    huan_bi_term = []
    huan_bi_rate = []

    for j in range(0,len(aver_term)):
        try:
            huan_bi_term.append(aver_term[j]/aver_term[j-1]-1)
            huan_bi_rate.append(aver_rate[j] / aver_rate[j-1] - 1)
        except:
            huan_bi_term.append(0)
            huan_bi_rate.append(0)

    tong_bi_term = []
    tong_bi_rate = []
    for j in range(0, len(aver_term)):
        try:
            tong_bi_term.append(aver_term[j] / aver_term[j - 4] - 1)
            tong_bi_rate.append(aver_rate[j] / aver_rate[j - 4] - 1)
        except:
            tong_bi_term.append(0)
            tong_bi_rate.append(0)
    #huan_bi_term.append(0)
    #huan_bi_rate.append(0)
'''
    d={'date':calc_date,'aver_term':aver_term,'aver_rate':aver_rate,
       'amount':amount,'group':group_name,'classify':classify_name}
        '''
       'huan_bi_term':huan_bi_term,'huan_bi_rate':huan_bi_rate,
       'tong_bi_term':tong_bi_term,'tong_bi_rate':tong_bi_rate}
        '''
    pd.DataFrame(d).to_excel('term_and_rate.xlsx',index=False,encoding='utf8')

    term_rate_amount = pd.read_excel('term_rate_amount.xlsx')
    '''
    huan_bi_amount = []
    huan_bi_rate = []
    tong_bi_amount = []
    tong_bi_rate = []
    '''
    term_rate_amount['huan_bi_amount'] = ''
    term_rate_amount['huan_bi_rate'] = ''

    term_rate_amount['tong_bi_amount'] = ''
    term_rate_amount['tong_bi_rate'] = ''

    reg = pd.DataFrame()
    for n,g in term_rate_amount.groupby('group'):
        g = g.reset_index().drop('index',1)
        for i in range(1,len(g)):
            g.loc[i,'huan_bi_amount'] = g.loc[i,'amount']/g.loc[i-1,'amount']-1
            g.loc[i, 'huan_bi_rate'] = g.loc[i, 'aver_rate'] / g.loc[i - 1, 'aver_rate'] - 1
            try:
                g.loc[i,'tong_bi_amount'] = g.loc[i,'amount']/g.loc[i-4,'amount']-1
                g.loc[i, 'tong_bi_rate'] = g.loc[i, 'aver_rate'] / g.loc[i - 4, 'aver_rate'] - 1
            except:
                pass
        reg = pd.concat([reg,g]).reset_index().drop('index',1).sort_values('date')

reg.to_excel('term_amount_tong_huan.xlsx',index=False,encoding='utf8')


huan_bi_term = g.