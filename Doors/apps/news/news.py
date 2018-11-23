# -*- coding: utf-8 -*-
# @author: Chou
# @time: 2018/11/21

from flask import Blueprint,render_template
news = Blueprint("news",__name__)

@news.route("/")
def news_list():
    return render_template('news/news_list.html')

@news.route("/<int:id>", methods=['GET', ])
def news_desc():
    return render_template('news/news_desc.html')
