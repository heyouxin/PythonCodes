# -*- coding: utf-8 -*-
"""
Created on Fri May 11 11:21:44 2018

@author: 何友鑫
"""

l1=[-2, 0, 3, -5, 2, -1]
l_sum=[[0 for col in range(len(l1))] for row in range(len(l1))]
max(max(l_sum))
for m in range(0,len(l1)):
    for n in range(m,len(l1)):
    
        if n==m:
            l_sum[m][n]=l1[n]
        else:
            
            l_sum[m][n]=l_sum[m][n-1]+l1[n]



l_sum[0][5]
class NumArray:

    def __init__(self, nums):
        """
        :type nums: List[int]
        """
        self.nums=nums
        

    def sumRange(self, i, j):
        """
        :type i: int
        :type j: int
        :rtype: int
        """
        carry=0
        for t in range(i,j+1):
            carry+=self.nums[t]
        
        return carry
        """
        l_sum=[[0 for col in range(i+1)] for row in range(j+1)]
        for m in range(0,i+1):
            for n in range(m,j+1):
                if n==m:
                    l_sum[m][n]==self.nums[n]
                else:
                    l_sum[m][n]=l_sum[m][n-1]+self.nums[n]
            
        return l_sum[i][j]
        """
    
l1=[-2, 0, 3, -5, 2, -1]
numa=NumArray(l1)
#numa.nums[0]
numa.sumRange(0,5)   

l=[0]
l=l[-1]+1
   
   
   
class Solution:
    def maxProfit(self, prices):
        """
        :type prices: List[int]
        :rtype: int
        """
        #profit=[0]
        max_profit=0
        for i in range(1,len(prices)):
            for j range(i+1,len(prices)): 
                if prices[j]-prices[i] > max_profit:
                    max_profit=prices[j]-prices[i]
                    
        return max_profit
    
    
