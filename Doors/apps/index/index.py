# -*- coding: utf-8 -*-
# @author: chenhuachao
# @time: 2018/11/20

from flask import Blueprint,render_template
index = Blueprint("index",__name__)


@index.route("/")
def show():
    return render_template('index.html')
