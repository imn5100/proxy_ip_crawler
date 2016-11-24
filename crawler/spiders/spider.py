# -*- coding: utf-8 -*-

import scrapy

from crawler.items import CrawlerItem
from crawler.util import BloomFilterUtil, ProxyCheck


class ProxyIpSpider(scrapy.Spider):
    name = "proxy_ip"
    allowed_domains = ["xicidaili.com"]
    start_urls = (
        'http://www.xicidaili.com',
    )

    def start_requests(self):
        """需爬取的链接"""
        reqs = []
        # 爬取范围 1- 2(不包含)
        for i in range(1, 2):
            req = scrapy.Request("http://www.xicidaili.com/nn/%s" % i)
            reqs.append(req)

        return reqs

    def parse(self, response):
        table = response.xpath('//table[@id="ip_list"]')

        trs = table[0].xpath('tr')
        items = []
        # 0为表头，从 1开始解析
        for tr in trs[1:]:
            item = CrawlerItem()
            item['ip'] = tr.xpath('td[2]/text()')[0].extract()
            item['port'] = tr.xpath('td[3]/text()')[0].extract()
            item['area'] = tr.xpath('string(td[4])')[0].extract().strip()
            item['protocol'] = tr.xpath('td[6]/text()')[0].extract()
            item['speed'] = tr.xpath('td[7]/div[@class="bar"]/@title').re('\d{0,2}\.\d{0,}')[0]

            items.append(item)
        items = BloomFilterUtil.filter_proxy_ip(items)
        return ProxyCheck.ProxyCheck.checkIpList(items, 10)
