# -*- coding: utf-8 -*-
import scrapy


class TencentSpider(scrapy.Spider):
    name = 'tencent'
    allowed_domains = ['ac.qq.com']
    start_urls = ['http://ac.qq.com/']

    def parse(self, response):
        pass
