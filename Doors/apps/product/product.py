# -*- coding: utf-8 -*-
# @author: Chou
# @time: 2018/11/21

from flask import Blueprint,render_template
product = Blueprint("product",__name__)

@product.route("/")
def product_list():
    return render_template('product/product_list.html')

@product.route("/<int:id>", methods=['GET', ])
def product_desc():
    return render_template('product/product_desc.html')
