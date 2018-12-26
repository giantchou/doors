#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     handle_kw_link
   Description :
   Author :       chou
   date：          2018/12/19
-------------------------------------------------
   Change Activity:
                   2018/12/19:
-------------------------------------------------
"""

import MySQLdb
import MySQLdb.cursors
import sys
from pyquery import PyQuery
import re

reload(sys)
sys.setdefaultencoding('utf-8')

def kw_handle(kw_list,text):
    handle = []
    for r in kw_list:
        if r['catelevel'] == 2 and r['cate2'] not in handle and r['keyword'] in text:
            text = text.replace(r['keyword'], r['productlink'])
            handle.append(r['cate1'])
            handle.append(r['cate2'])
        else:
            text = text.replace(r['keyword'], r['productlink'])
            handle.append(r['cate2'])
    return text

def main(sql):
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

    my_cur.execute("SELECT keyword,productlink,cate1,cate2,catelevel FROM cate_product_hyperlink")
    kw_list = my_cur.fetchall()
    my_cur.execute(sql['sl_sql'])
    content_list = my_cur.fetchall()
    title = u"金洋九峰科技发展有限公司系专业生产电动伸缩门厂家,严格要求制作工艺,保证产品完美品质,以品质占领市场.咨询热线:185-3008-5166"

    for text in content_list:
        _text = re.sub(title, "tmp_1-8-5-3-0-0-8-5-1-6-6", text['content'])
        content = kw_handle(kw_list, _text)
        _text = re.sub("tmp_1-8-5-3-0-0-8-5-1-6-6", title, content)
        my_cur.execute(sql['up_sql'] % (_text, text['id']))
        My_cxn.commit()
    my_cur.close()
    My_cxn.close()

if __name__ == '__main__':
    sql_list=[
        {'up_sql':"""UPDATE product SET content='%s',mark=1 where pid=%s""",
         'sl_sql':"""SELECT pid AS id,content FROM product WHERE mark=0"""},
        {'up_sql': """UPDATE cases SET content='%s',mark=1 where cid=%s""",
          'sl_sql': """SELECT cid AS id,content FROM cases WHERE mark=0"""},
        {'up_sql': """UPDATE news SET content='%s',mark=1 where pid=%s""",
         'sl_sql': """SELECT nid AS id,content FROM news WHERE mark=0"""}
    ]

    for sql in sql_list:
        main(sql)
