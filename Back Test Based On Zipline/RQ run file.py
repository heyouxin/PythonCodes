# -*- coding: utf-8 -*-
"""
Created on Sat Dec 30 13:43:28 2017

@author: 何友鑫
"""

import pandas as pd
import numpy as np
a=get_price('000001.XSHE',start_date='2015-04-01',end_date='2015-04-12')
a


rqalpha run -f C:/ProgramData/Anaconda3/envs/python35/Lib/site-packages/rqalpha/examples/buy_and_hold.py -d C:/Users/heyouxin/.rqalpha/bundle/ -s 2017-06-01 -e 2017-12-01 --account stock 100000 --benchmark 000300.XSHG --plot