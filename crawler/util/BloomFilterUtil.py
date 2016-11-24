# -*- coding: utf-8 -*-
import os

from pybloom import BloomFilter


def filter_proxy_ip(items):
    rfile = None
    try:
        if not os.path.isfile("proxy_ip.bloom"):
            bf = BloomFilter(10000, 0.001)
        else:
            rfile = open("proxy_ip.bloom", 'r')
            bf = BloomFilter.fromfile(rfile)
        filter_items = []
        for item in items:
            key = item['ip'] + ":" + str(item['port'])
            if key in bf:
                print (key + " is exited")
                continue
            else:
                bf.add(key)
                filter_items.append(item)
        bf.tofile(open('proxy_ip.bloom', 'w+'))
    except Exception, e:
        raise e
    finally:
        if rfile:
            rfile.close()
    return filter_items


if __name__ == '__main__':
    if not os.path.isfile("proxy_ip.bloom"):
        bf = BloomFilter(10000, 0.001)
    else:
        rwfile = open("proxy_ip.bloom", 'r')
        bf = BloomFilter.fromfile(rwfile)
    # for i in range(20, 40, 2):
    #     bf.add(i)
    for i in range(25):
        print(i in bf)
    bf.tofile(open('proxy_ip.bloom', 'w+'))
