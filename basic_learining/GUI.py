# -*- coding: utf-8 -*-
"""
Created on Sun Jun 25 16:43:21 2017

@author: 何友鑫
"""

#import tkinter.filedialog
#fn=tkinter.filedialog.askopenfilename(title='选择一个文件', filetypes=[('所有文件','.*'),('文本文件','.txt')])


#import _tkinter
#import tkinter
#tkinter._test()
#import tkinter.filedialog as tk_f
from tkinter import filedialog as tk_f
import pandas as pd
#fn=tk_f.askopenfilename(title='选择一个文件', filetypes=[('所有文件','.*'),('文本文件','.txt')])

fn=tk_f.askopenfilename()
data=pd.read_csv(fn)
print (type(data))
fn_save=tk_f.asksaveasfilename()
data.to_csv(fn_save+".csv")