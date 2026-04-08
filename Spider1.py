import scrapy
import scrapy.crawler as crawler
from bs4 import BeautifulSoup

from scrapy.crawler import CrawlerProcess


class Spider1   (scrapy.Spider):
    name = 'my_morizon_spider'

    custom_settings = {
        'DOWNLOAD_DELAY': '2.0',
        'ROBOTSTXT_OBEY': False,
        'AUTOTHROTTLE_ENABLED': True,
        'USER_AGENT': 'Mozilla/5.0'
    }

    top_url = 'https://www.morizon.pl/'

    async def start(self):
        urls = [
            'https://www.morizon.pl/mieszkania/warszawa/',
            'https://www.morizon.pl/mieszkania/warszawa/?page=2',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        self.logger.info('1. Got successful response from {}'.format(response.url))
