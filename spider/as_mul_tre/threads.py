#-*-coding:utf-8-*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import Queue
import urllib2
import os
import threading
import time

class Worker(threading.Thread):
	def __init__(self,workqueue,resultqueue,**kwargs):
		threading.Thread.__init__(self,**kwargs)
		self.setDaemon(True)
		self.workqueue=workqueue
		self.resultqueue=resultqueue
	
	def run(self):
		while True:
			try:
				callable,args,kwargs=self.workqueue.get(False)
				res=callable(*args,**kwargs)
				self.resultqueue.put(res)
			except self.workqueue.empty:
				break
				print "workqueue is empty"

class WorkManager:
	def __init__(self,num_of_workers=10):
		self.workqueue=Queue.Queue()
		self.resultqueue=Queue.Queue()
		self.workers=[]
		self.recruitThreads(num_of_workers)
		
	def recruitThreads(self,num_of_workers):
		for i in range(num_of_workers):
			worker=Worker(self.workqueue,self.resultqueue)
			self.workers.append(worker)

	def start(self):
		for item in self.workers:
			item.start()

	def wait_for_complete(self):
		while len(self.workers):
			worker=self.workers.pop()
			worker.join()
			if worker.isAlive and not self.workqueue.empty():
				self.workers.append(worker)
		print "All jobs were complete."

	def add_job(self,callable,*args,**kwargs):
		self.workqueue.put((callable,args,kwargs))

	def get_result(self,*args,**kwargs):
		return self.resultqueue.get(*args,**kwargs)
	
def download_file(url):
	headers={"User-Agent":"Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36"}
	request=urllib2.Request(url,headers=headers)
	response=urllib2.urlopen(request)
	print response.read().decode('utf-8')

def main():
	try:
		num_of_threads=int(sys.argv[1])
	except:
		num_of_threads=10
	curtime=time.time()
	wm=WorkManager(num_of_threads)
	print num_of_threads
	urls=['http://www.baidu.com']*100
	for i in urls:
		wm.add_job(download_file,i)
	wm.start()
	wm.wait_for_complete()
	print time.time()-curtime

if __name__=="__main__":
	main()
