# -*- coding: utf-8 -*-
"""

-------------------------------------------------
   File Name：        取财务数据
   Description :
   Author :           何友鑫
   date：             2018-09-05
   latest version:    v1.0.0
-------------------------------------------------
   Change Log:
    v1.0.0            hyx        2018-09-05
    1.
-------------------------------------------------

"""


#取动态财务数据
    w.start()
    df_all=pd.DataFrame()
    for i in range(len(code_issuer['code'])):
    #for i in range(0,3):
        wsd_data =w.wsd(code_issuer.loc[i,'code'],
              "roe,wgsd_ebit_oper,tot_oper_rev,yoy_tr,debttoassets,yoy_equity,quick,invturn,arturn,assetsturn1,roa,wgsd_oper_cf,tot_assets,nptocostexpense,caturn,cashtocurrentdebt,yoyop,latestissurercreditrating",
              "2000-01-01", "2018-09-04", "unit=1;rptType=1;currencyType=;Period=Q")
        df = pd.DataFrame(wsd_data.Data, index=wsd_data.Fields, columns=wsd_data.Times)
        df = df.T
        df['ISSUER']=code_issuer.loc[i,'ISSUERUPDATED']
        df['code']=code_issuer.loc[i,'code']
        df_all=pd.concat([df_all,df])

    df_all = df_all.reset_index().rename(columns={'index': 'time_report'})
    month= df_all['time_report'][len(df_all['time_report'])-1].month
    day= df_all['time_report'][len(df_all['time_report'])-1].day
    month_day= str(month)+str(day)
    if month_day not in ['1231','331','630','930']:
        df_all= df_all.loc[0:(len(df_all)-2),:]

    df_all['ID']=df_all['ISSUER'].map(lambda x:str(x))+df_all['time_report'].map(lambda x:str(x))


    #调整列的顺序
    issuer = df_all['ISSUER']
    df_all.drop(labels=['ISSUER'], axis=1, inplace=True)
    df_all.insert(0, 'ISSUER', issuer)


    ID = df_all['ID']
    df_all.drop(labels=['ID'], axis=1, inplace=True)
    df_all.insert(0, 'ID', ID)
