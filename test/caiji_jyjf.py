#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18/12/12 上午11:33
# @Author  : ZSG
# @Email   : 505972916@qq.com
# @File    : caiji_jyjf.py
# @Software: PyCharm
import time
import MySQLdb
import MySQLdb.cursors

from selenium import webdriver
from scrapy.selector import HtmlXPathSelector

def check_repeat(my_cur,title):
    my_cur.execute("SELECT * FROM product WHERE from_web='%s'"%title)
    R = my_cur.fetchone()
    if R :
        return True
    else :
        return False

def data_insert(my_conn,my_cur,item):
    SQL = """INSERT INTO product(pid,title,cate1,cate2,from_web,addtime,content,material,abstract) 
                          VALUES(NULL,'%s',%s,%s,'%s',%s,'%s','%s','%s')""" % (item.get('title', ''),
                                item.get('cate1', 0), item.get('cate2', 0), item["url"], item['addtime'],
                                item["content"].replace("'", '"'), item.get('material', ''), item.get('abstract', ''))
    my_cur.execute(SQL)
    my_conn.commit()

def get_data(item, _url):
    _browser = webdriver.Chrome()
    _browser.get(_url)
    _browser.implicitly_wait(6)
    time.sleep(3)
    item['material'] = _browser.find_element_by_xpath('//div[@id="protop"]/ul[@class="ul_prodinfo"]/li[@class="li_normalprice"]').text
    try:
        item['abstract'] = _browser.find_element_by_xpath('//div[@id="contentvalue100"]/p').text
    except :
        item['abstract'] = ''
    hxs = HtmlXPathSelector(text=_browser.page_source)
    info = hxs.select('//div[@id="contentvalue100"]//p//node()').extract()
    item['content'] = ''.join(info)
    item['url'] = _url
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

def list_handle(my_conn,my_cur,item):
    brow = webdriver.PhantomJS()
    brow.get(item['url'])
    url_list = brow.find_elements_by_xpath('//div[@class="cpright"]/ul/li/a')
    for index, _url in enumerate(url_list):
        item = get_cate(_url.get_attribute('title').split('-')[0].split()[0], my_cur)
        item['title'] = _url.get_attribute('title')
        if check_repeat(my_cur, _url.get_attribute('href')):
            print u'已采集,跳过~~~~'
            continue
        item['addtime'] = int(time.time())
        info = get_data(item, _url.get_attribute('href'))
        data_insert(my_conn, my_cur, info)
    brow.close()

def main():
    Mysql_conf = {
        'host': '172.16.13.165',
        'user': 'mha_user',
        'passwd': 'gc895316',
        'db': 'doors',
        'charset': 'utf8',
        'init_command': 'set autocommit=0',
        'cursorclass': MySQLdb.cursors.DictCursor
    }

    My_cxn = MySQLdb.connect(**Mysql_conf)
    my_cur = My_cxn.cursor()

    url = 'http://www.jyjf.com.cn/product/%s.htm'
    for page in range(1, 17):
        item = {'url': url%page}
        list_handle(My_cxn, my_cur, item)

if __name__ == '__main__':
    main()
