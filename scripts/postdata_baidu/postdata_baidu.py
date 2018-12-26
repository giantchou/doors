#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18/12/26 上午8:46
# @Author  : ZSG
# @Email   : 505972916@qq.com
# @File    : postdata_baidu.py
# @Software: PyCharm

import time
import pymysql as MySQLdb
import requests

def postXiongZhang(filecontent):
    url = "http://data.zz.baidu.com/urls?appid=1619713941008109&token=DCuZDmp9D0KfEl8X&type=realtime"
    send_headers = {'Content-Type': 'text/plain'}
    resp = requests.post(url, data=filecontent, headers=send_headers, timeout=3)
    return resp.text

def postBaiDu(filecontent):
    URL = "http://data.zz.baidu.com/urls?site=www.doors360.cn&token=DCuZDmp9D0KfEl8X"
    send_headers = {'Content-Type': 'text/plain'}
    resp = requests.post(URL, data=filecontent, headers=send_headers, timeout=3)
    return resp.text

def main():
    T = int(time.time()) - 1545804586
    N = int(T / 86400)
    sql = "SELECT pid FROM product ORDER BY pid DESC limit %s,15"
    Mysql_conf = {
        'host': '47.92.116.232',
        'user': 'mha_user',
        'passwd': 'gc895316',
        'db': 'doors',
        'charset': 'utf8',
        'init_command': 'set autocommit=0'
    }

    My_cxn = MySQLdb.connect(**Mysql_conf)
    My_cur = My_cxn.cursor()
    My_cur.execute(sql % (N*10))
    result = My_cur.fetchall()
    for res in result:
        # 提交百度
        #print(postBaiDu("https://www.doors360.cn/products/%s.html"%res[0]))
        # 提交到熊掌号
        print(postXiongZhang("https://m.doors360.cn/products/%s.html?fromxz" % res[0]))
    My_cur.close()
    My_cxn.close()

if __name__ == '__main__':
    main()
