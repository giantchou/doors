# -*- coding: utf-8 -*-
# @author: chenhuachao
# @time: 2018/11/22

from flask import request,jsonify
from functools import wraps
import pymysql.cursors
import time
from hashlib import sha1
from .setting import mysqlconfig


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



def api_login_auth(func):
    '''
    api认证
    :return:
    '''

    @wraps(func)
    def wrapper():
        args = request.args
        api_key = args.get('api_key') # api_key
        timestamp = args.get('timestamp') #时间戳
        random_str = args.get('random_str','') # 随机字符串 16位
        sign = args.get('sign')
        try:
            if not api_key or not timestamp or len(random_str)!=16 or not sign:
                raise Exception("参数错误")
            _mysqlhandle = MysqlHandle(**mysqlconfig)
            _result = _mysqlhandle.select("select * from  user_security_key where api_key = '{api_key}'".format(
                api_key = api_key
            ))
            security_key = _result[0]['security_key']  if _result else ""
            assert security_key,Exception('api_key参数错误')
            if time.time()>int(timestamp)+60:
                raise Exception("请求已过期")
            sort_str = ''.join(sorted([api_key,timestamp,random_str,security_key],reverse=False))
            _sha1 = sha1()
            _sha1.update(sort_str.encode())
            new_sign = _sha1.hexdigest()
            if new_sign != sign:
                raise Exception("认证错误")
            return func()
        except Exception as e:
            return jsonify({"code":1,"msg":str(e)})
    return wrapper