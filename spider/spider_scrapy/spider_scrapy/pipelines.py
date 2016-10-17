# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.conf import settings
import pymongo
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class SpiderScrapyPipeline(object):

    def __init__(self):
	host=settings['MONGODB_HOST']
	port=settings['MONGODB_PORT']
	dbName=settings['MONGODB_DBNAME']
	tabName=settings['MONGODB_TABNAME']
	client=pymongo.MongoClient(host=host,port=port)
	db=client[dbName]
	self.dbName=dbName
	self.client=client
	self.post=db[tabName]
	self.file=open("novel.txt","w+")

    def process_item(self, item, spider):
	#u'生成数据库'
	try:
        	bookInfo=dict(item)
		if self.dbName in self.client.database_names():
			self.client.drop_database(self.dbName)
		self.post.insert(bookInfo)
	except Exception,e:
		return e

	#u'生成txt文件'
	try:
		for each in item.keys():
			line=item[each]+"\n"
			self.file.write(line)
	except Exception,e:
		return e
	
	return item
