#-*-coding:utf-8-*-
'''
这一个脚本主要是用来装载算法程序的
其中包括了排序和查找等基本算法
当然也包括了哈希查找（时间复杂度为O(1)）等高级算法
'''

u'无序列表的顺序查找'

def Unsorted_Sequence_Search(alist,item):
	found=False
	passnum=0
	while passnum<len(alist) and not found:
		if alist[passnum]==item:
			found=True
		else:
			passnum += 1
	return found


u'有序列表的顺序查找'

def Sorted_Sequence_Search(alist,item):
	found=False
	passnum=0
	stop=False
	while passnum<len(alist) and not found and not stop:
		if alist[passnum]==item:
			found=True
		else:
			if alist[passnum]>item:
				stop=True
			else:
				passnum += 1
	return found


u'二分法查找'

def Binary_Search(alist,item):
	found=False
	first=alist[0]
	last=alist[len(alist)-1]
	while first <= last and not found:
		midpoint=(first+last)//2
		if alist[midpoint]==item:
			found=True
		else:
			if alist[midpoint]<item:
				first=midpoint+1
			else:
				last=midpoint-1
	return found

u'二分法采用递归手段'

def Recursion_Binary_Search(alist,item):
	if len(alist)==0:
		return False
	else:
		midpoint=len(alist)//2
		if alist[midpoint]==item:
			return True
		else:
			if alist[midpoint]<item:
				return Recursion_Binary_Search(alist[midpoint+1:],item)
			else:
				return Recursion_Binary_Search(alist[:midpoint],item) 


u'哈希表查找 还是要看看的吧。。。'

u'冒泡排序法'

def bubble_sort(alist):
	exchanges=True
	passnum=len(alist)-1
	while passnum>0 and exchanges:
		exchanges=False
		for i in range(passnum):
			if alist[i]>alist[i+1]:
				exchanges=True
				alist[i],alist[i+1]=alist[i+1],alist[i]
		
		passnum -= 1

if __name__=="__main__":
	alist=range(7,12)+range(5)
	bubble_sort(alist)
	print alist

u'杨氏矩阵查找 矩阵特点是从左到右 从上到下 都是递增的'
u'find 方法的查找是从第一行最后开始的 要是大于查找值就向前 要是小于查找值向下'

def find(l,x):
	m=len(l)-1
	n=len(l[0])-1
	r=0
	c=n
	while c>=0 and r<=m:
		value=getValue(l,r,c)
		if value==x:
			return True
		elif value<x:
			r += 1
		elif value>x:
			c -= 1
	return False

def getValue(l,r,c):
	return l[r][c]

l=[range(4),range(1,5),range(2,6),range(3,7)]
print l

print find(l,3)



u'合并两个有序列表'


def _recursion_merge_sort2(l1,l2,tmp):
	if len(l1)==0 or len(l2)==0:
		tmp.extend(l1)
		tmp.extend(l2)
		return tmp
	else:
		if l1[0] < l2[0]:
			tmp.append(l1[0])
			del l1[0]
		else:
			tmp.append(l2[0])
			del l2[0]
		return _recursion_merge_sort2(l1,l2,tmp)

def recursion_merge_sort(l1,l2):
	return _recursion_merge_sort2(l1,l2,[])

l1=range(2,9)
l2=range(19)

print recursion_merge_sort(l1,l2)
