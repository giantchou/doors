# -*- coding: utf-8 -*-
# @author: chenhuachao
# @time: 2018/11/20

from flask import Blueprint,render_template,request
from apps.utils import pc_and_m_transform
index = Blueprint("index",__name__)


@index.route("/")
@pc_and_m_transform({"m-template":"home/m-home.html","pc-template":"home/home.html"})
def show(template):
    print("****",template)
    return render_template(template,)

@index.route("/products/")
@pc_and_m_transform({"m-template":"home/m-products.html","pc-template":"home/products.html"})
def products(template):
    print("****",template)
    return render_template(template,)