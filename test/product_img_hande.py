#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18/12/12 下午5:28
# @Author  : ZSG
# @Email   : 505972916@qq.com
# @File    : product_img_hande.py
# @Software: PyCharm

import re
import pymysql
import upyun
import time
import requests
import random
from aip import AipOcr
import base64
import hashlib
import json

UPYUN_BUCKETNAME = 'doors'
UPYUN_USERNAME = 'doors360'
UPYUN_PASSWORD = 'doors360.cn'
UPYUN_BASE_URL = "https://upyun.doors360.cn"

Liyou = [{1: 'https://upyun.doors360.cn/image_upload/1544606984_7874088.jpg',
          2: 'https://upyun.doors360.cn/image_upload/1544606987_158426.jpg'},
         {1: 'https://upyun.doors360.cn/image_upload/1544606986_345472.jpg',
          2: 'https://upyun.doors360.cn/image_upload/1544606987_8461928.jpg'}]

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

### 使用百度云图片识别关键词 ###
def check_baidu(imgdata):
    APP_ID = '11681424'
    API_KEY = '1266Z5G0o3QdyDh08F3WtURD'
    SECRET_KEY = 'W9tbTSZPBPm5khIG2ZEmMXkFjORsaK0m'
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    Result = client.basicAccurate(imgdata)
    for res in reversed(Result['words_result']):
        if '实力雄厚' in res['words'] or '品质保证' in res['words']:
            return 1
        if '量身定制' in res['words'] or '售后无忧' in res['words']:
            return 2
    return 0

def Transfer(liyou,_url):
    response = requests.get(_url)
    _imgdata = response.content
    x = check_baidu(_imgdata)
    if not x:
        extname="." + _url.split(".")[-1].split("?")[0]
        if "/" in extname:
            extname = ".jpg"
        print(u'不是4大理由!!!')
        #new_name = upload_img(_imgdata, extname)
        #return new_name
    else:
        print(liyou[x])

### 使用腾讯云图片识别关键词 ###
""" 
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
"""

def main():
    liyou = random.choice(Liyou)
    url = 'http://www.jyjf.com.cn/UploadFiles/Product/2016-05-18/20160518165306898.jpg'
    Transfer(liyou, url)

if __name__ == '__main__':
    main()
