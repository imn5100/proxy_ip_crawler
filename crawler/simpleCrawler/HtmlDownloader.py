# -*- coding: utf-8 -*-

import requests
from crawler.simple_crawler_config import *


class HtmlDownloader(object):
    @classmethod
    def download(cls, url, encoding='utf-8'):
        count = 0  # 失败重试次数
        while count <= RETRY_TIME:
            try:
                r = requests.get(url=url, headers=SIMPLE_CRAWLER_HEADER, timeout=TIMEOUT)
                r.encoding = encoding
                if (not r.ok) or len(r.content) < 300:
                    count += 1
                    continue
                else:
                    return r.text
            except Exception, e:
                count += 1
                continue
        return None
