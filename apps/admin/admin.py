# -*- coding: utf-8 -*-
# @author: chenhuachao
# @time: 2018/11/20
from flask import Blueprint,render_template


admin = Blueprint("admin", __name__)

@admin.route("/")
def home():
    return render_template('admin/home.html')

@admin.route("/login")
def login():
    return ""