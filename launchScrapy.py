# encoding=utf-8
from scrapy import cmdline

if __name__ == '__main__':
    cmdline.execute('scrapy crawl proxy_ip'.split())
