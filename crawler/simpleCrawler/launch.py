# -*- coding: utf-8 -*-
from crawler import simple_crawler_config
from crawler.simpleCrawler.SimpleCrawler import SimpleCrawler

if __name__ == '__main__':
    parserList = simple_crawler_config.parserList
    crawler_list = []
    items = []
    for site in parserList:
        for url in site['urls']:
            print("start " + url)
            crawler_thread = SimpleCrawler(site, url, items)
            crawler_list.append(crawler_thread)
    for t in crawler_list:
        t.start()
    for t in crawler_list:
        t.join()
    print(len(items))
