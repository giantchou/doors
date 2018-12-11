#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18/9/5 上午10:08
# @Author  : ZSG
# @Email   : 505972916@qq.com
# @File    : runspider.py
# @Software: PyCharm

from scrapy import cmdline
cmdline.execute("scrapy crawl tbSpider --nolog".split())
