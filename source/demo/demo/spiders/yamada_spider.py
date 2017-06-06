# -*- coding: utf-8 -*-

from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor as sle
from scrapy.spiders import CrawlSpider, Rule
from demo.items import *

class YamadaSpider(CrawlSpider):
    name = "YamadaSpider"
    allowed_domains = ["yamada-denkiweb.com"]
    start_urls = [
        #"http://www.yamada-denkiweb.com/search/エレコム",
        "http://www.yamada-denkiweb.com/search/EHP-CH1010AGD",
        "http://www.yamada-denkiweb.com/search/ZSB-IBUB02BK",
    ]

    def parse(self, response):
        items = []
        sel = Selector(response)

        htmlProductName = sel.css('p.item-name')
        htmlInfo = sel.css('div.item-price-box')

        for index in range(len(htmlProductName)):
            item = DemoItem()

            item['productName'] = htmlProductName[index].xpath('a/text()').extract_first()

            item['price'] = htmlInfo[index].xpath('p')[0].css('span.highlight').xpath('text()').extract_first()

            # ¥5,906=>5906
            item['price'] = item['price'].replace(unicode("¥", "utf-8"), '')
            item['price'] = item['price'].replace(',', '')

            item['point'] = htmlInfo[index].xpath('p')[1].css('span.highlight').xpath('text()').extract_first()
            items.append(item)
        return items
