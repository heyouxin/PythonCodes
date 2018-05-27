#!/usr/bin/env python2
# -*- coding: utf-8 -*-


from __future__ import division, unicode_literals
import pymysql
import pymssql
import pandas as pd
from sqlalchemy import create_engine
import re
import numpy as np
import statsmodels.api as sm
from scipy.stats import *
from sklearn import preprocessing
import datetime
import re

gdb = ''
ghost = ''
guser = ''
gpassword = ''
gdatabase = ''
conn = ''
engine = ''



def set_sql(gdb, ghost, guser, gpassword, gdatabase):
    global db, host, user, password, database, engine, conn
    db = gdb
    host = ghost
    user = guser
    password = gpassword
    database = gdatabase
    engine = set_engine()
    conn = set_conn()


def set_engine():
    global engine
    try:
        engine.close()
    except:
        pass
    if db.lower() == 'mysql':
        engine = create_engine('mysql+pymysql://' + user + ':' + password + '@' + host + '/' + database)
    if db.lower() == 'mssql':
        engine = create_engine('mssql+pyodbc://' + user + ':' + password + '@' + host + '/' + database)
    return engine



def set_conn():
    if db.lower() == 'mysql':
        conn = pymysql.connect(host=host, user=user, password=password, db=database, charset='utf8')
    if db.lower() == 'mssql':
        conn = pymssql.connect(host=host, user=user, password=password, database=database, charset="utf8")
    return conn


def execute_sql(sql_str, conn):
    cursor = conn.cursor()
    cursor.execute(sql_str)
    conn.commit()



def search_sql(sql_str):
    s = pd.read_sql(sql_str, conn)
    return s



def to_sql(df, table_name):
    try:
        df.to_sql(table_name, engine, if_exists='append')
    except IOError as e:
        print('to sql error! \n ' + e)


###行业层面
set_sql('mysql', '172.16.8.184', 'qc_data', 'wisesoe.qc', 'qc_data')
data = search_sql('select * from induindextest')[:-149]
data['date'] = map(unicode,list(data['date']))
dates = search_sql('select * from dates')
macro = search_sql('select * from macro')
macro = pd.merge(macro,dates,on='date')
epu = search_sql('select * from EPU')[1:]
epu.columns = ['year','month','epu']
epu['epu'] = map(float,list(epu['epu']))
ym = []
for i in range(len(epu)):
    year = int(epu.iloc[i]['year'])
    month = int(epu.iloc[i]['month'])
    if month<10:
        ym.append(str(year)+'0'+str(month))
    else:
        ym.append(str(year)+str(month))
epu['ym'] = ym
del epu['year']
del epu['month']
index = search_sql('select ret,date from zhishu where qtid="000300.SH" and date>="2011-01-01"')
index['date'] = map(str,list(index['date']))
index = pd.merge(index,dates,on='date')
data = pd.merge(data,dates,on='date')
data = pd.merge(data,epu)
fin =pd.merge(data,index,on='date')
yujing = macro[240:-4]['yujing']
yizhi = macro[240:-4]['yizhi']
betas = []
for i in fin.groupby('indu').groups.keys():
    for j in range(21,80):
        hangye = list(fin.groupby('indu').get_group(i).groupby('ym_x')['ret_x'].sum().values)[j-20:j]
        zhishu = fin.groupby('indu').get_group(i).groupby('ym_x')['ret_y'].sum().values[j-20:j]
        bodong = fin.groupby('indu').get_group(i).groupby('ym_x')['ret_y'].std().values[j-20:j]
        bodong = list(pd.Series(bodong).fillna(pd.Series(bodong).mean()))
        epuu = fin.groupby('indu').get_group(i).groupby('ym_x')['epu'].mean().values[j-20:j]
        yj = list(yujing)[j-20:j]
        yz = list(yizhi)[j-20:j]
        #smb = finn.groupby('indu').get_group(i).groupby('ym_x')['SMB'].sum().values
        #hml = finn.groupby('indu').get_group(i).groupby('ym_x')['HML'].sum().values
        xs = np.column_stack([zhishu,bodong,np.log(epuu),yj,yz])
        kong = [i,fin['ym_x'].unique()[j+1]]
        model = sm.OLS(hangye,sm.add_constant(xs)).fit(method='qr')
        kong.append(model.params[0])
        kong.append(model.params[1])
        kong.append(model.resid.std())
        kong.append(np.array(hangye[:-3]).sum()-np.array(zhishu[:-3]).sum())
        kong.append(np.array(hangye[:-6]).sum()-np.array(zhishu[:-6]).sum())
        kong.append(np.array(hangye[:-9]).sum()-np.array(zhishu[:-9]).sum())
        kong.append(np.array(hangye[:-12]).sum()-np.array(zhishu[:-12]).sum())
        kong.append(abs(pd.Series(bodong).std()*model.params[2]))
        kong.append(abs(epuu.std()*model.params[3]))
        kong.append(abs(np.array(yj).std()*model.params[4]))
        kong.append(abs(np.array(yz).std()*model.params[5]))
        betas.append(kong)


