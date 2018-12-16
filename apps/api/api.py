# -*- coding: utf-8 -*-
# @author: chenhuachao
# @time: 2018/12/15
from flask import Blueprint,\
    request,jsonify

api = Blueprint("api",__name__)
from ..models import model



@api.route("cate/")
def cate():
    data = {}
    _cate = model.session.query(model.Cate).filter_by(level=1).all()
    cate = [(i.cateid,i.name) for i in _cate]
    model.session.close()
    data['code'] = 0
    data['data'] = cate
    data['msg'] = 'success'
    return jsonify(data)