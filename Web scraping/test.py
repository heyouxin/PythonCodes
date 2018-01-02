# -*- coding: utf-8 -*-
"""
Created on Sun Dec 10 19:13:31 2017

@author: 何友鑫
"""

import re
import urllib.request

def getLink(url):
    #urllib.request.install_opener(opener)
    file=urllib.request.urlopen(url)
    data=str(file.read())
    pat='(https?://[^\s)";]+\.(\w|/)*)'
    link=re.compile(pat).findall(data)
    link=list(set(link))
    return link


url="https://www.federalreserve.gov/releases/H41/default.htm"
linklist=getLink(url)
for link in linklist:
    print(link[0])






a=1
b=0
try:
    a=2
    c=a/b
    
except:
    pass
finally:
    pass
b=1








)'