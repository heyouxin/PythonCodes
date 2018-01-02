# -*- coding: utf-8 -*-
"""
Created on Sat Dec 30 13:46:32 2017

@author: 何友鑫
"""

from rqalpha import run_file

config = {
  "base": {
    "start_date": "2016-06-01",
    "end_date": "2016-12-01",
    "benchmark": "000300.XSHG",
    "accounts": {
        "stock": 100000
    }
  },
  "extra": {
    "log_level": "verbose",
  },
  "mod": {
    "sys_analyser": {
      "enabled": True,
      "plot": True
    }
  }
}

strategy_file_path = "C:/ProgramData/Anaconda3/envs/python35/Lib/site-packages/rqalpha/examples/buy_and_hold.py"

run_file(strategy_file_path, config)