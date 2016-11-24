# -*- coding: utf-8 -*-
import redis
import hashlib


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
        str_input = RedisBloomFilter.hexdigestStr(str_input)
        name = self.key + str(int(str_input[0:2], 16) % self.blockNum)
        for f in self.hashfunc:
            loc = f.hash(str_input)
            ret = ret & self.server.getbit(name, loc)
        return ret

    def insert(self, str_input):
        str_input = RedisBloomFilter.hexdigestStr(str_input)
        name = self.key + str(int(str_input[0:2], 16) % self.blockNum)
        for f in self.hashfunc:
            loc = f.hash(str_input)
            self.server.setbit(name, loc, 1)

    @classmethod
    def hexdigestStr(cls, val):
        fp = hashlib.sha1()
        fp.update(val)
        return fp.hexdigest()


if __name__ == '__main__':
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
