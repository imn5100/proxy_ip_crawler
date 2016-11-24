# -*- coding: utf-8 -*-
import codecs
import hashlib
import os
import redis

from pybloom import BloomFilter


def filter_proxy_ip(items):
    rfile = None
    try:
        if not os.path.isfile("proxy_ip.bloom"):
            bf = BloomFilter(10000, 0.001)
        else:
            rfile = codecs.open("proxy_ip.bloom", 'r')
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


class SimpleHash(object):
    def __init__(self, cap, seed):
        self.cap = cap
        self.seed = seed

    def hash(self, value):
        ret = 0
        for i in range(len(value)):
            ret += self.seed * ret + ord(value[i])
        return (self.cap - 1) & ret


class RedisBloomFilter(object):
    def __init__(self, server, key, blockNum=1):
        # bloom 长度
        self.bit_size = 1 << 12  # 2^12 1M容量
        # 5组种子数，5总hash算法
        self.seeds = [5, 7, 11, 13, 31]
        # redis server
        self.server = server
        # redis bloom key
        self.key = key
        # Redis String 最大为512M，超过需要分块
        self.blockNum = blockNum
        # hash算法数组
        self.hashfunc = []
        for seed in self.seeds:
            self.hashfunc.append(SimpleHash(self.bit_size, seed))

    def isContains(self, str_input):
        if not str_input:
            return False
        ret = True

        name = self.key + str(int(str_input[0:2], 16) % self.blockNum)
        for f in self.hashfunc:
            loc = f.hash(str_input)
            ret = ret & self.server.getbit(name, loc)
        return ret

    def insert(self, str_input):
        name = self.key + str(int(str_input[0:2], 16) % self.blockNum)
        for f in self.hashfunc:
            loc = f.hash(str_input)
            self.server.setbit(name, loc, 1)


'''
以下为测试
'''


def test_pybloom():
    if not os.path.isfile("proxy_ip.bloom"):
        bf = BloomFilter(10000, 0.001)
    else:
        rwfile = codecs.open("proxy_ip.bloom", 'r')
        bf = BloomFilter.fromfile(rwfile)
    for i in range(20, 40, 2):
        bf.add(i)
    for i in range(25):
        print(i in bf)
    bf.tofile(open('proxy_ip.bloom', 'w+'))


def test_redis_bloom():
    rconn = redis.Redis('127.0.0.1', 6379)
    bf = RedisBloomFilter(rconn, 'spider_1:dupefilter')
    url = b"https://shawblog.me"
    fp = hashlib.sha1()
    fp.update(url)
    if bf.isContains(fp.hexdigest()):
        print 'exist!'
    else:
        bf.insert(fp.hexdigest())
        print 'not exist!'


if __name__ == '__main__':
    test_redis_bloom()
