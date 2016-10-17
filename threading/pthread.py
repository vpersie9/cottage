import threading
from time import ctime,sleep

class MyThread(threading.Thread):
	def __init__(self,func,args,name=''):
		super(MyThread,self).__init__()
		self.func=func
		self.args=args
		self.name=name
	
	def getResult(self):
		return self.res
	
	def run(self):
		print "starting",self.name,"at:",ctime()
		self.res=self.func(*self.args)
		print self.name,"finished at:",ctime()
