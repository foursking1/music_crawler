#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# User define
DOWNLOAD_DELAY = 2

# DOWNLOADER_MIDDLEWARES = {
#     'title_spider.middlewares.PhantomJSMiddleware': 1000,
#
# }

BOT_NAME = 'scrapy_demo'

SPIDER_MODULES = ['scrapy_demo.spiders']
NEWSPIDER_MODULE = 'scrapy_demo.spiders'
SCHEDULER_ORDER =  "BF0"

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

WEBDRIVER_BROWSER = 'PhantomJS'
#WEBDRIVER_BROWSER = 'Firefox'
#WEBDRIVER_BROWSER = 'Chrome'
#WEBDRIVER_BROWSER = 'Ie'

WEBDRIVER_OPTIONS = {
    #'service_args': [ '--debug=true', '--load-images=false', '--webdriver-loglevel=debug'],
    'executable_path':'/home/foursking/project/phantomjs-2.1.1-linux-x86_64/bin/phantomjs'
    #'executable_path': ['D:/Program Files/phantomjs-1.9.1-windows/phantomjs.exe']
}


# WEBDRIVER_OPTIONS = {
#     'executable_path':['D:\Program Files (x86)\Mozilla Firefox\firefox.exe']
# }

#WEBDRIVER_OPTIONS = {
#    'executable_path':["D:/downloads/chromedriver_win32/chromedriver"]
#}

# WEBDRIVER_OPTIONS = {
#     'executable_path':["C:\Program Files\Internet Explorer\iexplore.exe"]
# }

DOWNLOAD_HANDLERS = {
    'http': 'scrapy_webdriver.download.WebdriverDownloadHandler',
    'https': 'scrapy_webdriver.download.WebdriverDownloadHandler',
}

SPIDER_MIDDLEWARES = {
    'scrapy_webdriver.middlewares.WebdriverSpiderMiddleware': 543
}

DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
    'scrapy_demo.rotate_useragent.RotateUserAgentMiddleware': 400
}

ITEM_PIPELINES = {
    'scrapy_demo.pipelines.JsonWriterPipeline': 800,
}


DOWNLOAD_DELAY = 0.25  # 间隔时间
# LOG_LEVEL = 'INFO'  # 日志级别
CONCURRENT_REQUESTS = 16  # 默认为16
# CONCURRENT_ITEMS = 1
# CONCURRENT_REQUESTS_PER_IP = 1
REDIRECT_ENABLED = False
