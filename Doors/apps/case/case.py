# -*- coding: utf-8 -*-
# @author: Chou
# @time: 2018/11/21

from flask import Blueprint,render_template
case = Blueprint("case",__name__)

@case.route("/")
def case_list():
    return render_template('case/case_list.html')

@case.route("/<int:id>", methods=['GET', ])
def case_desc():
    return render_template('case/case_desc.html')
