# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb

from crawler.sqliteClient.IPProxy import IPProxy


class CrawlerPipeline(object):
    dbClient = None
    mysql_conf = ""
    mysql_conn = None

    def process_item(self, item, spider):
        save_mode = spider.settings.get("SAVE_MODE")
        if save_mode == 'mysql':
            self.process_item_mysql(item, spider)
        else:
            self.process_item_sqlite(item, spider)

    def __del__(self):
        if self.dbClient:
            self.dbClient.disconnect();
        if self.mysql_conn:
            self.mysql_conn.close()

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
            "insert into proxy_ip(ip,port,http_type,position,speed,connect_time,check_time) values(%s,%s,%s,%s,%s,%s,%s)")
        item_list = (item['ip'], item['port'], item['http_type'], item['position'], item['speed'], item['connect_time'],
                     item['check_time'])
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