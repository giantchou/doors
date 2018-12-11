# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging
from twisted.enterprise import adbapi
import MySQLdb

class ThreeBaoPipeline(object):
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool(
                dbapiName='MySQLdb',
                db='doors',
                host='47.92.116.232',
                user='mha_user',
                passwd='gc895316',
                charset='utf8',
                use_unicode=True
        )

    #pipeline默认调用
    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._conditional_insert, item)
        query.addErrback(self.handle_error)
        return item

    #将每行更新或写入数据库中
    def _conditional_insert(self, tx, item):
        try:
            SQL = """INSERT INTO bx_news_plus(pid,title,cate1,cate2,from_web,addtime,content,material) 
                                       VALUES(NULL,'%s',%s,%s,'%s',%s,'%s','%s')""" % \
                                             (item.get('title', ''), item.get('cate1', 0), item.get('cate2', 0),
                                              item["url"],item['addtime'], item["content"].replace("'", '"'),
                                             item.get('material', ''))
            tx.execute(SQL)

        except Exception, e:
            print item.keys()
            print e, item['url']
        else:
            logging.log(logging.INFO, "Item stored in db: %s" % item["url"])
            pass

    def handle_error(self, e):
        logging.log(logging.ERROR, str(e))
