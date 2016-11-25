# -*- coding: utf-8 -*-
import threading
import HtmlDownloader
import HtmlParser


class SimpleCrawler(threading.Thread):
    def __init__(self, parser, url, item_list):
        """一个线程负责一个url的拉取和数据转换"""
        threading.Thread.__init__(self)
        self.parser = parser
        self.url = url
        self.item_list = item_list

    def run(self):
        response_text = None
        try:
            if self.parser.has_key('encoding'):
                response_text = HtmlDownloader.HtmlDownloader.download(self.url, self.parser['encoding'])
            else:
                response_text = HtmlDownloader.HtmlDownloader.download(self.url)
            if response_text:
                datas = HtmlParser.HtmlParser.parse(response_text, self.parser)
                if len(datas):
                    self.item_list.extend(datas)
                    print(self.url + "  :crawler end")
                else:
                    print(self.url + "  :can't parse")
            else:
                print(self.url + "  :response_text is null")
        except Exception, e:
            print(e.message)
