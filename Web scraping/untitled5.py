# -*- coding: utf-8 -*-
"""
Created on Thu May 17 21:07:12 2018

@author: 何友鑫
"""
'''
import math as m

def climbStairs(n):
    """
    :type n: int
    :rtype: int
    """
    ways=0
    n_two=n//2
    if n%2==0:
        k=n_two
        for i in range(0,k):
            ways=ways+m.factorial(n-i)/(m.factorial(i)*m.factorial(n-i-i))
        return int(ways+1)
   
    else:
        k=n_two+1
        for i in range(0,k):
            ways=ways+m.factorial(n-i)/(m.factorial(i)*m.factorial(n-i-i))
        return int(ways)
 
    
#climbStairs(5)



def longestPalindrome( s): 
    max_sub=""
    temp=""
    for i in range(0,len(s)):
        #aba
        l=i
        r=i
        while l>=0 and r<len(s) and s[l]==s[r]:
            temp=s[l:r+1]
            l-=1
            r+=1
            
        if len(temp)>len(max_sub):
            max_sub=temp
        l=i
        r=i+1
        while l>=0 and r<len(s) and s[l]==s[r]:
            temp=s[l:r+1]
            l-=1
            r+=1
        if len(temp)>len(max_sub):
            max_sub=temp
        
    return max_sub

longestPalindrome("babad")
'''


l=[
  [0,0,0],
  [0,1,0],
  [0,0,0]
]

def uniquePathsWithObstacles( obstacleGrid):
    """
    :type obstacleGrid: List[List[int]]
    :rtype: int
    """
    ways=0
    m=len(obstacleGrid)
    n=len(obstacleGrid[0])
    way_sum=0
    for i in range(m):
        for j in range(n):
            way_sum+=obstacleGrid[m][n]
            if way_sum==
    
    
    i=0  
    
    
    
    while i<m:
        j=0
        while j<n:
                      
            if i==m and j==n:
                ways+=1
            
            if obstacleGrid[i][j+1]!=1:
              
                j+=1
            else:
                j-=1
                break

                
        if obstacleGrid[i+1][j]!=1:
            i+=1
                
        if i==m and j==n:
            ways+=1       
    return ways

uniquePathsWithObstacles(l)