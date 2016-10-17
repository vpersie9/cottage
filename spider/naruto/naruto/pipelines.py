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

class NarutoPipeline(object):

	def __init__(self):
		self.host=settings['MONGODB_HOST']
		self.port=settings['MONGODB_PORT']
		self.dbName=settings['MONGODB_DBNAME']
		self.tabName=settings['MONGODB_TABNAME']

	def open_spider(self,spider):
		self.client=pymongo.MongoClient(self.host,self.port)
		self.db=self.client[self.dbName]
		self.tab=self.db[self.tabName]
	
	def close_spider(self,spider):
		self.client.close()

	def process_item(self,item,spider):
		try:
			comdyInfo=dict(item)
			if self.dbName in self.client.database_names():
				self.client.drop_database(self.dbName)
			self.tab.insert(comdyInfo)
		except Exception,e:
			print e

		try:
			imgURL=item['imgURL']
			pass
