#-*-coding:utf-8-*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import time
from datetime import timedelta
import tornado.httpclient
import tornado.gen
import tornado.ioloop
import tornado.queues
import traceback

class AsySpider(object):
	"class of asynchronous spider"
	def __init__(self,urls,concurrency=10,**kwargs):
		urls.reverse()
		self.urls=urls
		self.concurrency=concurrency
		self.queue=tornado.queues.Queue()
		self.fetching=set()
		self.fetched=set()

	def fetch(self,url,**kwargs):
		fetch=getattr(tornado.httpclient.AsyncHTTPClient(),'fetch')
		return fetch(url,**kwargs)

	def handle_html(self,url,html):
		pass
	
	def handle_response(self,url,response):
		if response.code==200:
			self.handle_html(url,response.body)
		elif response.code==599:
			self.fetching.remove(url)
			self.queue.put(url)
	u'协程'	
	@tornado.gen.coroutine
	def get_page(self,url):
		try:
			response=yield self.fetch(url)
			print "#######fetched %s"%url
		except Exception,e:
			print 'Exception: %s %s'%(e,url)
			raise tornado.gen.Return(e)
		raise tornado.gen.Return(response)

	@tornado.gen.coroutine
	def get_run(self):
		@tornado.gen.coroutine
		def fetch_url():
			current_url=yield self.queue.get()
			try:
				if current_url in self.fetching:
					return
		
				print 'fetching ***** %s'%current_url
				self.fetching.add(current_url)

				response=yield self.get_page(current_url)
				self.handle_response(current_url,response)
			
				self.fetched.add(current_url)
				for i in range(self.concurrency):
					if self.urls:
						yield self.queue.put(self.urls.pop())
			finally:
				self.queue.task_done()
	
		@tornado.gen.coroutine
		def worker():
			while True:
				yield fetch_url()


		self.queue.put(self.urls.pop())
		for _ in range(self.concurrency):
			worker()
		yield self.queue.join(timeout=timedelta(seconds=300000))
		assert self.fetching==self.fetched

	def run(self):
		io_loop=tornado.ioloop.IOLoop.current()
		io_loop.run_sync(self.get_run)


class MySpider(AsySpider):

	u'继承AsySpider类 重写fetch handle_html方法'
	def fetch(self,url,**kwargs):
		headers={
			'User-Agent':'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36'	
		}
		return super(MySpider,self).fetch(url,headers=headers,request_timeout=1)
	
	def handle_html(self,url,html):
		print url,html

def main():
	curtime=time.time()
	urls=[]
	for page in range(1,100):
		urls.append('http://www.baidu.com?page=%s'%page)
	spider=MySpider(urls)
	spider.run()
	print time.time()-curtime

if __name__=="__main__":
	main()
	
