# -*- coding: utf-8 -*-
from crawler.items import CrawlerItem
from crawler.sqliteClient.sqliteOperator import Table


class IPProxy(Table):
    def __init__(self, data_file):
        super(IPProxy, self).__init__(data_file, 'dy_proxy',
                                      ['id INTEGER PRIMARY KEY AUTOINCREMENT',
                                       'ip VARCHAR(15) NOT NULL',
                                       'port CHAR(5) NOT NULL',
                                       'http_type VARCHAR(5) DEFAULT NULL',
                                       'position VARCHAR(45) NOT NULL',
                                       'speed FLOAT(4,3) NOT NULL',
                                       'connect_time FLOAT(4,3) NOT NULL',
                                       'check_time VARCHAR(40) DEFAULT NULL'])

    def select(self, *args, **kwargs):
        cursor = super(IPProxy, self).select(*args, **kwargs)
        results = cursor.fetchall()
        cursor.close()
        return results

    def select_all(self, *args, **kwargs):
        cursor = super(IPProxy, self).select_all(*args, **kwargs)
        results = cursor.fetchall()
        cursor.close()
        return results

    '''当只有一个参数时，默认为插入的是对象，从对象中取值'''

    def insert(self, *args):
        if 1 == len(args):
            item = args[0]
            self.free(super(IPProxy, self).insert(None, item['ip'], item['port'], item['position'], item['http_type'],
                                                  item['speed'],
                                                  item['connect_time'], item['check_time']))
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


if __name__ == '__main__':
    #构造方法参数为存储的sqlite文件
    ipproxy = IPProxy("/Project/mygit/myCrawler/proxy_ip_crawler/ip.dat")
    #查询所有代理ip记录
    for data in ipproxy.select_all('*'):
        print (data[1] + ":" + data[2] + " position:" + data[3])
    #删除sqlite中所有记录
    # ipproxy.delete_all();
    ipproxy.disconnect()
