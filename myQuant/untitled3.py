# -*- coding: utf-8 -*-
"""
Created on Sun Nov  5 15:08:32 2017

@author: 何友鑫
"""

class Solution:
    a=0
    b=0
    c=1
    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        self.c=2
        l=[]
        nums_1=nums
        #[nums<=target]
        for i in range(len(nums_1)):
            for j in range(i+1,len(nums_1)):
                if (nums_1[i]+nums_1[j])==target:
                    l.append(i)
                    l.append(j)
                    return (l)
    def Dis(self):
        print(self.c)

if __name__=='__main__':
   
    s=Solution()
    s.Dis()  
    nums=[2,7,11,15]
    target=26
    l=s.twoSum(nums,target)
    print(l)   
    
    
    
    '''
    hs_file='./HS300数据/hs300_weights_2005.xls'
    hs300s=pd.read_excel(hs_file)
    '''    