# -*- coding: utf-8 -*-

from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor as sle
from scrapy.spiders import CrawlSpider, Rule
from demo.items import *

class RakutenSpider(CrawlSpider):
    name = "RakutenSpider"
    allowed_domains = ["rakuten.co.jp"]
    start_urls = [
        #"http://search.rakuten.co.jp/search/mall/エレコム",
        "http://search.rakuten.co.jp/search/mall/EHP-CH1010AGD",
        "http://search.rakuten.co.jp/search/mall/ZSB-IBUB02BK",
    ]

    def parse(self, response):
        items = []
        sel = Selector(response)

        htmlProductName = sel.css('div.rsrSResultSect').css('div.rsrSResultItemTxt')
        htmlInfo = sel.css('div.rsrSResultSect').css('div.rsrSResultItemInfo')

        for index in range(len(htmlProductName)):
            item = DemoItem()

            item['productName'] = htmlProductName[index].xpath('h2/a/text()').extract_first()

            item['price'] = htmlInfo[index].css('p.price').xpath('a/text()').extract_first()

            # 6,145=>6145
            item['price'] = item['price'].replace(',', '')

            item['point'] = ''
            items.append(item)
        return items
