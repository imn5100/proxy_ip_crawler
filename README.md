# proxy_ip_crawler

  抓取[西刺](http://www.xicidaili.com "xicidaili.com")代理IP的爬虫<br>
  目前支持存储_Mysql_，_Sqlite_<br>
  运行于_Python2.7_<br>
  运行前请先安装 __scrapy__<br>
  使用_mysql_存储内容需先运行SQL文件'proxy_ip.sql',并配置setting.py文件中的连接参数:MYSQL_CONNECT<br>
      cd 'project root path'
      scrapy crawl proxy_ip
