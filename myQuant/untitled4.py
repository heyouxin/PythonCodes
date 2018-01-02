# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 19:01:30 2017

@author: 何友鑫
"""

import re
import tkinter.filedialog
fn=tkinter.filedialog.askopenfilename(title='选择一个文件', filetypes=[('所有文件','.*'),('文本文件','.txt')])
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import jieba
from os import path
f = open(fn, 'r',encoding='utf-8', errors='ignore')
###测试文件用gbk
#f = open(fn, 'r',encoding='gbk')

###2.7版本的python codecs.open 或 io.open
#import codecs
#f=codecs.open(fn,'r','utf-8')

print("open success!")
file=f.readlines()
print("read success!")
f.close()
file=str(file)
wordcloud = WordCloud(background_color="white",mask='1111.png',font_path='C:\Windows\Fonts\STZHONGS.TTF',width=8000, height=8060, margin=20).generate(file)
# width,height,margin可以设置图片属性
# generate 可以对全部文本进行自动分词,但是他对中文支持不好,对中文的分词处理请看我的下一篇文章
#wordcloud2 = WordCloud(background_color="white",mask='1111.png',max_words=200,font_path = r'D:\Fonts\simkai.ttf').generate(file)
# 你可以通过font_path参数来设置字体集
#background_color参数为设置背景颜色,默认颜色为黑色
plt.imshow(wordcloud2)
plt.axis("off")
plt.show()
d = path.dirname(__file__)
imgname1 = "1122.png"
wordcloud2.to_file(path.join(d, imgname1))