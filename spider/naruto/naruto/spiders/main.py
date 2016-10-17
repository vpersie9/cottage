#-*-coding:utf-8-*-
__author__="vpersie9"

from scrapy.contrib.spiders import CrawlSpider
from scrapy.selector import Selector
from naruto.items import NarutoItem
from scrapy.http import Request
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class MainSpider(CrawlSpider):
	name="naruto"
	start_urls=["http://ac.qq.com/ComicView/index/id/505432/cid/1"]
