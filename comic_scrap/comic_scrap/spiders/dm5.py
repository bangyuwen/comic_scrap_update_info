# -*- coding: utf-8 -*-
import scrapy
import pytz
from datetime import datetime, timedelta


class Dm5Spider(scrapy.Spider):
    name = 'dm5'
    allowed_domains = ['dm5.com']
    start_urls = ['http://www.dm5.com/manhua-new/']

    def parse(self, response):
        comics = response.css("div.mh-item-detali")
        today = (
            datetime.now(pytz.timezone('Asia/Taipei'))
            .replace(hour=0, minute=0, second=0, microsecond=0)
        )

        for comic in comics:
            title = comic.css("h2.title a::text").extract_first()
            chapter = comic.css("p.chapter a::text").extract_first().strip()
            update_time = comic.css("p.zl::text").extract_first().strip()
            time = timedelta(hours=1)
            yield {
                "website": "dm5",
                "title": title,
                "chapter": chapter,
                "update_time": update_time
            }
