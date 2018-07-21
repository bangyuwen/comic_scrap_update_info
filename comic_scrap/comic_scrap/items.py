# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ComicScrapItem(scrapy.Item):
    website = scrapy.Field()
    title = scrapy.Field()
    chapter = scrapy.Field()
    update_time = scrapy.Field()
