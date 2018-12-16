# -*- coding: utf-8 -*-
# @author: chenhuachao
# @time: 2018/11/20

from flask import Blueprint,render_template,\
    request,jsonify
from apps.utils import pc_and_m_transform,intcheck,limitcheck

index = Blueprint("index",__name__)
import time
from ..models.model import Products,Customer,session,Cases



@index.route("/")
@pc_and_m_transform({"m-template":"home/m-home.html","pc-template":"home/home.html"})
def show(*args,**kwargs):
    '''
    主页
    :param template:
    :return:
    '''
    template = args[0]
    product_recomment = session.query(Products).limit(4)
    hot_product = session.query(Products).order_by('hot').limit(4)
    session.close()
    return render_template(template,product_recomment = product_recomment,
                           hot_product = hot_product)

@index.route("/products/<int:cid>/")
@pc_and_m_transform({"m-template":"home/m-products.html","pc-template":"home/products.html"})
def products(*args,**kwargs):
    '''
    产品列表页
    :param template:
    :return:
    '''
    cid = kwargs.get('cid')
    cid = cid if cid else 0
    template = args[0]
    page = request.args.get("page")
    page = intcheck(page)
    limit = request.args.get('limit')
    limit = limitcheck(limit)
    if page>1:
        previous_page = page-1
    else:
        previous_page = 1
    next_page = page +1
    if cid:
        products = session.query(Products).filter_by(cate1=cid).all()[(page-1)*limit:page*limit]
    else:
        products = session.query(Products).all()[(page - 1) * limit:page * limit]
    session.close()
    count = len(products)
    print(count)
    return render_template(template,products=products,page=page,
                           count=count,cid = cid,previous_page = previous_page,
                           next_page = next_page)

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
    productinfo = session.query(Products).filter_by(pid = pid).first()
    session.close()
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
    page = request.args.get("page")
    page = intcheck(page)
    limit = request.args.get('limit')
    limit = limitcheck(limit)
    examples = session.query(Cases).all()[(page-1)*limit:page*limit]
    return render_template(template,examples = examples)


@index.route("/sexample/<int:cid>.html")
@pc_and_m_transform({"m-template":"home/m-success-example.html","pc-template":"home/success-example.html"})
def sexample_desc(*args,**kwargs):
    '''
     成功案例
    :param args:
    :param kwargs:
    :return:
    '''
    template = args[0]
    page = request.args.get("page")
    page = intcheck(page)
    limit = request.args.get('limit')
    limit = limitcheck(limit)
    examples = session.query(Cases).all()[(page-1)*limit:page*limit]
    return render_template(template,examples = examples)



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
    _productids = session.query(Products).all()
    idlist = [(i.pid,i.format_date())for i in _productids]
    session.close()
    return render_template('sitemap/sitemap.xml', idlist=idlist)


@index.route("/buyuser",methods=['POST'])
def buyuser():
    data = {}
    params = request.form
    print("data",request.data)
    print(params)
    print(params.get('userdesc'))
    customer = Customer(tel=params.get('telnumber'),name=params.get('username'),
                        email=params.get("email"),address=params.get('address'),
                        desc=params.get("userdesc"),addtimes=int(time.time()))
    session.add(customer)
    session.commit()
    data['code'] = 0
    data['msg'] = '提交成功'
    return jsonify(data)