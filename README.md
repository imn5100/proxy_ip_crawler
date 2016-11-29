# proxy_ip_crawler
##简述
  抓取代理IP的爬虫<br>
  支持存储方式：_Mysql_，_Sqlite_，_Json_<br>
  运行于_Python2.7_<br>
  
###A.使用__scrapy__抓取<br>
  依赖模块：__[scrapy](https://scrapy.org/)__，__[requests](https://github.com/kennethreitz/requests "requests")__，__[lxml](http://lxml.de/ "lxml")__，__[pybloom](https://github.com/jaybaird/python-bloomfilter/ "pybloom")__。可选模块:mysql<br>
  运行配置：setting.py<br>
  使用_Mysql_存储内容需先运行SQL文件 proxy_ip.sql，并配置setting.py文件中的连接参数:MYSQL_CONNECT<br>
  
      python launchScrapy.py
    
 
###B.使用__requests__抓取 <br>
  增加的爬取的网址，减少了必要依赖<br>
  依赖模块：__[requests](https://github.com/kennethreitz/requests "requests")__，__[lxml](http://lxml.de/ "lxml")__，__[redis](https://pypi.python.org/pypi/redis/ "redis")__或__[pybloom](https://github.com/jaybaird/python-bloomfilter/ "pybloom")__ ，可选模块:mysql<br>
  运行配置：simple_crawler_config.py<br>
  
      python launchSimpleCrawler.py


      
