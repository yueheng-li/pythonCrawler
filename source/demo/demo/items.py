# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DemoItem(scrapy.Item):
    # define the fields for your item here like:
    productName = scrapy.Field()
    price = scrapy.Field()
    point = scrapy.Field()
    pass

'''
    def __unicode__(self):
        return repr(self).decode('unicode_escape')
'''