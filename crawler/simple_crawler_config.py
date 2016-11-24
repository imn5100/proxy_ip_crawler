# -*- coding: utf-8 -*-

# simpleCrawler setting
TIMEOUT = 5
RETRY_TIME = 3
SIMPLE_CRAWLER_HEADER = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    'Connection': 'keep-alive',
    'Accept-Encoding': 'gzip, deflate',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
}
parserList = [
    {
        'urls': ['http://www.xicidaili.com/%s/%s' % (m, n) for m in ['nn', 'nt', 'wn', 'wt'] for n in range(1, 3)],
        'position': ".//*[@id='ip_list']/tr[position()>1]",
        'detail': {'ip': './td[2]', 'port': './td[3]', 'area': './td[5]', 'protocol': './td[6]'}
    },
    {
        'urls': ['http://www.cz88.net/proxy/%s' % m for m in
                 ['index.shtml'] + ['http_%s.shtml' % n for n in range(2, 3)]],
        'position': ".//*[@id='boxright']/div/ul/li[position()>1]",
        'detail': {'ip': './div[1]', 'port': './div[2]', 'area': './div[4]', 'protocol': ''},
        'encoding': 'utf-8'
    },
    {
        'urls': ['http://www.kuaidaili.com/proxylist/%s/' % n for n in range(1, 3)],
        'position': ".//*[@id='index_free_list']/table/tbody/tr[position()>0]",
        'detail': {'ip': './td[1]', 'port': './td[2]', 'area': './td[5]', 'protocol': './td[4]'}
    },
    {
        'urls': ['http://www.kuaidaili.com/free/%s/%s/' % (m, n) for m in ['inha', 'intr', 'outha', 'outtr'] for n in
                 range(1, 3)],
        'position': ".//*[@id='list']/table/tbody/tr[position()>0]",
        'detail': {'ip': './td[1]', 'port': './td[2]', 'area': './td[5]', 'protocol': './td[4]'}
    }
]