hy ={'33':'制造业','34':'制造业','30':'制造业','25':'制造业','26':'制造业','60':'制造业','28':'制造业','27':'制造业',
     '22':'制造业','35':'卫生和社会工作','23':'建筑业','24':'建筑业','42':'房地产业','31':'批发和零售业','36':'批发和零售业',
    '63':'文化、体育和娱乐业','20':'电力、热力、燃气及水生产和供应业','40':'金融业','41':'金融业','11':'采矿业','12':'采矿业',
    '70':'综合','32':'住宿和餐饮业','50':'交通运输、仓储和邮政业','60':'信息传输、软件和信息技术服务业',
    '61':'信息传输、软件和信息技术服务业','62':'信息传输、软件和信息技术服务业','37':'农、林、牧、渔业','10':'采矿业','21':'采矿业'}


para = pd.DataFrame(betas)
para[0] = para[0].map(hy)
para.columns=['code','ym','alpha','beta','idio','mom1','mom2','mom3','mom4','ecbd2','ecep2','ecyj2','ecyz2']


adds = []
for i in para.groupby('code').groups.keys():
    ki= para.groupby('code').get_group(i).groupby('ym').mean()
    ki['industry_name'] = np.repeat(i,len(ki))
    adds.append(ki)

adds = pd.concat(adds)


trade=search_sql('select * from tradercomponent')
datas = search_sql('select * from industry where field3 = "2017/1/4"')
indu = pd.DataFrame({'qtid':datas['field2'],'indu':datas['field4']})
def trans(x):
    if list(x)[0]=='6':
        kk = x+'.SH'
    else:
        kk = x+'.SZ'
    return kk
trade['qtid']=map(trans,list(trade['code']))
trades = pd.merge(indu,trade,on='qtid')
grouped = trades.groupby('date')
cons = []
for i in range(len(grouped.groups.keys())):
    ev = grouped.get_group(grouped.groups.keys()[i]).groupby('indu')['ratio1'].mean()
    every = pd.DataFrame({'indu':ev.index,'ratio1':ev.values,'date':np.repeat(grouped.groups.keys()[i],len(ev))})
    cons.append(every)
trades = pd.concat(cons).sort_values('date')
trades.to_csv('~/trade.csv')
trades = pd.read_csv('~/trade.csv')
trades['indu'] = map(str,list(trades['indu']))
trades['industry_name'] = trades['indu'].map(hy)
trades=pd.merge(trades,dates,on='date')
trgr = trades.groupby('ym')
trcon = []
for i in trgr.groups.keys():
    trcon.append(pd.DataFrame({'ratio1':trgr.get_group(i).groupby('industry_name')['ratio1'].mean().values,
                               'industry_name':trgr.get_group(i).groupby('industry_name')['ratio1'].mean().index,
                             'ym':np.repeat(i,len(trgr.get_group(i).groupby('industry_name')['ratio1'].mean()))}))
