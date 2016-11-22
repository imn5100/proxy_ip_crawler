# -*- coding: utf-8 -*-
import scrapy
from crawler.items import CrawlerItem

class ProxyIpSpider(scrapy.Spider):
    name = "proxy_ip"
    allowed_domains = ["xicidaili.com"]
    start_urls = (
        'http://www.xicidaili.com',
    )

    def start_requests(self):
        '''需爬取的链接'''
        reqs = []

        for i in range(1,2):
            req = scrapy.Request("http://www.xicidaili.com/nn/%s"%i)
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
            item['position'] = tr.xpath('string(td[4])')[0].extract().strip()
            item['http_type'] = tr.xpath('td[6]/text()')[0].extract()
            item['speed'] = tr.xpath('td[7]/div[@class="bar"]/@title').re('\d{0,2}\.\d{0,}')[0]
            item['connect_time'] = tr.xpath('td[8]/div[@class="bar"]/@title').re('\d{0,2}\.\d{0,}')[0]
            item['check_time'] = tr.xpath('td[10]/text()')[0].extract()

            items.append(item)

        return items

