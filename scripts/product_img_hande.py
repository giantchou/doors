#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18/12/12 下午5:28
# @Author  : ZSG
# @Email   : 505972916@qq.com
# @File    : product_img_hande.py
# @Software: PyCharm

import re
from pyquery import  PyQuery
import upyun
import time
import requests
import random
from aip import AipOcr
import base64
import hashlib
import json
import MySQLdb
import HTMLParser

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
        if u'实力雄厚' in res['words'] or u'品质保证' in res['words']:
            return 1
        if u'量身定制' in res['words'] or u'售后无忧' in res['words']:
            return 2
    return 0

def Transfer(liyou, _url):
    response = requests.get(_url)
    _imgdata = response.content
    x = check_baidu(_imgdata)
    if not x:
        extname="." + _url.split(".")[-1].split("?")[0]
        if "/" in extname:
            extname = ".jpg"
        new_name = upload_img(_imgdata, extname)
        return new_name
    else:
        return liyou[x]

def filter_tags(htmlstr):
    s = re.sub("<[^<>]+>", '', htmlstr)
    return s

def replace_charentity(htmlstr):
    htmlstr = htmlstr.replace("&quot;", '"')
    htmlstr = htmlstr.replace("&amp;", '&')
    htmlstr = htmlstr.replace("&lt;", '<')
    htmlstr = htmlstr.replace("&gt;", '>')
    htmlstr = htmlstr.replace("&nbsp;", ' ')
    return htmlstr

def get_simple_content(self):
    a = filter_tags(self)
    b = replace_charentity(a)
    _ = HTMLParser.HTMLParser()
    return _.unescape(b.strip())

def main():
    Mysql_conf = {
        'host': '172.16.13.165',
        'user': 'mha_user',
        'passwd': 'gc895316',
        'db': 'doors',
        'charset': 'utf8',
        'init_command': 'set autocommit=0'
    }

    My_cxn = MySQLdb.connect(**Mysql_conf)
    My_cur = My_cxn.cursor()

    My_cur.execute('SELECT title,from_web,cate1,cate2 FROM product_bakup')
    result = My_cur.fetchall()
    for res in result:
        """
        liyou = random.choice(Liyou)
        kw = res[0].split()[0].split('-')[0] + u',伸缩门,电动门,电动伸缩门,伸缩门厂家,电动伸缩门厂家,河南电动伸缩门厂家'
        doc = PyQuery("<div>" + res[1] + "</div>")
        for j in doc("img"):
            src=PyQuery(j).attr("src")
            if 'jyjf.com.cn' not in src:
                src = 'http://www.jyjf.com.cn'+src
            #img_newurl = Transfer(liyou, src)
            #j.set("src", new_name)
        #print doc
        doc("script").remove()
        #doc("a").remove()
        #simple_content = get_simple_content(doc)
        content = doc.html()
        """
        My_cur.execute('UPDATE product SET title="%s",cate1=%s,cate2=%s WHERE from_web="%s"'%(res[0],res[-2],res[-1],res[1]))

    My_cxn.commit()

if __name__ == '__main__':
    main()
