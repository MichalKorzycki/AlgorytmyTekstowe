import scrapy
import scrapy.crawler as crawler
from bs4 import BeautifulSoup

from scrapy.crawler import CrawlerProcess


class Spider2(scrapy.Spider):
    name = 'my_morizon_spider'
    start_urls = [
        'https://www.morizon.pl/mieszkania/warszawa/'
    ]

    custom_settings = {
        'DOWNLOAD_DELAY': '4.0',
        'ROBOTSTXT_OBEY': False,
        'AUTOTHROTTLE_ENABLED': True,
        'USER_AGENT': 'My Morizon Demo Bot (michal.korzycki@gmail.com)'
    }

    top_url = 'https://www.morizon.pl'

    async def start(self):
        urls = [
            'https://www.morizon.pl/mieszkania/warszawa/',
            'https://www.morizon.pl/mieszkania/warszawa/?page=2',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        self.logger.info('Got successful response from {}'.format(response.url))
        soup = BeautifulSoup(response.body, 'html.parser')

        links = [link.get('href')
                 for link in soup.find_all('a')]

        links = [link for link in links if link.startswith('/oferta/')]
        print(links)

        for item_url in links:
            yield scrapy.Request(url=self.top_url+item_url, callback=self.parse_item)

    def parse_item(self,
                   response):  # item_url - odwiedzanie strony, #self.parse_item - przetworzenie przy pomocy funkcji
        self.logger.info('Got successful response from {}'.format(response.url))
