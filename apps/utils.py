# -*- coding: utf-8 -*-
# @author: chenhuachao
# @time: 2018/11/22

from flask import request
from functools import wraps
import pymysql.cursors

mysqlconfig={
    "host":"mysql.site.bao361.cn",
    "port":3306,
    "user":"bx_user",
    "passwd":"gc895316",
    "db":"bx_abc",
    "cursorclass":pymysql.cursors.DictCursor,
     "charset":'utf8'
}






class MysqlHandle(object):
    def __init__(self,**conf):
        self.conf=conf
        self.conn = self.connection()
        self.cusor = self.conn.cursor()
    def connection(self):
        _conn= pymysql.connect(**self.conf)
        return _conn

    def other_op(self,sql):
        print(sql)
        self.cusor.execute(sql)
        self.conn.commit()
    def select(self,sql):
        _r = self.cusor.execute(sql)
        return self.cusor.fetchall()

    def __del__(self):
        print("close db")
        self.conn.close()
intcheck = lambda x: int(x) if x else 1
limitcheck = lambda x: int(x) if x else 10

def pc_and_m_transform(params):
    '''
    M站和PC站的切换装饰器
    :param params:
    :return:
    '''
    def wrapper(func):
        @wraps(func)
        def _logic(*args,**kwargs):
            host = request.host
            _check = lambda x: x.startswith('192.168') or x.startswith('10') or x.startswith("m.")
            if _check(host):
                args = args.__add__((params.get('m-template'),))
                return func(*args,**kwargs)
            else:
                args = args.__add__((params.get('pc-template'),))
                return func(*args,**kwargs)
        return _logic
    return wrapper
