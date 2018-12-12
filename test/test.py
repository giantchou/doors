#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18/8/15 下午22:03
# @Author  : ZSG
# @Email   : 505972916@qq.com
# @File    : caiji_sohu.py
# @Software: PyCharm
"""
图片处理模块验证
"""
import time
import sys

from PIL import Image
import zbar

from gcutils.encrypt import md5
import upyun

import random
import requests
from aip import AipOcr
import hmac
import base64
import hashlib
import json

reload(sys)
sys.setdefaultencoding('utf8')

UPYUN_BUCKETNAME = 'manman-1234'
UPYUN_USERNAME = 'mm123456'
UPYUN_PASSWORD = 'mm123456'
UPYUN_BASE_URL = "https://upyun.bao361.cn"

def check_qcode(_url):
    headers = {'user-agent': "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)"}
    result = requests.get(_url, headers=headers)
    _imgdata = result.content
    with open('_tmp.jpg', 'wb')as f:
        f.write(_imgdata)
    f.close()
    scanner = zbar.ImageScanner()
    scanner.parse_config('enable')
    img = Image.open('_tmp.jpg').convert('L')
    w, h = img.size
    zimg = zbar.Image(w, h, 'Y800', img.tobytes())
    scanner.scan(zimg)

    try:
        """只要扫码出图片中包含二维码、不论内容是什么,一概不要"""
        for s in zimg:
            print s.data, type(s.data)
            if s.data:
                print(u'识别成功~~~')
                return True
    except:
        pass

    return False

### 将图片转存至又拍云上 ###
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

### 使用百度云图片识别关键词 ###
def check_baidu(stopword_list, imgdata):
    APP_ID = '11681424'
    API_KEY = '1266Z5G0o3QdyDh08F3WtURD'
    SECRET_KEY = 'W9tbTSZPBPm5khIG2ZEmMXkFjORsaK0m'
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    Result = client.basicAccurate(imgdata)
    for res in reversed(Result['words_result']):
        for sw in stopword_list:
            if sw in res['words']:
                return True
    return False

### 使用腾讯云图片识别关键词 ###
def check_tencent(stopword_list, imgdata):
    appid = '1253358209'
    secret_id = 'AKIDLXddS5gu5HSSGv6hnsodHo9IG3jEEjme'
    secret_key = 'qX7Xp031pSuGaptlT1QjsvnZH7UmsrfH'
    bucket = 'BUCKET'
    current = time.time()
    expired = current + 2592000

    rdm = ''.join(random.choice("0123456789") for i in range(10))
    info = "a=" + appid + "&b=" + bucket + "&k=" + secret_id + "&e=" + str(expired) + "&t=" + str(current) + "&r=" + str(rdm) + "&u=0&f="
    signindex = hmac.new(secret_key, info, hashlib.sha1).digest()
    sign = base64.b64encode(signindex + info)
    url = "http://recognition.image.myqcloud.com/ocr/general"
    headers = {'Host': 'recognition.image.myqcloud.com',
               "Authorization": sign,
               }
    files = {'appid': (None, appid),
             'bucket': (None, bucket),
             'image': ('1.jpg', imgdata, 'image/jpeg')
             }

    Result = requests.post(url, files=files, headers=headers)
    result = json.loads(Result.content)

    for Res in reversed(result['data']['items']):
        print ''.join([res['character'] for res in Res['words']])
        for sw in stopword_list:
            if sw in ''.join([res['character'] for res in Res['words']]):
                return True
    return False

### 获取图片并截取、去掉无用的内容 ###
def Transfer(_url):
    stopword_list = [u'保友圈', u'纪家保险', u'燕梳杂谈', u'保险岛', u'yanshuzt', u'bxd365',u'保险真谛',u'乐保通',u'全民云科技',
                     u'纪家', u'保险自媒体联盟', u'微ans山z', u'全民云科技', u'微信号', u'微信', u'信号', u'保险新闻网',u'智保网',
                     u'微言', u'微后', u'言号', u'后号']

    pic_name = '_tmp.jpg'
    headers = {'user-agent': "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)"}
    result = requests.get(_url, headers=headers)
    _imgdata = result.content
    if check_tencent(stopword_list, _imgdata) or check_baidu(stopword_list, _imgdata):
        with open(pic_name, 'wb')as f:
            f.write(_imgdata)
        f.close()
        i = Image.open(pic_name)
        size = i.size                           #获取图片的长宽
        coderange = (0, 0, size[0], size[1]-50) #写成我们需要截取的位置坐标,截去图片的底部50像素
        _imgdata = i.crop(coderange)
        _imgdata.save(r"_tmp.png")
        with open("_tmp.png", 'rb') as fp:
            _imgdata = fp.read()

    extname = "." + _url.split(".")[-1]

    if "/" in extname:
        extname = ".jpg"

    print type(_imgdata)
    #new_name = upload_img(str(_imgdata), extname)
    #print new_name


if __name__ == '__main__':
    _url = 'http://5b0988e595225.cdn.sohucs.com/images/20180727/3375ca110da14585bc5f3ccbdb800616.jpg'
    _url = 'http://5b0988e595225.cdn.sohucs.com/images/20180807/509ac94514b34864a4e0e660b4c5dda0.jpeg'
    _url = 'http://img.mp.itc.cn/upload/20170802/cf3f128de000446585be277f45998817_th.jpg'
    #Transfer(_url)
    check_qcode(_url)
