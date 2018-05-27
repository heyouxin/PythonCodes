# -*- coding: utf-8 -*-
"""
Created on Tue May 15 22:05:13 2018

@author: 何友鑫
"""
a,b=b,a
a=b=0
a=1


def print_():
    print(111)
    t=1
    m=2

def longestPalindrome( s):
    """
    :type s: str
    :rtype: str
    """
    length=0
    max_len=0
    sub_str=''

    
    if len(s)==1:
        sub_str=s
    else:
        for i in range(0,len(s)-1):
            for j in range(i+1,len(s)):
                if (j-i)%2==0:
                    print_()
                    if s[i:(((j+i)//2)+1)]==s[((j+i)//2):(j+1)][::-1]:
                        length=j-i+1                 
                        max_len=max(length,max_len)
                        if length==max_len:
                            sub_str=s[i:j+1]
                else:
                    if s[i:(((j+i)//2)+2)]==s[((j+i)//2):(j+1)][::-1]:
                        length=j-i+1                 
                        max_len=max(length,max_len)
                        if length==max_len:
                            sub_str=s[i:j+1]
                
    if sub_str=='':
        sub_str=s[0]
    return sub_str       


s="aba"
#s[0:2]
longestPalindrome(s)
"""
s[1:(((2+1)//2)+1)]==s[((2+1)//2):(2+1)][::-1]
"""