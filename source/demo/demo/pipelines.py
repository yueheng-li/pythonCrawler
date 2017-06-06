# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import signals
import json
import codecs
from twisted.enterprise import adbapi
from datetime import datetime
import MySQLdb
import MySQLdb.cursors

class DemoPipeline(object):
    def process_item(self, item, spider):
        return item


class JsonWithEncodingYodobashiPipeline(object):
    def __init__(self):
        self.file = codecs.open('data.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item

    def spider_closed(self, spider):
        self.file.close()


class MySQLStoreYodobashiPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbargs = dict(
            host=settings['MYSQL_HOST'],
            port=settings['MYSQL_PORT'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
        return cls(dbpool)

    # pipeline默认调用
    def process_item(self, item, spider):
        d = self.dbpool.runInteraction(self._do_upinsert, item, spider)
        d.addErrback(self._handle_error, item, spider)
        d.addBoth(lambda _: item)
        return d

    # 将每行更新或写入数据库中
    def _do_upinsert(self, conn, item, spider):
        #now = datetime.utcnow().replace(microsecond=0).isoformat(' ')

        if spider.name == 'YamadaSpider':
            site = '2'
        elif spider.name == 'AmazonSpider':
            site = '3'
        elif spider.name == 'RakutenSpider':
            site = '4'
        else:
            site = '1'
        conn.execute("""
                select 1 from price where product_name = %s and site = %s
        """, (item['productName'], site))
        ret = conn.fetchone()

        if ret:

            print """
                update price set price = %s, point = %s where product_name = %s and site = %s
            """, (item['price'], item['point'], item['productName'], site)

            conn.execute("""
                update price set price = %s, point = %s where product_name = %s and site = %s
            """, (item['price'], item['point'], item['productName'], site))

        else:

            print """
                insert into price(site, product_name, price, point)
                values(%s, %s, %s, %s)
            """, (site, item['productName'], item['price'], item['point'])

            conn.execute("""
                insert into price(site, product_name, price, point)
                values(%s, %s, %s, %s)
            """, (site, item['productName'], item['price'], item['point']))

    # 异常处理
    def _handle_error(self, failure, item, spider):
        spider.logger.err(failure)
