#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18/7/26 上午9:41
# @Author  : ZSG
# @Email   : 505972916@qq.com
# @File    : upyun_sendimg_test.py
# @Software: PyCharm

import urlparse
from gcutils.encrypt import md5
import upyun
import random, time

import urllib2,urllib
import json

UPYUN_BUCKETNAME = 'manman-1234'
UPYUN_USERNAME = 'mm123456'
UPYUN_PASSWORD = 'mm123456'
UPYUN_BASE_URL = "https://upyun.bao361.cn"

def upload_img(_imgdata,extname):
    try:
        _file = _imgdata
        extname = extname.split("?")[0]

        def up_to_upyum(key, value):
            up_conn = upyun.UpYun(UPYUN_BUCKETNAME, UPYUN_USERNAME, UPYUN_PASSWORD)
            up_headers = {}
            up_conn.put(key, value, checksum=True, headers=up_headers)
            return UPYUN_BASE_URL + key

        filename = md5(str(time.time()) + str(random.random())) + extname
        image_key = "/image_upload_api/" + filename
        url = up_to_upyum(image_key, _file)
        return {"status": True, "filename": filename, "imgurl": url}
    except Exception, e:
        print e
        return {"status": False, "message": e.message}
def Transfer(_url):
    request = urllib2.Request(_url)
    request.headers["Upgrade-Insecure-Requests"] = 1
    request.headers["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36 QQBrowser/4.2.4718.400"
    request.headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
    _imgdata = urllib2.urlopen(request, timeout=3).read()
    extname="." + _url.split(".")[-1]
    if "/" in extname:
        extname = ".jpg"
    new_name = upload_img(_imgdata, extname)
    return new_name

_url="http://www.threebao.com/uploadfile/2018/0319/20180319104845203.jpg"
Transfer(_url)