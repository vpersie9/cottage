#-*-coding:utf-8-*-

u'''
这个脚本的代码主要介绍了树包括二叉树和AVL树等数据结构的
实现和基本的操作
'''

class BinaryTree(object):
	def __init__(self,root):
		self.key=root
		self.left_child=None
		self.right_child=None

	def insert_left(self,new_node):
		#u'树的最下端插入肯定是None'
		if self.left_child==None:
			self.left_child=BinaryTree(new_node)
		#u'树的顶端或者中间进行插入 会涉及到树结构的断开和重新拼接'
		else:
			t=BinaryTree(new_node)
			t.left_child=self.left_child
			self.left_child=t

	def insert_right(self,new_node):
		if self.right_child==None:
			self.right_child=BinaryTree(new_node)
		else:
			t=BinaryTree(new_node)
			t.left_child=self.left_child
			self.left_child=t

	def get_right_child(self):
		return self.right_child

	def get_left_child(self):
		return self.left_child

	def set_root_val(self,obj):
		self.key=obj

	def get_root_val(self):
		return self.key

u'二叉树的遍历'



u'二叉堆（最小二叉堆）'

class BinHeap:
    def __init__(self):
        self.heapList = [0]
        self.currentSize = 0


    def percUp(self,i):
        while i // 2 > 0:
          if self.heapList[i] < self.heapList[i // 2]:
             tmp = self.heapList[i // 2]
             self.heapList[i // 2] = self.heapList[i]
             self.heapList[i] = tmp
          i = i // 2

    def insert(self,k):
      self.heapList.append(k)
      self.currentSize = self.currentSize + 1
      self.percUp(self.currentSize)

    def percDown(self,i):
      while (i * 2) <= self.currentSize:
          mc = self.minChild(i)
          if self.heapList[i] > self.heapList[mc]:
              tmp = self.heapList[i]
              self.heapList[i] = self.heapList[mc]
              self.heapList[mc] = tmp
          i = mc

    def minChild(self,i):
     # u'说明只有左子节点'
      if i * 2 + 1 > self.currentSize:
          return i * 2
      else:
	 # u'左子节点小于右子节点'
          if self.heapList[i*2] < self.heapList[i*2+1]:
              return i * 2
	  #u'左子节点大于由子节点'
          else:
              return i * 2 + 1

    def delMin(self):
      retval = self.heapList[1]
      self.heapList[1] = self.heapList[self.currentSize]
      self.currentSize = self.currentSize - 1
      self.heapList.pop()
      self.percDown(1)
      return retval

    def buildHeap(self,alist):
      i = len(alist) // 2
      self.currentSize = len(alist)
      self.heapList = [0] + alist[:]
      while (i > 0):
          self.percDown(i)
          i = i - 1

u'树的遍历'
class NodeTree(object):
	def __init__(self,root,left=None,right=None):
		self.root=root
		self.left=left
		self.right=right

u'层次遍历'
def lookup(node):
	stack=[node]
	while stack:
		current=stack.pop(0)
		print current.root
		if current.left:
			stack.append(current.left)
		if current.right:
			stack.append(current.right)

u'前序遍历（深度）'
def deep_front(node):
	if not node:
		return 
	print node.root
	deep_front(node.left)
	deep_front(node.right)

u'中序遍历（深度）'
def deep_middle(node):
	if not node:
		return 
	deep_middle(node.left)
	print node.root
	deep_middle(node.right)

u'后序遍历（深度）'
def deep_rear(node):
	if not node:
		return 
	deep_rear(node.left)
	deep_rear(node.right)
	print node.root

u'最大树深'
def maxDeep(node):
	if not node:
		return 0
	return max(maxDeep(node.left),maxDeep(node.right))+1

u'判断两个树是否相等'
def isSameTree(p,q):
	if p==None and q==None:
		return True
	elif p and q:
		return p.root==q.root and isSameTree(p.left,q.left) and isSameTree(p.right,q.right)
	else:
		return False

u"""
前序遍历：根节点->左子树->右子树
中序遍历：左子树->根节点->右子树
后序遍历：左子树->右子树->根节点
一定要找到规律
"""
u'前序中序求后序，重构二叉树'
def rebuild(front,middle):
	if not front:
		return 
	current=NodeTree(front[0])
	index=middle.index(front[0])
	current.left=rebuild(front[1:index+1],middle[:index])
	current.right=rebuild(front[index+1:],middle[index+1:])
	return current

u'后序中序求前序'
def rebuild_(rear,middle):
	if not rear:
		return 
	current=NodeTree(rear[len(rear)-1])
	index=middle.index(rear[len(rear)-1])
	current.left=rebuild_(rear[:index],middle[:index])
	current.right=rebuild_(rear[index:len(rear)-1],middle[index+1:])
	return current
u'前序后序求中序。。。 有难度的。。。'

if __name__=="__main__":
	tree = NodeTree(1, NodeTree(3,NodeTree(5),NodeTree(6)),NodeTree(4,NodeTree(0),NodeTree(7)))
	front=[1,3,5,6,4,0,7]
	middle=[5,3,6,1,0,4,7]	
	rear=[5,6,3,0,7,4,1]
	print u"层次遍历"
	lookup(tree)
	print u"前序遍历"
	deep_front(tree)
	print u"中序遍历"
	deep_middle(tree)
	print u"后序遍历"
	deep_rear(tree)
	print u"最大树深"
	print maxDeep(tree)
	print u'树是否相等'
	print isSameTree(tree,tree)
	print u'前中序求后序'
	node=rebuild(front,middle)
	deep_rear(node)
	print u'中序后序求前序'
	node=rebuild_(rear,middle)
	deep_front(node)