tr = pd.concat(trcon)



testt = search_sql('select ret,open,close,qtid,date,hi from marketData')
tes = pd.merge(testt,indu,on='qtid')
tes['date'] = map(str,list(tes['date']))
tess = pd.merge(dates,tes,on='date')
tessgr = tess.groupby('ym')
yzbcon = []
for i in tessgr.groups.keys():
    ever = tessgr.get_group(i)
    size = pd.DataFrame({'number':ever.groupby('indu').size().values,'indu':ever.groupby('indu').size().index,})
    kk = ever[(ever['open']==ever['close'])
               & (ever['open']==ever['hi']) & (ever['ret']>=0.092)].groupby('indu')['ret'].sum()/0.09
    kks =pd.DataFrame({'indu':kk.index,'yzb':map(int,kk.values)})
    pro = pd.merge(kks,size,how='outer').fillna(0)
    yzbcon.append(pd.DataFrame({'indu':pro['indu'],'yzb':pro['yzb']/pro['number'],'ym':np.repeat(i,len(pro))}))
zrztcon = []
for i in tessgr.groups.keys():
    ever = tessgr.get_group(i)
    size = pd.DataFrame({'number':ever.groupby('indu').size().values,'indu':ever.groupby('indu').size().index,})
    kk = ever[(ever['open']!=ever['close'])
               & (ever['close']==ever['hi']) & (ever['ret']>=0.092)].groupby('indu')['ret'].sum()/0.09
    kks =pd.DataFrame({'indu':kk.index,'zrzt':map(int,kk.values)})
    pro = pd.merge(kks,size,how='outer').fillna(0)
    zrztcon.append(pd.DataFrame({'indu':pro['indu'],'zrzt':pro['zrzt']/pro['number'],'ym':np.repeat(i,len(pro))}))
emo1 = pd.merge(pd.concat(yzbcon),pd.concat(zrztcon),on=['indu','ym'])
tessgr2 = tess.groupby('qtid')
import warnings
warnings.filterwarnings("ignore")
dk = []
for i in range(len(tessgr2.groups.keys())):
    tf = tessgr2.get_group(tessgr2.groups.keys()[i])
    tf['mv60'] = tf['close'].rolling(60).mean()
    tf['mv30'] = tf['close'].rolling(30).mean()
    tf['mv20'] = tf['close'].rolling(20).mean()
    tf['mv10'] = tf['close'].rolling(10).mean()
    tf['mv60df'] = tf['mv60'].diff()
    tf['mv30df'] = tf['mv30'].diff()
    tf['mv20df'] = tf['mv20'].diff()
    tf['mv10df'] = tf['mv10'].diff()
    tf['duotou'] = map(float,(tf['mv10']>tf['mv30']) & (tf['mv30']>tf['mv60']) & (tf['mv30df']>0) & (tf['mv60df']>0))
    tf['kongtou'] = map(float,(tf['mv10']<tf['mv30']) & (tf['mv30']<tf['mv60']) & (tf['mv30df']<0) & (tf['mv60df']<0))
    dk.append(tf)


rational = search_sql('select * from rational')
def trans(x):
    if list(x)[0]=='6':
        kk = x+'.SH'
    else:
        kk = x+'.SZ'
    return kk
datas = search_sql('select * from industry where field3 = "2017/1/4"')
indu = pd.DataFrame({'qtid':datas['field2'],'indu':datas['field4']})
rational['qtid'] = map(trans,list(rational['code']))
ras = pd.merge(rational,indu)
rass =pd.merge(ras,dates,on='date')
ragr = rass.groupby('ym')
rascon = []
for i in ragr.groups.keys():
    changemean = ragr.get_group(i).groupby('indu')['beta'].mean()
    changestd = ragr.get_group(i).groupby('indu')['beta'].std()
    changeskew = ragr.get_group(i).groupby('indu')['beta'].skew()
    rascon.append(pd.DataFrame({'cmean':changemean.values,'cstd':changestd.values,
                 'cskew':changeskew.values,'indu':changemean.index,'ym':np.repeat(i,len(changemean))}))
