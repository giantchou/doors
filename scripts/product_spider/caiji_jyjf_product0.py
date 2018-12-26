#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18/12/12 上午11:33
# @Author  : ZSG
# @Email   : 505972916@qq.com
# @File    : caiji_jyjf_product0.py
# @Software: PyCharm
import sys
import time
import MySQLdb
import MySQLdb.cursors
import re
from selenium import webdriver
from scrapy.selector import HtmlXPathSelector
import upyun
import requests
import random
from aip import AipOcr

reload(sys)
sys.setdefaultencoding('utf-8')


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
    #x = check_baidu(_imgdata)
    x = 0
    if not x:
        extname = "." + _url.split(".")[-1]
        if "/" in extname:
            extname = ".jpg"
        new_name = upload_img(_imgdata, extname)
        return new_name['imgurl']
    else:
        return liyou[x]

def check_repeat(my_cur,item):
    my_cur.execute("SELECT * FROM product WHERE from_web='%s'" % item['url'])
    R = my_cur.fetchone()
    if R:
        return True
    else:
        return False
        my_cur.execute("SELECT * FROM product WHERE title='%s'" % item['title'])
        _R = my_cur.fetchone()
        if _R:
            return True
    return False

def data_insert(my_conn,my_cur,item):
    SQL = """INSERT INTO product(pid,title,cate1,cate2,from_web,addtime,content,material,abstract,title_img,keyword) 
                          VALUES(NULL,'%s',%s,%s,'%s',%s,'%s','%s','%s','%s','%s')""" % (item.get('title', ''),
                                item.get('cate1', 0), item.get('cate2', 0), item["url"], item['addtime'],
                                item["content"].replace("'", '"'), item.get('material', ''), item.get('abstract', ''),
                                                                               item['title_img'], item['kw'])
    my_cur.execute(SQL)
    my_conn.commit()

def get_cate(catename, my_cur):
    SQL = "SELECT cateid AS cate2,parentid AS cate1 FROM cate WHERE `level`=2 AND `name` LIKE '%%%s%%'"
    my_cur.execute(SQL % catename)
    result = my_cur.fetchone()
    if result:
        return result
    else:
        return {'cate1': 0, 'cate2': 0}

def list_handle(my_conn, my_cur, item):
    brow = webdriver.PhantomJS()
    brow.get(item['url'])
    info = brow.find_elements_by_xpath('//ul[@class="itemList"]/li')
    hxs = HtmlXPathSelector(text=brow.page_source)
    Info = hxs.select('//ul[@class="itemList"]/li/div[@class="pdemo"]/node()').extract()
    for index, _info in enumerate(info):
        try:
            liyou = random.choice(Liyou)
            item['title'] = _info.find_element_by_xpath('div[@class="ppic"]/a/img').get_attribute('title')
            item['url'] = _info.find_element_by_xpath('div[@class="ppic"]/a').get_attribute('href')
            if check_repeat(my_cur, item):
                print item['title'], item['url'], '已采集~~~'
                continue
            src_img_url = _info.find_element_by_xpath('div[@class="ppic"]/a/img').get_attribute('src')
            img_newurl = Transfer(liyou, src_img_url)
            item['title_img'] = img_newurl
            try:
                item['abstract'] = Info[index]
            except:
                item['abstract'] = ''

            item['addtime'] = int(time.time())
            if item['title'] in u'伸缩门,电动伸缩门,伸缩门厂家,电动伸缩门厂家,河南电动伸缩门厂家' or item['title'].isdigit():
                item['kw'] = u'伸缩门,电动门,电动伸缩门,伸缩门厂家,电动伸缩门厂家,河南电动伸缩门厂家'
            else:
                item['kw'] = item['title'] + u',伸缩门,电动伸缩门,伸缩门厂家,电动伸缩门厂家,河南电动伸缩门厂家'
            content = '<img src="'+item['title_img'] + '" title="金洋九峰科技发展有限公司系专业生产电动伸缩门厂家,严格要求制作工艺,保证产品完美品质,以品质占领市场.咨询热线:185-3008-5166">'+ item['abstract'] + '<img src="%s" title="金洋九峰科技发展有限公司系专业生产电动伸缩门厂家,严格要求制作工艺,保证产品完美品质,以品质占领市场.咨询热线:185-3008-5166"><img src="%s" title="金洋九峰科技发展有限公司系专业生产电动伸缩门厂家,严格要求制作工艺,保证产品完美品质,以品质占领市场.咨询热线:185-3008-5166"><br>'
            item["content"] = content % (liyou[1], liyou[2])
            item['abstract'] = item['abstract'][:250]
            data_insert(my_conn, my_cur, item)
            print item['url'], item['title'], '\r\n\r\n'
        except Exception, e:
            print e
            pass
    brow.close()

def main():
    Mysql_conf = {
        'host': '47.92.116.232',
        'user': 'mha_user',
        'passwd': 'gc895316',
        'db': 'doors',
        'charset': 'utf8',
        'init_command': 'set autocommit=0',
        'cursorclass': MySQLdb.cursors.DictCursor
    }

    My_cxn = MySQLdb.connect(**Mysql_conf)
    my_cur = My_cxn.cursor()
    data = [
        {'cate1': 2, 'cate2': 19, 'catid': 54},
        {'cate1': 5, 'cate2': 32, 'catid': 55},
        {'cate1': 0, 'cate2': 0, 'catid': 56},
        {'cate1': 4, 'cate2': 24, 'catid': 57},
        {'cate1': 8, 'cate2': 38, 'catid': 58},
        {'cate1': 14, 'cate2': 0, 'catid': 59},
        {'cate1': 3, 'cate2': 22, 'catid': 60},
        {'cate1': 11, 'cate2': 39, 'catid': 60}
    ]
    url = 'http://www.bjjyjf.net/index.php?c=content&a=list&catid=%s&page=%s'
    for item in data:
        brower = webdriver.PhantomJS()
        brower.get(url % (item['catid'], 1))
        max_page_url = brower.find_elements_by_xpath('//div[@id="pages"]/a')[-1]
        max_page = max_page_url.get_attribute('href').split('=')[-1]
        for page in range(1, int(max_page)+1):
            item['url'] = url % (item['catid'], page)
            list_handle(My_cxn, my_cur, item)

if __name__ == '__main__':
    main()
