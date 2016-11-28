# -*- coding: utf-8 -*-
import random
import threading
import HtmlDownloader
import HtmlParser
import time


class SimpleCrawler(threading.Thread):
    # 默认延迟1s起
    delay = 1

    def __init__(self, parser, url, item_list):
        """一个线程负责一个url的拉取和数据转换"""
        threading.Thread.__init__(self)
        self.parser = parser
        self.url = url
        self.item_list = item_list

    def run(self):
        response_text = None
        try:
            if self.parser.has_key('delayStep'):
                """某些网站需要设置延时爬取"""
                SimpleCrawler.delay += self.parser['delayStep']
                print(self.url + "  delay:" + str(SimpleCrawler.delay))
                time.sleep(SimpleCrawler.delay)
            if self.parser.has_key('encoding'):
                """某些非utf-8编码网站需要手动设置编码"""
                response_text = HtmlDownloader.HtmlDownloader.download(self.url, self.parser['encoding'])
            else:
                response_text = HtmlDownloader.HtmlDownloader.download(self.url)
            if response_text:
                datas = HtmlParser.HtmlParser.parse(response_text, self.parser)
                if len(datas) > 0:
                    self.item_list.extend(datas)
                    print(self.url + "  end")
                else:
                    print(self.url + "  can't parse")
            else:
                print(self.url + "  response is null")
        except Exception, e:
            print(e.message)