rationals = pd.concat(rascon)
rationals['industry_name'] = rationals['indu'].map(hy)

'''
adds['ym'] = adds.index
add2 = []
for i in range(len(fik)):
    every = fik.iloc[i]
    start,end = every['ym_x'],every['ym_y']
    indu = every['industry_name']
    ek = adds[adds['industry_name']==indu]
    add2.append(ek[(ek['ym']>=start) & (ek['ym']<=end)].mean())

'''


###宏观层面
interest = search_sql('select * from intrate where maturity in (1,2,3,5,7,10,15,20)')
grrk = pd.merge(interest,dates,on='date')
grr = pd.merge(interest,dates,on='date').groupby('ym')
grp = []
for i in grr.groups.keys():
    grp.append(list(grr.get_group(i).groupby('maturity')['rate'].mean().sort_index().values))
tra = grrk[(grrk['date']>='2011-01-01') & (grrk['date']<='2017-09-01')]
grp2 = []
days = []
for i in tra.groupby('ym').groups.keys():
    grp2.append(list(grr.get_group(i).groupby('maturity')['rate'].mean().sort_index().values))
    days.append(i)
from sklearn.decomposition import PCA
model = PCA(n_components=3)
model.fit(np.array(pd.DataFrame(grp).fillna(0)))
#print model.explained_variance_ratio_
inter = pd.DataFrame(model.transform(pd.DataFrame(grp2).fillna(0)))
inter['ym'] = days
inter = inter.sort_values('ym')
inter.columns=['f1','f2','f3','ym']
termsp1 = np.array(interest[interest['maturity']=='10.0']['rate'])-np.array(interest[interest['maturity']=='5.0']['rate'])
termsp2 = np.array(interest[interest['maturity']=='10.0']['rate'])-np.array(interest[interest['maturity']=='1.0']['rate'])
termsp3 = np.array(interest[interest['maturity']=='20.0']['rate'])-np.array(interest[interest['maturity']=='10.0']['rate'])
termsp = pd.DataFrame([termsp1,termsp2,termsp3]).T
termsp['date'] = list(interest[interest['maturity']=='10.0']['date'])
termsp = termsp[(termsp['date']>='2011-01-01') & (termsp['date']<='2017-09-01')]
termspread = pd.DataFrame({'10m5':list(pd.merge(termsp,dates,on='date').groupby('ym')[0].mean().values),
            '10m1':list(pd.merge(termsp,dates,on='date').groupby('ym')[1].mean().values),
            '20m10':list(pd.merge(termsp,dates,on='date').groupby('ym')[2].mean().values)})
termspread['ym'] = days
part1 = pd.merge(termspread,inter,on='ym')
corporate = pd.read_csv('~/corporate.csv',encoding='gb2312')[1:-2]
cop = pd.DataFrame({'AAA':corporate[corporate.columns[6]],
                    'AA':corporate[corporate.columns[24]],
                    'A':corporate[corporate.columns[42]]})
#pd.read_csv('~/corporate.csv',encoding='gb2312').columns[42]
cop['date']=corporate[corporate.columns[0]]
cop =pd.merge(cop,interest[interest['maturity']=='1.0'],on='date')
copp = pd.DataFrame({'aaa':pd.Series(map(float,cop['AAA']))-cop['rate'],
'aa':pd.Series(map(float,cop['AA']))-cop['rate'],'a':pd.Series(map(float,cop['A']))-cop['rate']})
copp['date'] = cop['date']
copp = pd.merge(copp,dates,on='date')
copp =copp[(copp['date']>='2011-01-01') & (copp['date']<='2017-09-01')]
part2 = pd.DataFrame({'aaa':copp.groupby('ym')['aaa'].mean().values,
              'aa':copp.groupby('ym')['aa'].mean().values,
              'a':copp.groupby('ym')['a'].mean().values})
