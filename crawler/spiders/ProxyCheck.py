# -*- coding: utf-8 -*-

import threading
import urllib2
import time

from crawler.sqliteClient.IPProxy import IPProxy


class ProxyCheck(threading.Thread):
    def __init__(self, proxyList, checkedProxyList):
        threading.Thread.__init__(self)
        self.checkedProxyList = checkedProxyList
        self.proxyList = proxyList
        self.timeout = 5
        self.testUrl = "http://www.baidu.com/"
        # 百度ICP证,能正常获取说明代理网络连接成功
        self.testStr = "030173"

    def checkProxy(self):
        cookies = urllib2.HTTPCookieProcessor()
        for proxy in self.proxyList:
            proxyHandler = urllib2.ProxyHandler({"http": r'http://%s:%s' % (proxy['ip'], proxy['port'])})
            opener = urllib2.build_opener(cookies, proxyHandler)
            opener.addheaders = [('User-Agent',
                                  'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36')]
            t1 = time.time()
            try:
                req = opener.open(self.testUrl, timeout=self.timeout)
                result = req.read()
                timeused = time.time() - t1
                pos = result.find(self.testStr)

                if pos > 1:
                    proxy['speed'] = timeused;
                    self.checkedProxyList.append(proxy)
                else:
                    continue
            except Exception, e:
                continue

    def run(self):
        self.checkProxy()


def checkIpList(ip_list, thread_num):
    filter_list = []
    ip_list_size = len(ip_list);
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


if __name__ == '__main__':
    ipproxy = IPProxy("/Project/mygit/myCrawler/proxy_ip_crawler/proxy_ip.dat")
    ip_list = ipproxy.select_all('*')
    ipproxy.disconnect();
    filter_list = checkIpList(ip_list, 10)
    for item in filter_list:
        print(item)