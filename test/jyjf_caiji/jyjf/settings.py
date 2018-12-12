# -*- coding: utf-8 -*-

# Scrapy settings for jyjf project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the jyjfumentation:
#
#     http://jyjf.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthejyjfs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthejyjfs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'jyjf'
SPIDER_MODULES = ['jyjf.spiders']
NEWSPIDER_MODULE = 'jyjf.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
ITEM_PIPELINES = {
    'jyjf.pipelines.ThreeBaoPipeline': 300,
    'scrapy.pipelines.files.FilesPipeline': 1
}
FILES_STORE = './tmp'
# Obey robots.txt rules
DEFAULT_REQUEST_HEADERS = {
     'accept': 'image/webp,*/*;q=0.8',
     'accept-language': 'zh-CN,zh;q=0.8',
     'referer': 'http://www.jyjf.com.cn/',
     'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
}

DOWNLOADER_MIDDLEWARES = {
#    'baidutieba.rotate_ipagent.ProxyMiddleware': 100,
    'scrapy.downloadermiddlewares.downloadtimeout.DownloadTimeoutMiddleware': 350,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware':200,
    #'jyjf.middleware.RotateUserAgentMiddleware' :400,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware':100,
    #'jyjf.middleware.ProxyMiddleware' :543,
 }

LOG_LEVEL='INFO'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'jyjf (+http://www.yourdomain.com)'

# Obey robots.txt rules
"""观察代码可以发现，默认为True，就是要遵守robots.txt 的规则，那么 robots.txt 是个什么东西呢？
通俗来说， robots.txt 是遵循 Robot协议 的一个文件，它保存在网站的服务器中，它的作用是，告诉搜索引擎爬虫，本网站哪些目录下的网页 不希望 你进行爬取收录。在Scrapy启动后，会在第一时间访问网站的 robots.txt 文件，然后决定该网站的爬取范围。
当然，我们并不是在做搜索引擎，而且在某些情况下我们想要获取的内容恰恰是被 robots.txt 所禁止访问的。所以，某些时候，我们就要将此配置项设置为 False ，拒绝遵守 Robot协议 ！"""
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 1
# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthejyjfs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and jyjfs
DOWNLOAD_DELAY = 1
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
CONCURRENT_REQUESTS_PER_IP = 1

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthejyjfs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'jyjf.middlewares.MyCustomSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthejyjfs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'jyjf.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthejyjfs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthejyjfs.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'jyjf.pipelines.SomePipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://jyjf.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthejyjfs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
