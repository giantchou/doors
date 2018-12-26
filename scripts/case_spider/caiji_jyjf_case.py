#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18/12/12 上午11:33
# @Author  : ZSG
# @Email   : 505972916@qq.com
# @File    : caiji_jyjf.py
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
    x = check_baidu(_imgdata)
    if not x:
        extname = "." + _url.split(".")[-1]
        if "/" in extname:
            extname = ".jpg"
        new_name = upload_img(_imgdata, extname)
        return new_name['imgurl']
    else:
        return liyou[x]

def check_repeat(my_cur,title):
    my_cur.execute("SELECT * FROM product WHERE from_web='%s'"%title)
    R = my_cur.fetchone()
    if R :
        return True
    else :
        return False

def data_insert(my_conn,my_cur,item):
    SQL = """INSERT INTO cases_ssxt_caiji(cid,title,cate1,cate2,from_web,addtime,content,area,abstract,title_img,keyword) 
                                          VALUES(NULL,'%s',%s,%s,'%s',%s,'%s','%s','%s','%s','%s')""" % (
        item.get('title', ''),
        item.get('cate1', 0), item.get('cate2', 0), item["url"], item['addtime'],
        item["content"].replace("'", '"'), item.get('area', ''), item.get('abstract', ''),
        item.get('title_img', ''), item.get('keyword', ''))

    my_cur.execute(SQL)
    my_conn.commit()

def get_data(item, _url):
    _info, img_list = [], []
    liyou = random.choice(Liyou)
    _browser = webdriver.Chrome()
    _browser.get(_url)
    _browser.implicitly_wait(3)
    time.sleep(1)
    try:
        item['abstract'] = _browser.find_element_by_xpath('//div[@class="age_li_about"]/p').text
    except :
        item['abstract'] = ''
    hxs = HtmlXPathSelector(text=_browser.page_source)
    info = hxs.select('//div[@class="age_li_about"]/p/node()').extract()
    for i in info:
        i = re.sub(r'</a>', '', i)
        i = re.sub(r'<a .*?>', '', i)
        i = re.sub(r'\<img(.*?)src="(.*?)".*?\>', r'<img src="\2">', i)
        try:
            img_url = re.search(r'<img src="(.*?)">', i).group()
            src_img_url = img_url[10:-2]
            if 'jyjf.com.cn' not in src_img_url:
                src_img_url = 'http://www.jyjf.com.cn' + src_img_url
            img_newurl = Transfer(liyou, src_img_url)
            img_list.append(img_newurl)
            i = re.sub(r'\<img src="(.*?)"\>', '<img src="%s" title="金洋九峰科技发展有限公司系专业生产电动伸缩门厂家,严格要求制作工艺,保证产品完美品质,以品质占领市场.咨询热线:185-3008-5166">'%img_newurl, i)
        except Exception, e:
            print e
            pass
        _info.append(i)

    item['content'] = ''.join(_info)
    item['url'] = _url
    item['title_img'] = img_list[0]
    _browser.quit()
    return item

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
    url_list = brow.find_elements_by_xpath('//div[@class="agent_con"]/dl/dt/a')
    for index, _url in enumerate(url_list):
        item['title'] = _url.get_attribute('title')
        kw = item['title'].split('-')[0].split()[0]
        item = get_cate(kw, my_cur)
        item['title'] = _url.get_attribute('title')
        if 'jyjf.com' not in _url.get_attribute('href'):
            item['url'] = 'http://www.jyjf.com.cn' + _url.get_attribute('href')
        if kw in u'伸缩门,电动伸缩门,伸缩门厂家,电动伸缩门厂家,河南电动伸缩门厂家':
            item['kw'] = u'伸缩门,电动门,电动伸缩门,伸缩门厂家,电动伸缩门厂家,河南电动伸缩门厂家'
        else:
            item['kw'] = kw + u',伸缩门,电动伸缩门,伸缩门厂家,电动伸缩门厂家,河南电动伸缩门厂家'
        if check_repeat(my_cur, _url.get_attribute('href')):
            print u'已采集,跳过~~~~'
            continue
        item['addtime'] = int(time.time())
        info = get_data(item, _url.get_attribute('href'))
        data_insert(my_conn, my_cur, info)
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

    start_urls = ['http://www.jyjf.com.cn/jyjfgcalzs-1.htm',
                  'http://www.jyjf.com.cn/jyjfgcalzs-2.htm',
                  'http://www.jyjf.com.cn/jyjfgcalzs-3.htm',
                  'http://www.jyjf.com.cn/jyjfgcalzs-4.htm'
                  ]
    for url in start_urls:
        item = {'url': url}
        list_handle(My_cxn, my_cur, item)

if __name__ == '__main__':
    main()
