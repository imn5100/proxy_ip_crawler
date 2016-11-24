# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs

import MySQLdb
import json

from crawler.sqliteClient.IPProxy import IPProxy


class CrawlerPipeline(object):
    def __init__(self):
        self.dbClient = None
        self.mysql_conf = ""
        self.mysql_conn = None
        self.file = None

    def spider_closed(self, spider):
        print('spider closed,Release resource')
        if self.dbClient:
            self.dbClient.disconnect()
        if self.mysql_conn:
            self.mysql_conn.close()
        if self.file:
            self.file.close()

    def process_item(self, item, spider):
        save_mode = spider.settings.get("SAVE_MODE")
        if save_mode == 'mysql':
            self.process_item_mysql(item, spider)
        elif save_mode == 'sqlite':
            self.process_item_sqlite(item, spider)
        else:
            self.process_item_json(item, spider)

    def process_item_sqlite(self, item, spider):
        try:
            if not self.dbClient:
                self.dbClient = IPProxy(spider.settings.get('SQLITE_FILE'))
            self.dbClient.insert(item)
        except Exception, e:
            print "Insert error:", e
        return item

    def process_item_mysql(self, item, spider):
        if self.mysql_conf == "" or not self.mysql_conn:
            self.mysql_conf = spider.settings.get('MYSQL_CONNECT')
            self.mysql_conn = MySQLdb.connect(**self.mysql_conf)
        cur = self.mysql_conn.cursor()
        sql = (
            "insert into proxy_ip(ip,port,protocol,area,speed) values(%s,%s,%s,%s,%s)")
        item_list = (item['ip'], item['port'], item['protocol'], item['area'], item['speed'])
        try:
            cur.execute(sql, item_list)
        except Exception, e:
            print "Insert error:", e
            self.mysql_conn.rollback()
        else:
            self.mysql_conn.commit()
        finally:
            cur.close()
        return item

    def process_item_json(self, item, spider):
        try:
            if not self.file:
                self.file = codecs.open(spider.settings.get('JSON_FILE'), 'a', encoding='utf-8')
            line = json.dumps(dict(item), ensure_ascii=False) + "\n"
            self.file.write(line)
        except Exception, e:
            print "write json file  error:", e
        return item
