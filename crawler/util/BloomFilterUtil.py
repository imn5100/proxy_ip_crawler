# -*- coding: utf-8 -*-
import os

from pybloom import BloomFilter


class FileBloomFilter(object):
    def __init__(self, path):
        self.path = path
        self.rfile = None
        self.is_tofile = False
        if not os.path.isfile(path):
            self.bf = BloomFilter(100000, 0.001)
        else:
            self.rfile = open(path, 'r')
            self.bf = BloomFilter.fromfile(self.rfile)

    def __del__(self):
        if not self.is_tofile:
            self.tofile()
        if self.rfile:
            self.rfile.close()

    def tofile(self):
        if self.bf:
            wfile = open(self.path, 'w+')
            self.bf.tofile(wfile)
            wfile.close()
            self.is_tofile = True

    def have(self, item):
        key = item['ip'] + ":" + str(item['port'])
        if key in self.bf:
            return True
        else:
            return False

    def filter_proxy_ip_list(self, items):
        filter_items = []
        for item in items:
            if not self.have(item):
                filter_items.append(item)
        return filter_items

    def add_proxy_ip(self, item):
        key = item['ip'] + ":" + str(item['port'])
        self.bf.add(key)
        self.is_tofile = False

    def add_proxy_ip_all(self, items):
        for item in items:
            self.add_proxy_ip(item)

# if __name__ == '__main__':
#     item = {}
#     item['ip'] = "192.168.10.1"
#     item['port'] = 1024
#     item2 = {}
#     item2['ip'] = "192.168.10.2"
#     item2['port'] = 1021
#     item3 = {}
#     item3['ip'] = "192.168.10.3"
#     item3['port'] = 1024
#     item4 = {}
#     item4['ip'] = "10.1.1.1"
#     item4['port'] = 1111
#     item_list = [item, item2, item3, item4]
#     item_list2 = [item, item2, item3]
#     fbf = FileBloomFilter("filter.bloom")
#     fbf.add_proxy_ip_all(item_list2)
#     print(fbf.have(item2))
#     print(fbf.have(item4))
#     print(fbf.filter_proxy_ip_list(item_list))
