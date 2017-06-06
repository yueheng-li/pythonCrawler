# -*- coding: utf-8 -*-

from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor as sle
from scrapy.spiders import CrawlSpider, Rule
from django.utils.encoding import smart_str, smart_unicode
from demo.items import *

class YodobashiSpider(CrawlSpider):
    name = "YodobashiSpider"
    allowed_domains = ["yodobashi.com"]
    start_urls = [
        #"http://www.yodobashi.com/?word=エレコム",
        "http://www.yodobashi.com/?word=EHP-CH1010AGD",
        "http://www.yodobashi.com/?word=ZSB-IBUB02BK",
    ]
    '''
    rules = [
        Rule(sle(allow=("/p\d{1,}/\?word=EHP-CH1010AGD")),
             follow=True,
             callback='parse_item')
    ]
    '''

    def parse(self, response):
        items = []
        sel = Selector(response)

        htmlProductName = sel.css('div.pName')
        htmlInfo = sel.css('div.pInfo')

        for index in range(len(htmlProductName)):
            item = DemoItem()

            item['productName'] = htmlProductName[index].xpath('p[2]/text()').extract_first()

            item['price'] = htmlInfo[index].css('span.productPrice')[0].xpath('text()').extract_first()

            # ￥6,760=>6760
            item['price'] = item['price'].replace(unicode("￥", "utf-8"), '')
            item['price'] = item['price'].replace(',', '')

            item['point'] = htmlInfo[index].css('span.orange')[0].xpath('text()').extract_first()
            items.append(item)
        return items
