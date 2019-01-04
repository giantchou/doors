# -*- coding: utf-8 -*-
# @author: chenhuachao
# @time: 2018/12/15
from flask import Blueprint,\
    jsonify
from apps.setting import mysqlconfig
from apps.utils import MysqlHandle,api_login_auth
api = Blueprint("api",__name__)



@api.route("cate/")
def cate():
    data = {}
    mysqlhandle = MysqlHandle(**mysqlconfig)
    _cate = mysqlhandle.select("select * from cate where level = 1")
    cate = [(i.get("cateid"),i.get("name")) for i in _cate]
    data['code'] = 0
    data['data'] = cate
    data['msg'] = 'success'
    return jsonify(data)





@api.route("test/")
@api_login_auth
def test():
    data = {}
    data['code'] = 0
    data['msg'] = 'success'
    return jsonify(data)