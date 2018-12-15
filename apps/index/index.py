# -*- coding: utf-8 -*-
# @author: chenhuachao
# @time: 2018/11/20

from flask import Blueprint,render_template,\
    request,jsonify
from apps.utils import pc_and_m_transform

index = Blueprint("index",__name__)
import time
from ..models.model import Products,Customer,db



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
    hot_product = Products.query.order_by('hot').limit(4)
    db.session.close()
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
    intcheck = lambda x:int(x) if x else 1
    limitcheck = lambda x:int(x) if x else 10
    page = intcheck(page)
    limit = request.args.get('limit')
    limit = limitcheck(limit)
    if cid:
        products = Products.query.filter_by(cate1=cid).all()[(page-1)*limit:page*limit]
    else:
        products = Products.query.all()[(page - 1) * limit:page * limit]
    db.session.close()
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
    db.session.close()
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
    db.session.close()
    return render_template('sitemap/sitemap.xml', idlist=idlist)


@index.route("/buyuser",methods=['POST'])
def buyuser():
    data = {}
    params = request.form
    print(params)
    print(params.get('userdesc'))
    customer = Customer(tel=params.get('telnumber'),name=params.get('username'),
                        email=params.get("email"),address=params.get('address'),
                        desc=params.get("userdesc"),addtimes=int(time.time()))
    db.session.add(customer)
    db.session.commit()
    data['code'] = 0
    data['msg'] = '提交成功'
    return jsonify(data)