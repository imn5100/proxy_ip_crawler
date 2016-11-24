# -*- coding: utf-8 -*-
from lxml import etree


class Html_Parser(object):
    @classmethod
    def parse(cls, response, parser):
        datas = []
        root = etree.HTML(response)
        trs = root.xpath(parser['position'])
        for tr in trs:
            try:
                ip = tr.xpath(parser['detail']['ip'])[0].text
                port = tr.xpath(parser['detail']['port'])[0].text
                area = tr.xpath(parser['detail']['area'])[0].text
                protocol = ''
                if len(parser['detail']['protocol']) > 0:
                    protocol = tr.xpath(parser['detail']['protocol'])[0].text
                proxy_ip = {'ip': ip, 'port': port, 'area': area, 'protocal': protocol}
                datas.append(proxy_ip)
            except Exception, e:
                continue
        return datas
