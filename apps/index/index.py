# -*- coding: utf-8 -*-
# @author: chenhuachao
# @time: 2018/11/20

from flask import Blueprint,render_template,request
from apps.utils import pc_and_m_transform
index = Blueprint("index",__name__)
from ..models.model import Products


@index.route("/")
@pc_and_m_transform({"m-template":"home/m-home.html","pc-template":"home/home.html"})
def show(*args,**kwargs):
    '''
    主页
    :param template:
    :return:
    '''
    template = args[0]
    product_recomment = Products.query.limit(4)
    return render_template(template,product_recomment = product_recomment,
                           )

@index.route("/products/")
@pc_and_m_transform({"m-template":"home/m-products.html","pc-template":"home/products.html"})
def products(*args,**kwargs):
    '''
    产品列表页
    :param template:
    :return:
    '''
    template = args[0]
    page = request.args.get("page")
    intcheck = lambda x:int(x) if x else 1
    limitcheck = lambda x:int(x) if x else 10
    page = intcheck(page)
    limit = request.args.get('limit')
    limit = limitcheck(limit)
    products = Products.query.all()[(page-1)*limit:page*limit]
    return render_template(template,products=products,page=page)

@index.route("/products/<int:pid>.html")
@pc_and_m_transform({"m-template":"home/m-products-detail.html","pc-template":"home/products-detail.html"})
def product_detail(*args,**kwargs):
    '''
    产品详情页页
    :param template:
    :return:
    '''
    pid = kwargs.get('pid')
    template = args[0]
    productinfo = Products.query.filter_by(pid = pid).first()

    return render_template(template,productinfo = productinfo)


@index.route("/news/")
@pc_and_m_transform({"m-template":"home/m-news-list.html","pc-template":"home/news-list.html"})
def newslist(*args,**kwargs):
    '''
    新闻列表页
    :param template:
    :return:
    '''
    template = args[0]
    return render_template(template,)


@index.route("/news/<int:nid>.html")
@pc_and_m_transform({"m-template":"home/m-news-detail.html","pc-template":"home/news-detail.html"})
def newsdetail(*args,**kwargs):
    '''
    新闻详情页
    :param template:
    :param nid:
    :return:
    '''
    nid = kwargs.get("nid")
    print("nid=",nid)
    return render_template(args[0])

@index.route("/aboutus.html")
@pc_and_m_transform({"m-template":"home/m-about-us.html","pc-template":"home/about-us.html"})
def about_us(*args,**kwargs):
    template = args[0]
    return render_template(template)

@index.route("/honour")
@pc_and_m_transform({"m-template":"home/m-honour.html","pc-template":"home/honour.html"})
def honour(*args,**kwargs):
    template = args[0]
    return render_template(template)


@index.route("/sexample")
@pc_and_m_transform({"m-template":"home/m-success-example.html","pc-template":"home/success-example.html"})
def sexample(*args,**kwargs):
    '''
     成功案例
    :param args:
    :param kwargs:
    :return:
    '''
    template = args[0]
    return render_template(template)

@index.route("/address")
@pc_and_m_transform({"m-template":"home/m-address.html","pc-template":"home/address.html"})
def address(*args,**kwargs):
    '''
     成功案例
    :param args:
    :param kwargs:
    :return:
    '''
    template = args[0]
    return render_template(template)

@index.route("/sitemap")
def sitemap():
    _productids = Products.query.all()
    idlist = [(i.pid,i.format_date())for i in _productids]
    return render_template('sitemap/sitemap.xml', idlist=idlist)