#-*-coding:utf-8-*-
u'''
这个python 文件是关于各种数据结构的python 代码实现
用于工作面试用
'''
u'堆栈的实现'
class _Stack(object):
	def __init__(self):
		self.items=[]
	
	def isEmpty(self):
		return self.items==[]

	def push(self,item):
		self.items.append(item)

	def pop(self):
		self.items.pop()

	def peek(self):
		return self.items[len(self.items)-1]

	def size(self):
		return len(self.items)

	def __repr__(self):
		return self.items

u'队列的实现'
class _Queue(object):
	def __init__(self):
		self.items=[]

	def isEmpty(self):
		return self.items==[]

	def enqueue(self,item):
		self.items.insert(0,item)

	def dequeue(self):
		self.items.pop()

	def size(self):
		return len(self.items)

	def __repr__(self):
		return self.items

u'双向队列的实现'

class _Deque(object):
	def __init__(self):
		self.items=[]

	def isEmpty(self):
		return self.items==[]

	def addFront(self,item):
		self.items.append(item)

	def addRear(self,item):
		self.items.insert(0,item)
	
	def removeFront(self):
		self.items.pop()
	
	def removeRear(self):
		self.items.pop(0)

	def size(self):
		return len(self.items)

	def __repr__(self):
		return self.items
u'无序链表'

class Node(object):
	def __init__(self,initdata):
		self.data=initdata
		self.next=None
		
	def getData(self):
		return self.data

	def getNext(self):
		return self.next
	
	def setData(self,newdata):
		self.data=newdata

	def setNext(self,newnext):
		self.next=newnext

class UnorderedList(object):
	def __init__(self):
		self.head=None

	def isEmpty(self):
		return self.head==None

	def add(self,item):
		temp=Node(item)
		temp.setNext(self.head)
		self.head=temp

	def size(self):
		current=self.head
		count=0
		while current != None:
			count += 1
			current=current.getNext()
		return count

	def search(self,item):
		current=self.head
		found=False
		while current != None and not found:
			if current.getData() == item:
				found=True	
			else:
				current=current.getNext()
		return found

	def remove(self,item):
		current=self.head
		previous=None
		found=False
		while not found:
			if current.getData() == item:
				found=True
			else:
				previous=current
				current=current.getNext()
		if previous==None:
			self.head=current.getNext()
		else:
			'''
			这里的previous 和 current 都是可修改
			对象 下面这行代码真正实现了删除
			直接将删除的一个值过掉 利用previous拼接
			类似于 _ _ 0 _ _ 然后删除0 拼接成_ _ _ _
			'''
			previous.setNext(current.getNext())

u'有序列表'

class OrderedList(object):
	def __init__(self):
		self.head=None

	def search(self,item):
		current=self.head
		found=False
		stop=False
		while current != None and not found and not stop:
			if current.getData() == item:
				found=True
			else:
				if current.getData()>item:
					stop=True
				else:
					current=current.getNext()
		return found

	def add(self,item):
		current=self.head
		previous=None
		stop=False
		while current != None and not stop:
			if current.getData() > item:
				stop=True
			else:
				previous=current
				current=current.getNext()
		temp=Node(item)
		if previous == None:
			temp.setNext(self.head)
			self.head=temp
		else:
			u'''
			分成两段进行拼接 _ _ _ _
			_ _ 
			temp _ _
			拼接成previous_ _ temp _ _
			也就是_ _ _ _ _	
			'''
			temp.setNext(current)
			previous.setNext(temp)

u'交叉链表求交点'
u'''
仔细研究两个链表，如果他们相交的话，那么他们最后的一个节点一定是相同的，否则是不相交的。因此判断两个链表是否相交就很简单了，分别遍历到两个链表的尾部，然后判断他们是否相同，如果相同，则相交；否则不相交。

判断出两个链表相交后就是判断他们的交点了。假设第一个链表长度为len1，第二个问len2，然后找出长度较长的，让长度较长的链表指针向后移动|len1 - len2| (len1-len2的绝对值)，然后在开始遍历两个链表，判断节点是否相同即可。
'''

def node_point(l1,l2):
	length1,length2=node_len(l1,l2)
	if length1>length2:
		for i in range(length1-length2):
			l1=l1.next
			print l1.initdata
	else:
		for i in range(length2-length1):
			l2=l2.next
			print l2.initdata

	while l1 and l2:
		if node_test(l1,l2):
			print 'Points True,the point object is:'
			return l1
		l1=l1.next
		l2=l2.next
	return False

def node_len(l1,l2):
	length1,length2=0,0
	while l1.next:
		l1=l1.next
		length1 += 1
	while l2.next:
		l2=l2.next
		length2 += 1
	return (length1,length2)

def node_test(l1,l2):
	while l1 and l2:
		if not l1.initdata==l2.initdata:
			return False
		l1=l1.next
		l2=l2.next
	return True


class Node_(object):
	def __init__(self,initdata=None,next=None):
		self.initdata=initdata
		self.next=next

def reverseNode(node):
	previous=node
	current=node.next
	previous.next=None
	while current:
		tmp=current.next
		current.next=previous
		previous=current
		current=tmp
	return previous

if __name__=="__main__":
	node1=Node_(1,Node_(2,Node_(3,Node_(4,Node_(5,Node_(6,None))))))
	node2=Node_(8,Node_(5,Node_(6,None)))
	print node_point(node1,node2)
	node=reverseNode(node1)
	while node:
		print node.initdata
		node=node.next
