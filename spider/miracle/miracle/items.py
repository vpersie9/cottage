# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class MiracleItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    bookName=scrapy.Field()
    chapterName=scrapy.Field()
    chapterURL=scrapy.Field()
    text=scrapy.Field()
