#-*-coding:utf8-*-
__author__="vpersie9"

from scrapy.contrib.spiders import CrawlSpider
from scrapy.selector import Selector
from spider_scrapy.items import SpiderScrapyItem
from scrapy.http import Request
import re
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class MainSpider(CrawlSpider):
	name="novel"
	allowed_domains=["daomubiji.com","idaomu.com"]
	start_urls=["http://www.daomubiji.com"]

	def parse(self,response):

		select=Selector(response)
		#item=SpiderScrapyItem()
		table=select.xpath("//table")
		for each in table:
			bookName=each.xpath('tr/td[@colspan="3"]/center/h2/text()').extract()[0]
			content=each.xpath('tr/td/a/text()').extract()
			url=each.xpath('tr/td/a/@href').extract()
			for i in range(len(url)):
				item=SpiderScrapyItem()
				item['bookName']=bookName.decode('utf8')
				item['chapterURL']=url[i]
				try:
					item['bookTitle']=content[i].split(' ')[0].decode('utf8')
					item['chapterNum']=content[i].split(' ')[1].decode('utf8')
				except Exception,e:
					continue
				
				try:
					item['chapterName']=content[i].split(' ')[2].decode('utf8')
				except Exception,e:
					item['chapterName']=content[i].split(' ')[1][-3:].decode('utf8')

				yield Request(url[i],callback=self.parseContent,meta={'item':item})

	
	def parseContent(self,response):
		selector=Selector(response)
		item=response.meta['item']
		html=selector.xpath('//div[@class="content"]').extract()[0]
		textField_compile=re.compile('<div style="clear:both"></div>(.*?)<p class="shangxia"',re.S)
		textField=re.search(textField_compile,html).group(1)
		text_compile=re.compile('<p>(.*?)</p>',re.S)
		text=re.findall(text_compile,textField)
		fulltext='\n'
		for each in text:
			fulltext += each.decode('utf8')
		item['text']=fulltext
		yield item
