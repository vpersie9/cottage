# -*- coding: utf-8 -*-
import scrapy


class DomainSpider(scrapy.Spider):
    name = "domain"
    allowed_domains = ["domain.com"]
    start_urls = (
        'http://www.domain.com/',
    )

    def parse(self, response):
        pass