part2['ym'] = copp.groupby('ym')['aaa'].mean().index
macro = pd.merge(part2,part1,on='ym')




##企业层面：
set_sql('mysql','210.34.5.184','group1','Group1.321','group1')
data= pd.read_csv('~/fund.csv')
test1 = search_sql('select institution_id,industry_name from static_institution')
test1['institution_id'] = np.int64(list(test1['institution_id']))
set_sql('mysql', '172.16.8.184', 'qc_data', 'wisesoe.qc', 'qc_data')
data = search_sql('select * from induindextest')[:-149]
da1 = pd.DataFrame({'security_id':fin['security_id'],'date':fin['listed_date']})
da2 = pd.DataFrame({'security_id':fin['security_id'],'date':fin['delisted_date']})
add1 = pd.merge(pd.merge(da1,dates),pd.merge(da2,dates),on='security_id')
fik = pd.merge(fin,add1,on='security_id')
add2 = []
for i in range(len(fik)):
    every = fik.iloc[i]
    start,end = every['ym_x'],every['ym_y']
    indu = every['industry_name']
    ek = adds[adds['industry_name']==indu]
    add2.append(ek[(ek['ym']>=start) & (ek['ym']<=end)].mean())
add2 = pd.DataFrame(add2)
del add2['industry_name']
del add2['ym']
fik2 = pd.concat([fik,add2],axis=1)
fik2  = fik2[fik2['industry_name']!='金融业']
fik2['cash_mean'] = fik2['A0001_mean'].fillna(0)+fik2['A0002_mean'].fillna(0)
fik2['accountre_mean'] = fik2['A0003_mean'].fillna(0)+fik2['A0004_mean'].fillna(0)+fik2['A0005_mean'].fillna(0)
fik2['prepaidex_mean'] = fik2['A0006_mean'].fillna(0)
fik2['inven_mean'] = fik2['A0009_mean'].fillna(0)
fik2['unamortized_mean'] = fik2['A0011_mean'].fillna(0)
fik2['othercurr_mean'] = fik2['A0019_mean'].fillna(0)
fik2['curra_mean'] = np.maximum(fik2['A0020_mean'].fillna(0),fik2['cash_mean']+fik2['accountre_mean']+fik2['prepaidex_mean']+fik['inven_mean']+
                          fik2['unamortized_mean']+fik2['othercurr_mean'])
fik2['ppe_mean'] = fik2['A0028_mean'].fillna(0)
fik2['ltar_mean'] = fik2['A0027_mean'].fillna(0)
fik2['intangiblea_mean'] = fik2['A0034_mean'].fillna(0)
fik2['rd_mean'] = fik2['A0035_mean'].fillna(0)
fik2['nonca_mean'] = np.maximum(fik2['A0021_mean'].fillna(0)+fik2['A0022_mean'].fillna(0)+fik2['A0023_mean'].fillna(0)+
fik2['A0024_mean'].fillna(0)+fik2['A0025_mean'].fillna(0)+fik2['A0026_mean'].fillna(0)+fik2['A0027_mean'].fillna(0)+
fik2['A0028_mean'].fillna(0)+fik2['A0029_mean'].fillna(0)+fik2['A0030_mean'].fillna(0)+fik2['A0031_mean'].fillna(0)+
fik2['A0032_mean'].fillna(0)+fik2['A0033_mean'].fillna(0)+fik2['A0034_mean'].fillna(0)+fik2['A0035_mean'].fillna(0)+
fik2['A0036_mean'].fillna(0)+fik2['A0037_mean'].fillna(0)+fik2['A0038_mean'].fillna(0)+fik2['A0039_mean'].fillna(0)+
fik2['A0040_mean'].fillna(0),fik2['A0041_mean'].fillna(0))
fik2['profit_mean'] =fik2['C0056_mean']
fik2['ebit_mean'] = fik2['profit_mean'].fillna(0)+fik2['interex_mean'].fillna(0)+fik2['B0046_mean'].fillna(0)
fik2['ebitda_mean'] = fik2['ebit']+fik2['ebit']+fik2['C0059_mean'].fillna(0)+fik2['C0060_mean'].fillna(0)+fik2['C0061_mean'].fillna(0)
fik2['cfoa_mean'] = fik2['coo_mean'].fillna(0)/fik2['ta_mean'].fillna(0)
fik2['cfoa_mean'] = (fik2['reve_mean'].fillna(0)-fik2['B0023_mean'].fillna(0))/fik2['ta_mean'].fillna(0)
fik2['roa_mean'] = fik2['profit_mean'].fillna(0)/fik2['ta_mean'].fillna(0)
fik2['roe_mean'] = fik2['profit_mean'].fillna(0)/(fik2['ta_mean'].fillna(0)-fik2['tl_mean'].fillna(0))

