# -*- coding: utf-8 -*-
import re
import unittest
from datetime import datetime, time, timedelta
from time import sleep

import pytz
import scrapy
from selenium import webdriver
from scrapy.selector import Selector


class Dm5Spider(scrapy.Spider):
    name = 'dm5'
    allowed_domains = ['dm5.com']
    start_urls = ['http://www.dm5.com/manhua-new/']

    def parse(self, response):
        self.driver = webdriver.Chrome('/Users/bangyuwen/chromedriver')
        self.driver.get(self.start_urls[0])

        self.logger.info('Click Yesterday.')
        yesterday_button = self.driver.find_element_by_xpath(
            '//a[@class="bt_daykey" and @daylabel="昨天"]')
        yesterday_button.click()

        sleep(3)

        datetime_now = datetime.now(pytz.timezone('Asia/Shanghai'))
        yesterday_date = (datetime_now - timedelta(days=1)).strftime('%d')
        response = Selector(text=self.driver.page_source)
        yesterday_comics = response.xpath(f'.//ul[@id="update_{yesterday_date}"]//div[@class="mh-item-detali"]')
        for comic in yesterday_comics:
            yield Dm5Spider.parse_comic({
                'website': 'dm5',
                'title': comic.xpath('.//h2[@class="title"]/a/text()').extract_first(),
                'chapter': comic.xpath('.//p[@class="chapter"]/a/text()').extract_first(),
                'update_time': comic.xpath('.//p[@class="zl"]/text()').extract_first()
            })
        self.driver.quit()

    @staticmethod
    def parse_comic(comic: dict):
        try:
            chapter = comic['chapter'].strip() if comic['chapter'] else ''
            chapter_num = re.search(r"\d+|$", chapter)
            return({
                'website': 'dm5',
                'title': comic['title'],
                'chapter_num': chapter_num.group(0) if chapter_num else '',
                'chapter_title': (chapter.split(r" ", maxsplit=1) + [''])[1],
                'update_time': Dm5Spider.parse_datetime(comic['update_time'])
            })
        except Exception:
            print(f"Error Parse on {comic['title']}")
            raise

    @staticmethod
    def parse_datetime(datetime_str: str):
        if datetime_str:
            if '昨天' in datetime_str:
                hour, minute = map(int, re.findall(r'\d\d', datetime_str))
                yesterday = datetime.now(pytz.timezone('Asia/Shanghai')).date() - timedelta(days=1)
                no_timezone_datetime = datetime.combine(yesterday, time(hour, minute))
                timezone_datetime = pytz.timezone('Asia/Shanghai').localize(no_timezone_datetime)
                return timezone_datetime.strftime('%s')
            return datetime_str
        return ''


class test(unittest.TestCase):
    def test_parse_comic(self):
        self.assertEqual(Dm5Spider.parse_comic({
            'website': 'dm5', 'title': '军阀霸宠：纯情妖女火辣辣',
            'chapter': '最新第52話', 'update_time': '今天 02:06更新'
        }), {
            'website': 'dm5',
            'title': '军阀霸宠：纯情妖女火辣辣',
            'chapter_num': '52',
            'chapter_title': '',
            'update_time': '今天 02:06更新'
        })

    def test_parse_datetime(self):
        self.assertEqual(Dm5Spider.parse_datetime("昨天 16:14更新"), "1532247240")


if __name__ == '__main__':
    unittest.main()
