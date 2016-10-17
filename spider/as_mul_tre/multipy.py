#-*-coding:utf-8-*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import urllib2
import time
import multiprocessing

def function(url,headers):
	request=urllib2.Request(url=url,headers=headers)
	response=urllib2.urlopen(request)
	print response.read().decode('utf-8')

def main():
	headers={'User-Agent':'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36'}
	urls=[]
	url_root='http://www.baidu.com?page='
	for i in range(1,100):
		urls.append(url_root+'%s'%i)
	pool=multiprocessing.Pool(processes=1)
	try:
		for url in urls:
			pool.apply_async(function,(url,headers))
		pool.close()
		pool.join()
		print "All tasks done"
	except Exception,e:
		print e

if __name__=="__main__":
	curtime=time.time()
	main()
	time.time()-curtime
