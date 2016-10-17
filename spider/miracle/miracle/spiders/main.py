#-*-coding:utf-8-*-
__author__="vpersie9"

from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.selector import Selector
from miracle.items import MiracleItem
from scrapy.http import Request
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class MainSpider(CrawlSpider):
	name="miracle"
#	allowed_domains=["sushubaike.com"]
	start_urls=["http://dushubaike.com/a/guji/shanhaijing.html"]
	
	def start_requests(self):
#		return [Request("http://dushubaike.com/a/guji/shanhaijing.html",callback=self.parse_page)]
		for url in self.start_urls:
			yield Request(url,callback=self.parse_page)
			#yield self.make_requests_from_url(url)	调用make_requests_from_url方法无法制定自己的回调 只能用默认的parse而不是parse_page
	
	def parse_page(self,response):
		selector=Selector(response)
		all=selector.xpath('//div[@class="dushubaike_main"]')[0]
		bookName=all.xpath('div[@class="dushubaike_main_ls fl"]/h1/text()').extract()[0]
		chapter_all=all.xpath('//div[@class="speciallist"]/dl[@class="tbox"]//dd//a').extract()
		url_all=all.xpath('//div[@class="speciallist"]/dl[@class="tbox"]//dd//a/@href').extract()
		url=[]
		for each in url_all:
			tar='http://dushubaike.com/view/'+each.split('/')[3].split('.')[0]
			url.append(tar)

		for i in range(len(url)):
			item=MiracleItem()
			item["bookName"]=bookName.decode('utf-8')
			item["chapterURL"]=url[i]
			Compile=re.compile('blank">(.*?)</a>',re.S)			
			chaptername=chapter_all[i].decode('utf-8')
			result=re.search(Compile,chaptername).group(1)
			item["chapterName"]=result
#			yield item
			yield Request(url[i],callback=self.parseContent,meta={'item':item})

	def parseContent(self,response):
		selector=Selector(response)
		item=response.meta['item']
		html=selector.xpath('//div[@class="panel-body"]/div[@class="entry-content"]/p/text()').extract()
		text=''
		for each in html:
			text += each.decode('utf-8')+'\n'
		item['text']=text
		yield item
