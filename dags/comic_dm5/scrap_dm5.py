# -*- coding: utf-8 -*-
import re
import logging
import csv
import os
from datetime import datetime, time, timedelta
from time import sleep
from typing import List

import pytz
from selenium import webdriver
from scrapy.selector import Selector

logging.basicConfig(format='[%(levelname)s] %(message)s', level=logging.INFO)

store = []


def parse_comic(comic: dict, now):
    try:
        chapter = comic['chapter'].strip() if comic['chapter'] else ''
        chapter_num = re.search(r"\d+|$", chapter)
        return({
            'website': 'dm5',
            'title': comic['title'],
            'chapter_num': chapter_num.group(0) if chapter_num else '',
            'chapter_title': (chapter.split(r" ", maxsplit=1) + [''])[1],
            'update_time': parse_datetime(comic['update_time'], now)
        })
    except Exception:
        print(f"Error Parse on {comic['title']}")
        raise


def parse_datetime(datetime_str: str, now):
    if datetime_str:
        if '昨天' in datetime_str:
            hour, minute = map(int, re.findall(r'\d\d', datetime_str))
            yesterday = now.date() - timedelta(days=1)
            no_timezone_datetime = datetime.combine(
                yesterday, time(hour, minute))
            timezone_datetime = pytz.timezone(
                'Asia/Shanghai').localize(no_timezone_datetime)
            return timezone_datetime.strftime('%s')
        return datetime_str
    return ''


def write_csv(path: str, data: List[dict]):
    folder = os.path.dirname(path)
    os.makedirs(folder, exist_ok=True)
    with open(path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['website', 'title', 'chapter_num', 'chapter_title', 'update_time']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for datum in data:
            writer.writerow(datum)


def run():
    # need to install chrome too
    module_dir = os.path.dirname(os.path.abspath(__file__))
    chrome_options = webdriver.chrome.options.Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_driver_path = f'{module_dir}/chromedriver'
    logging.info(f'chrome driver: {chrome_driver_path}')
    with webdriver.Chrome(chrome_driver_path, chrome_options=chrome_options) as driver:
        driver.get('http://www.dm5.com/manhua-new/')
        logging.info('Click Yesterday.')
        yesterday_button = driver.find_element_by_xpath(
            '//a[@class="bt_daykey" and @daylabel="昨天"]')
        yesterday_button.click()

        logging.info('Wait for JS to run')
        sleep(3)
        response = Selector(text=driver.page_source)

    datetime_now = datetime.now(pytz.timezone('Asia/Shanghai'))
    yesterday_month_day = (datetime_now - timedelta(days=1)).strftime('%-d')
    yesterday_comics = response.xpath(
        f'.//ul[@id="update_{yesterday_month_day}"]//div[@class="mh-item-detali"]')

    for comic in yesterday_comics:
        comic_info = {
            'website': 'dm5',
            'title': comic.xpath('.//h2[@class="title"]/a/text()').extract_first(),
            'chapter': comic.xpath('.//p[@class="chapter"]/a/text()').extract_first(),
            'update_time': comic.xpath('.//p[@class="zl"]/text()').extract_first()
        }
        comic_formated = parse_comic(comic_info, datetime_now)
        store.append(comic_formated)

    yesterday_date = (datetime_now - timedelta(days=1)).strftime('%Y%m%d')
    write_csv(f'/tmp/scrap_dm5/{yesterday_date}.csv', store)
    logging.info('Finished')


if __name__ == '__main__':
    run()
