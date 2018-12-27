#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18/12/12 上午11:33
# @Author  : ZSG
# @Email   : 505972916@qq.com
# @File    : caiji_jyjf_news.py
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
from PIL import Image
import zbar
import json
import hashlib
import urllib
import httplib

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
        image_key = "/news_image_upload/" + filename
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
            if s.data:
                return 'https://upyun.doors360.cn/image_upload/20181227001.png'
    except:
        pass

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

def md(Str):
    md = hashlib.md5()
    md.update(Str.encode())
    return md

def weiyuanchuang_youdao(q):
    appKey = '350c1b23eec0e75a'
    secretKey = 'i10wUwuDLZzYNlc8ePABLCzaLdAJ16fV'
    httpClient = None
    _httpClient = None
    fromLang = 'zh-CHS'
    toLang = 'EN'
    salt = random.randint(1, 65536)
    sign = appKey + q + str(salt) + secretKey
    sign = md(sign).hexdigest()
    _myurl = '/api?appKey=' + appKey
    myurl = _myurl + '&q=' + urllib.quote(q) + '&from=' + fromLang + '&to=' + toLang + '&sign=' + sign + '&salt=' + str(salt)
    try:
        httpClient = httplib.HTTPConnection('openapi.youdao.com')
        httpClient.request('GET', myurl)
        # response是HTTPResponse对象
        response = httpClient.getresponse()
        translate_result = json.loads(response.read())['translation'][0]
        print translate_result, u'  伪原创中间数据~'
        if translate_result:
            time.sleep(2)
            salt = random.randint(1, 65536)
            sign = appKey + translate_result + str(salt) + secretKey
            sign = md(sign).hexdigest()
            Myurl = _myurl + '&q=' + urllib.quote(translate_result) + '&from=' + toLang + '&to=' + fromLang + '&sign=' + sign + '&salt=' + str(salt)
            _httpClient = httplib.HTTPConnection('openapi.youdao.com')
            _httpClient.request('GET', Myurl)
            Response = _httpClient.getresponse()
            print Response.read(), 'ABCD1234~~~'
            translate_result = json.loads(Response.read())['translation'][0]

    except Exception, e:
        print e
    finally:
        if httpClient:
            httpClient.close()
        if _httpClient:
            _httpClient.close()

    return translate_result

def weiyuanchuang(cut_words):
    appid = 20181227000252607
    salt = int(time.time())
    Key = 'na5bNsNBPweyEi1XuXyJ'
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    }
    try:
        # 中文转韩文zh_to_kor
        data = requests.post("http://api.fanyi.baidu.com/api/trans/vip/translate",
                             data={"from": "zh", "to": "kor", "q": cut_words, "appid": appid, "salt": salt,
                                   "sign": md(str(appid)+cut_words+str(salt)+Key).hexdigest()},
                             headers=headers, timeout=10)
        response = data.text
        translate_result_kor = json.loads(response).get("trans_result")[0].get("dst")
        print translate_result_kor, '  翻译后的韩语 '
        if translate_result_kor:
            # 韩文转化为中文kor_to_zh
            data = requests.post("http://api.fanyi.baidu.com/api/trans/vip/translate",
                                 data={"from": "kor", "to": "zh", "q": translate_result_kor, "appid": appid,"salt":salt,
                                       "sign": md(str(appid)+translate_result_kor+str(salt)+Key).hexdigest()},
                                 headers=headers, timeout=10)
            response = data.text
            translate_result = json.loads(response).get("trans_result")[0].get("dst")
        else:
            print '翻译成韩语失败~~~'
            translate_result = cut_words
    except Exception as e:
        translate_result = cut_words
        print str(e)
    return translate_result

def check_repeat(my_cur, _url):
    my_cur.execute("SELECT * FROM news WHERE from_web='%s'" % _url)
    R = my_cur.fetchone()
    if R:
        return True
    else:
        return False

def data_insert(my_conn,my_cur,item):
    SQL = """INSERT INTO news(nid,title,cate1,cate2,from_web,addtime,content,abstract,title_img,keyword) 
                          VALUES(NULL,'%s',%s,%s,'%s',%s,'%s','%s','%s','%s')""" % (item.get('title', ''),
                                item.get('cate1', 0), item.get('cate2', 0), item["url"], item['addtime'],
                                item["content"].replace("'", '"'), item.get('abstract', ''),
                                item.get('title_img', ''), item['kw'])
    my_cur.execute(SQL)
    my_conn.commit()

def get_data(item, _url):
    _info, img_list = [], []
    liyou = random.choice(Liyou)
    _browser = webdriver.Chrome()
    _browser.get(_url)
    item['url'] = _url
    _browser.implicitly_wait(6)
    time.sleep(1)
    hxs = HtmlXPathSelector(text=_browser.page_source)
    info = hxs.select('//div[@id="cntrBody"]/p/node()').extract()
    for i in info:
        i = re.sub(r'13910630394', '18530085166', i)
        i = re.sub(r'jyjf.com', 'doors360', i)
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
        if 'doors360.cn' in i or u'金洋九峰' in i or '18530085166' in i:
            _info.append(i)
        else:
            #进行伪原创处理
            i = re.sub(r'<.*?>', '', i)
            if len(i.strip()):
                print i, '伪原创处理前的~~~'
                i = weiyuanchuang(i)
                print i, '伪原创处理后的~~~'
                _info.append('<span style="font-family:黑体">'+i+'</span>')
            else:
                pass

    item['content'] = ''.join(_info)
    item['title_img'] = img_list[0] if img_list else ''
    item = get_cate(item)

    _browser.quit()
    return item

def get_cate(item):
    if u'伸缩门' in item['title']:
        item['cate1'] = 2
        item['cate2'] = 19
    item['kw'] = u'伸缩门,电动门,电动伸缩门,伸缩门厂家,电动伸缩门厂家,河南电动伸缩门厂家'
    return item

def list_handle(my_conn, my_cur, item):
    brow = webdriver.PhantomJS()
    brow.get(item['url'])
    url_list = brow.find_elements_by_xpath('//div[@class="xlt"]/p/a')
    for index, _url in enumerate(url_list):
        item['title'] = _url.get_attribute('title')
        item['abstract'] = _url.text
        if 'jyjf.com' not in _url.get_attribute('href'):
            item['url'] = 'http://www.jyjf.com.cn' + _url.get_attribute('href')
        else:
            item['url'] = _url.get_attribute('href')
        if check_repeat(my_cur, item['url']):
            print u'已采集,跳过~~~~'
            continue
        item['addtime'] = int(time.time())
        info = get_data(item, item['url'])
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

    url = 'http://www.jyjf.com.cn/xwmt-%s.htm'
    for page in range(1, 14):
        item = {'url': url % page}
        list_handle(My_cxn, my_cur, item)

if __name__ == '__main__':
    main()
