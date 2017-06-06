# -*- coding: utf-8 -*-

from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor as sle
from scrapy.spiders import CrawlSpider, Rule
from demo.items import *

class AmazonSpider(CrawlSpider):
    name = "AmazonSpider"
    allowed_domains = ["amazon.co.jp"]
    start_urls = [
        # 検索の時、「-」から「－」へ変換の処理がある
        #"https://www.amazon.co.jp/s/ref=nb_sb_noss_1?__mk_ja_JP=カタカナ&url=search-alias%3Daps&field-keywords=エレコム&rh=i%3Aaps%2Ck%3Aエレコム",
        "https://www.amazon.co.jp/s/ref=nb_sb_noss?__mk_ja_JP=カタカナ&url=search-alias%3Daps&field-keywords=EHP－CH1010AGD&rh=i%3Aaps%2Ck%3AEHP－CH1010AGD",
        "https://www.amazon.co.jp/s/ref=nb_sb_noss?__mk_ja_JP=カタカナ&url=search-alias%3Daps&field-keywords=ZSB-IBUB02BK&rh=i%3Aaps%2Ck%3AZSB-IBUB02BK",
    ]

    def parse(self, response):
        items = []
        sel = Selector(response)

        htmlResult= sel.xpath('//div[@id="centerMinus"]/div[@id="atfResults"]/ul/li')

        for index in range(len(htmlResult)):
            item = DemoItem()

            htmlInfo = htmlResult[index].xpath('div[1]/div[@class="a-row a-spacing-mini"]')
            # 「お得」の商品にとって、長さ＝３．以外の商品、長さ＝２
            if len(htmlInfo) == 3:
                htmlDiv = htmlInfo[2]
            else:
                htmlDiv = htmlInfo[1]

            item['productName'] = htmlInfo[0].xpath('div[1]/a/h2/text()').extract_first()
            item['price'] = htmlDiv.xpath('div[1]/a/span[2]/text()').extract_first()

            # ￥ 6,145=>6145
            item['price'] = item['price'].replace(unicode("￥ ", "utf-8"), '')
            item['price'] = item['price'].replace(',', '')

            if htmlDiv.xpath('div[2]/div[1]/span[3]'):
                item['point'] = htmlDiv.xpath('div[2]/div[1]/span[3]/text()').extract_first()
            else:
                item['point'] = ''
            items.append(item)
        return items
