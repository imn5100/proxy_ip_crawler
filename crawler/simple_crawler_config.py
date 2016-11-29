# -*- coding: utf-8 -*-

# simpleCrawler setting
# 获取代理网页超时时间5s
TIMEOUT = 5
# 失败重试次数
RETRY_TIME = 3
# 存储模式 mysql || sqlite || json
SAVE_MODE = 'sqlite'
# bloom 过滤模式 pybloom (需要安装pybloom库)|redisbloom(需要本机安装redis数据库和python redis扩展库)
BLOOM_FILTER_MODE = "pybloom"
# MySQL配置
MYSQL_CONNECT = {'db': 'test', 'user': 'username', 'passwd': 'passwd',
                 'host': '127.0.0.1', 'use_unicode': True, 'charset': 'utf8'}
# sqlite文件配置
SQLITE_FILE = 'proxy_ip_simple.dat'
# json格式存储文件
JSON_FILE = 'proxy_ip_simple.json'
# bloom  文件(如果过滤模式是pybloom)
BLOOM_FILTER_FILE = 'filter_simple.bloom'
# 爬虫请求头
SIMPLE_CRAWLER_HEADER = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    'Connection': 'keep-alive',
    'Accept-Encoding': 'gzip, deflate',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
}
# 爬取的网站及相关设置
parserList = [
    {
        # 爬取url列表
        'urls': ['http://www.xicidaili.com/%s/%s' % (m, n) for m in ['nn', 'nt', 'wn', 'wt'] for n in range(1, 2)],
        # 数据表格所在位置 xpath
        'position': ".//*[@id='ip_list']/tr[position()>1]",
        # 详细数据获取xpath表达式
        'detail': {'ip': './td[2]', 'port': './td[3]', 'area': './td[4]/a', 'protocol': './td[6]'},
        'delayStep': 1
    },
    # {
    #     'urls': ['http://www.cz88.net/proxy/%s' % m for m in
    #              ['index.shtml'] + ['http_%s.shtml' % n for n in range(2, 3)]],
    #     'position': ".//*[@id='boxright']/div/ul/li[position()>1]",
    #     'detail': {'ip': './div[1]', 'port': './div[2]', 'area': './div[4]', 'protocol': ''},
    #     # 某些网站需要指定编码 防止乱码 默认utf-8
    #     'encoding': 'GBK'
    # },
    # {
    #     'urls': ['http://www.kuaidaili.com/proxylist/%s/' % n for n in range(1, 3)],
    #     'position': ".//*[@id='index_free_list']/table/tbody/tr[position()>0]",
    #     'detail': {'ip': './td[1]', 'port': './td[2]', 'area': './td[5]', 'protocol': './td[4]'}
    # },
    # {
    #     'urls': ['http://www.kuaidaili.com/free/%s/%s/' % (m, n) for m in ['inha', 'intr', 'outha', 'outtr'] for n in
    #              range(1, 3)],
    #     'position': ".//*[@id='list']/table/tbody/tr[position()>0]",
    #     'detail': {'ip': './td[1]', 'port': './td[2]', 'area': './td[5]', 'protocol': './td[4]'},
    #     # 延迟步伐。延迟步伐越大每次请求延迟间隔越长。某些网站限制一定时间内的请求数，所以需要设置延迟
    #     'delayStep': 1
    # }
]
