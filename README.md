# proxy_ip_crawler

  抓取代理IP的爬虫<br>
  支持存储方式：_Mysql_，_Sqlite_，_Json_<br>
  运行于_Python2.7_<br>
  运行前请先安装 __scrapy__<br>
  使用 BloomFilter过滤重复代理地址、urllib2验证代理地址有效性<br>
  setting.py文件配置 SAVE_MODE,可选择存储模式<br>
  使用_Mysql_存储内容需先运行SQL文件 proxy_ip.sql，并配置setting.py文件中的连接参数:MYSQL_CONNECT<br>
  
      cd 'project root path'
      scrapy crawl proxy_ip
