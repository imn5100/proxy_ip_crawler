# -*- coding: utf-8 -*-

import threading
import time
import requests


class ProxyCheck(threading.Thread):
    def __init__(self, proxyList, checkedProxyList):
        threading.Thread.__init__(self)
        self.checkedProxyList = checkedProxyList
        self.proxyList = proxyList
        self.timeout = 5
        self.testUrl = "http://www.baidu.com/"
        # 百度ICP证,能正常获取说明代理网络连接成功
        self.testStr = "030173"

    def checkProxyByRequests(self):
        session = requests.Session()
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36"}
        for proxy in self.proxyList:
            proxies = {
                "http": r"http://%s:%s" % (proxy['ip'], proxy['port'])
            }
            t1 = time.time()
            try:
                r = session.get(self.testUrl, headers=headers, proxies=proxies, timeout=self.timeout)
                time_used = time.time() - t1
                result = r.content
                pos = result.find(self.testStr)
                if pos > 1:
                    proxy['speed'] = time_used
                    self.checkedProxyList.append(proxy)
                else:
                    continue
            except Exception:
                continue

    def run(self):
        self.checkProxyByRequests()

    @staticmethod
    def checkIpList(ip_list, thread_num=20):
        filter_list = []
        if len(ip_list) == 0:
            return filter_list
        ip_list_size = len(ip_list)
        checkThreads = []
        if not thread_num or thread_num <= 0:
            thread_num = 20
        if ip_list_size <= thread_num:
            for i in range(ip_list_size):
                t = ProxyCheck(ip_list[i], filter_list)
                checkThreads.append(t)
        else:
            size = ip_list_size / thread_num
            for i in range(thread_num):
                if i == thread_num - 1:
                    t = ProxyCheck(ip_list[i * size:], filter_list)
                else:
                    t = ProxyCheck(ip_list[i * size: (i + 1) * size], filter_list)
                checkThreads.append(t)
        for t in checkThreads:
            t.start()
        for t in checkThreads:
            t.join()
        return filter_list
