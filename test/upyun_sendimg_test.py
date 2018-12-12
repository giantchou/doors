#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18/12/11 上午9:41
# @Author  : ZSG
# @Email   : 505972916@qq.com
# @File    : upyun_sendimg_test.py
# @Software: PyCharm
import upyun
import time
import requests

UPYUN_BUCKETNAME = 'doors'
UPYUN_USERNAME = 'doors360'
UPYUN_PASSWORD = 'doors360.cn'
UPYUN_BASE_URL = "https://upyun.doors360.cn"

def upload_img(_imgdata,extname):
    def up_to_upyum(key, value):
        up_conn = upyun.UpYun(UPYUN_BUCKETNAME, UPYUN_USERNAME, UPYUN_PASSWORD)
        up_headers = {}
        up_conn.put(key, value, checksum=True, headers=up_headers)
        return UPYUN_BASE_URL + key
    try:
        _file = _imgdata
        filename = str(time.time()).replace('.', '_') + extname
        image_key = "/image_upload/" + filename
        url = up_to_upyum(image_key, _file)
        return {"status": True, "filename": filename, "imgurl": url}
    except Exception:
        return {"status": False, "message": 'Err'}

def Transfer(_url):
    response = requests.get(_url)
    _imgdata = response.content
    extname="." + _url.split(".")[-1].split("?")[0]
    if "/" in extname:
        extname = ".jpg"
    new_name = upload_img(_imgdata, extname)
    print(new_name)
img_list=['http://www.jyjf.com.cn/UploadFiles/Product/2016-05-18/20160518165306898.jpg',
          'http://www.jyjf.com.cn/UploadFiles/Product/2017-03-29/20170329120729171.jpg',
          'http://www.jyjf.com.cn/UploadFiles/Product/2016-05-18/20160518165308398.jpg',
          'http://www.jyjf.com.cn/UploadFiles/Product/2017-03-29/20170329120731390.jpg']
for _url in img_list:
  Transfer(_url)

