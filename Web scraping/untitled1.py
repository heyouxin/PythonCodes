# -*- coding: utf-8 -*-
"""
Created on Thu May  3 16:11:30 2018

@author: 何友鑫
"""

class ListNode:   
    def __init__(self, x):
        self.val = x
        self.next = None

l1=ListNode(1) 
l2=ListNode(2)
l1.val
l1.next=l2
l1.next.val

ll=[1,2,3]
ll[::-1]

x=-123
x1=abs(x)
x1=list(str(x1))
y=''
for i in range(0,len(x1)):
    y=y+x1[i]
y=int(y)
if x<0:
    y=-1*y



(x[::-1])

x=str(x)



res=[]
for i in range(0,len(x)):
    #print()
    res.append(x[len(x)-i-1])

res=int(res)
    
len(x)


dict={}
dict[0]=1
0 in dict

r=0
while x:
    r=r*10+x%10
    x/=10
    
    
class ListNode:   
    def __init__(self, x):
        self.val = x
        self.next = None

l1=ListNode(2)
l11=ListNode(4)
l111=ListNode(3)  
l1.next=l11 
l11.next=l111

l2=ListNode(5)
l22=ListNode(6)
l222=ListNode(4) 
l2.next=l22
l22.next=l222

num1=0
num2=0
while l1 or l2:
    num1=num1*10+l1.val
    l1=l1.next
    
    num2=num2*10+l2.val
    l2=l2.next

re_num1=0
re_num2=0
while num1:
  
    re_num1=re_num1*10+num1%10
    num1=int(num1/10)

while num2:
  
    re_num2=re_num2*10+num2%10
    num2=int(num2/10)

x >= -1*(2^31) & x <= (pow(2,31))-1 < 
        
        
        x=1534236469
        
    
        r=0
        if x>=0:
            while x:
                r=r*10+x%10
                x=int(x/10)
        else:
            x=-1*x
            while x:
                r=r*10+x%10
                x=int(x/10)
            r=-1*r
        if (r < -1*pow(2,31)) | (r > pow(2,31)-1): 
            r=0
        r
        
        
        
test_list=[[1],[2]]
test_list[1][0] 
        
        
        
        
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
        l_sum=[]
        for m in range(0,len(self.nums)):
            for n in range(m,len(self.nums)):
                if n==m:
                    l_sum[m][n]=self.nums[n]
                else:
                    l_sum[m][n]=l_sum[m][n-1]+self.nums[n]
            
        return l_sum[i][j]
    
    
l1=[-2, 0, 3, -5, 2, -1]
l_sum=[[0] * len(l1)] * len(l1)
for m in range(0,len(l1)):
    for n in range(m,len(l1)):
    
        if n==m:
            l_sum[m][n]=l1[n]
        else:
            
            l_sum[m][n]=l_sum[m][n-1]+l1[n]

l_sum[1][5]

numa=NumArray(l1)
#numa.nums[0]
numa.sumRange(1,2)