fik2['ta_mean'] = np.maximum(fik2['curra_mean'] + fik2['nonca_mean'],fik2['A0060_mean'].fillna(0))
fik2['cl_mean'] = np.maximum(fik2['A0061_mean'].fillna(0)+fik2['A0062_mean'].fillna(0)+fik2['A0063_mean'].fillna(0)+fik2['A0064_mean'].fillna(0)+fik2['A0065_mean'].fillna(0)
+fik2['A0066_mean'].fillna(0)+fik2['A0067_mean'].fillna(0)+fik2['A0068_mean'].fillna(0)+fik2['A0071_mean'].fillna(0)+
fik2['A0072_mean'].fillna(0)+fik2['A0073_mean'].fillna(0)+fik2['A0074_mean'].fillna(0)+fik2['A0075_mean'].fillna(0)+
fik2['A0076_mean'].fillna(0)+fik2['A0077_mean'].fillna(0)+fik2['A0078_mean'].fillna(0),fik2['A0084_mean'].fillna(0))
fik2['ncl_mean'] = np.maximum(fik2['A0086_mean'].fillna(0)+fik2['A0087_mean'].fillna(0)+fik2['A0088_mean'].fillna(0)+fik2['A0089_mean'].fillna(0)+
                       fik2['A0090_mean'].fillna(0)+fik2['A0091_mean'].fillna(0)+fik2['A0092_mean'].fillna(0)+fik2['A0093_mean'].fillna(0),fik2['A0094_mean'].fillna(0))
fik2['tl_mean'] = np.maximum(fik2['A0111_mean'].fillna(0),fik2['cl_mean']+fik2['ncl_mean'])
fik2['quickratio_mean'] = fik2['curra_mean']/fik2['cl_mean']
fik2['cashratio_mean'] = (fik2['cash_mean'])/fik2['cl_mean']
fik2['superratio_mean'] = (fik2['curra_mean']-fik2['prepaidex_mean']-fik2['inven_mean']-fik2['unamortized_mean'])/fik2['cl_mean']
fik2['leverage_mean'] = fik2['tl_mean']/fik2['ta_mean']
fik2['equityratio_mean'] = fik2['tl_mean']/(fik2['ta_mean']-fik2['tl_mean'])
fik2['reve_mean'] = fik2['B0002_mean'].fillna(0)
fik2['interex_mean'] = fik2['B0029_mean']
fik2['coo_mean'] =fik2['C0026_mean'].fillna(0)
fik2['cio_mean'] = fik2['C0032_mean'].fillna(0)
fik2['cfo_mean'] =  fik2['C0051_mean'].fillna(0)
fik2['fcf_mean'] = (fik2['coo_mean']-fik2['ppe_mean']+fik2['A0028_1']+fik2['C0059_mean'].fillna(0)+fik2['C0060_mean'].fillna(0)+fik2['C0061_mean'].fillna(0))
fik2['fcfcoo_mean']=fik2['fcf_mean'].fillna(0)/fik2['coo_mean']
fik2['cootl_mean'] = fik2['coo_mean']/fik2['tl_mean']
fik2['operex_mean'] = fik2['B0022_mean']


