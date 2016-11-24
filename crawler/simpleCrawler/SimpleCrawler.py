# -*- coding: utf-8 -*-
import threading
import HtmlDownloader
import HtmlParser


class Simple_Crawler(threading.thread):
    def __init__(self, parser):
        threading.Thread.__init__(self)
        self.parser = parser

    def run(self):
        self.parser.urls
