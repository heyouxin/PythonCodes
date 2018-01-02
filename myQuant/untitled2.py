# -*- coding: utf-8 -*-
"""
Created on Fri Nov  3 12:48:52 2017

@author: 何友鑫
"""



w.wsq("600000.SH,000001.SZ","rt_last,rt_last_vol")


w.wset("IndexConstituent","date=20171103;windcode=000300.SH;field=wind_code,i_weight")

data=w.wss("600000.SH,000001.SZ","eps_ttm,orps,surpluscapitalps","rptDate=20121231")



from WindPy import *
w.start()
w.isconnected()
data=w.wsd("600000.SH","close,amt", datetime.today()-timedelta(100))