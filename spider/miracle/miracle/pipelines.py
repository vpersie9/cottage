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

class MiraclePipeline(object):

	def __init__(self):
		self.host=settings['MONGODB_HOST']
		self.port=settings['MONGODB_PORT']
		self.dbName=settings['MONGODB_DBNAME']
		self.tabName=settings['MONGODB_TABNAME']

	def open_spider(self,spider):
		self.client=pymongo.MongoClient(self.host,self.port)
		self.db=self.client[self.dbName]
		self.tab=self.db[self.tabName]
		self.file=open("miracle.odt",'wb+')
	
	def close_spider(self,spider):
		self.client.close()
		self.file.close()
		
	def process_item(self, item, spider):
		try:
			bookInfo=dict(item)
			if self.dbName in self.client.database_names():
				self.client.drop_database(self.dbName)
			self.tab.insert(bookInfo)
		except Exception,e:
			print e
		
		try:	
			title=item['chapterName']
			self.file.write(title+"\n")
			content=item['text']
			self.file.write(content+"\n\n")
		except Exception,e:
			print e

		return item
