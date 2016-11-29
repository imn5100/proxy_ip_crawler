# -*- coding: utf-8 -*-
from crawler.items import CrawlerItem
from crawler.sqliteClient.sqliteOperator import Table


class IPProxy(Table):
    def __init__(self, data_file):
        super(IPProxy, self).__init__(data_file, 'proxy_ip',
                                      ['id INTEGER PRIMARY KEY AUTOINCREMENT',
                                       'ip VARCHAR(15) NOT NULL',
                                       'port CHAR(5) NOT NULL',
                                       'protocol VARCHAR(20) DEFAULT NULL',
                                       'area VARCHAR(45) NOT NULL',
                                       'speed FLOAT(4,3) NOT NULL'])

    def select(self, *args, **kwargs):
        cursor = super(IPProxy, self).select(*args, **kwargs)
        results = cursor.fetchall()
        cursor.close()
        return IPProxy.convert(results)

    def select_all(self, *args, **kwargs):
        cursor = super(IPProxy, self).select_all(*args, **kwargs)
        results = cursor.fetchall()
        cursor.close()
        return IPProxy.convert(results)

    def insert(self, *args):
        """当只有一个参数时，默认为插入的是对象，从对象中取值"""
        if 1 == len(args):
            item = args[0]
            self.free(super(IPProxy, self).insert(None, item['ip'], item['port'], item['protocol'], item['area'],
                                                  item['speed']))
            return
        self.free(super(IPProxy, self).insert(*args))

    def update(self, set_args, **kwargs):
        self.free(super(IPProxy, self).update(set_args, **kwargs))

    def delete(self, **kwargs):
        self.free(super(IPProxy, self).delete(**kwargs))

    def delete_all(self):
        self.free(super(IPProxy, self).delete_all())

    def drop(self):
        self.free(super(IPProxy, self).drop())

    def insertMany(self, items):
        cursor = self.db.cursor()
        sql = "INSERT INTO %s VALUES(%s)" % ("proxy_ip", ",".join("?" * 6))
        try:
            args = []
            for item in items:
                item_list = (None, item['ip'], item['port'], item['protocol'], item['area'], item['speed'])
                args.append(item_list)
            cursor.executemany(sql, args)
            self.db.commit()
        except Exception, e:
            raise e
        finally:
            cursor.close()
        return cursor

    @staticmethod
    def convert(result):
        ip_list = []
        for tu in result:
            item = CrawlerItem()
            item['ip'] = tu[1]
            item['port'] = tu[2]
            item['protocol'] = tu[3]
            item['area'] = tu[4]
            item['speed'] = tu[5]
            ip_list.append(item)
        return ip_list


if __name__ == '__main__':
    ipproxy2 = IPProxy("/Project/mygit/myCrawler/proxy_ip_crawler/proxy_ip.dat")
    items = ipproxy2.select_all('*')
    for item in items:
        print(item)
