# -*- coding: utf-8 -*-
# @author: chenhuachao
# @time: 2018/12/15
from flask import Blueprint,\
    jsonify,request,make_response
from apps.setting import mysqlconfig
from apps.utils import MysqlHandle,api_login_auth
import time
import os
import json
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





@api.route("/product/")
@api_login_auth
def products():
    _data = {}
    cate1 = request.args.get('cate1')
    limit = int(request.args.get("limit",10))
    page = int(request.args.get("page",1))
    mysqlhandle = MysqlHandle(**mysqlconfig)
    if cate1:
        sql = "select * from product where cate1 = {cate1} " \
              "order by addtime desc limit 0,{limit}".format(cate1 = cate1,limit=limit*page)
    else:
        sql = "select * from product " \
              " order by hot desc limit 0,{limit}".format(limit=limit * page)
    _products = mysqlhandle.select(sql)
    _data['code'] = 0
    for i in _products:
        if i['addtime']:
            i['addtime']=time.strftime("%Y-%m-%d %H:%M",time.localtime(i['addtime']))
    _data['data'] = _products
    return jsonify(_data)


@api.route("/product/detail/")
@api_login_auth
def productdetail():
    _data = {}
    pid = request.args.get('pid')
    mysqlhandle = MysqlHandle(**mysqlconfig)
    _products = mysqlhandle.select("select * from product where "
                                   "pid = {pid}".format(
        pid = pid))
    _data['code'] = 0
    _products = _products[0] if _products else ""
    if _products:
       _products['addtime']=time.strftime("%Y-%m-%d %H:%M",time.localtime(_products['addtime']))
    _data['data'] = _products
    return jsonify(_data)

@api.route("lottie/<string:jsonname>")
# @api_login_auth
def lottie(*args,**kwargs):
    jsonname  = kwargs.get("jsonname")

    jsondir = os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))))+'/static/lottie/{}'.format(jsonname)
    with open(jsondir,'r') as f:
        jsondata = f.read()
    data = json.loads(jsondata)
    # response = make_response(jsondata)
    # response.headers["Content-Type"] = "application/xhr"
    return jsonify(data)

@api.route("test/")
@api_login_auth
def test():
    data = {}
    data['code'] = 0
    data['msg'] = 'success'
    return jsonify(data)