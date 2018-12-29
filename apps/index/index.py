# -*- coding: utf-8 -*-
# @author: chenhuachao
# @time: 2018/11/20

from flask import Blueprint,render_template,\
    request,jsonify,make_response
import json
from apps.setting import mysqlconfig
from apps.utils import pc_and_m_transform,intcheck,\
    limitcheck,MysqlHandle

index = Blueprint("index",__name__)
import time



@index.route("/")
@pc_and_m_transform({"m-template":"home/m-home.html","pc-template":"home/home.html"})
def show(*args,**kwargs):
    '''
    主页
    :param template:
    :return:
    '''
    template = args[0]
    mysqlhandle = MysqlHandle(**mysqlconfig)
    product_recomment = mysqlhandle.select("select * from product order by addtime desc limit 0,4")
    hot_product = mysqlhandle.select("select * from product order by hot desc limit 0,4")
    news = mysqlhandle.select("select * from news order by addtime desc limit 0,5")
    return render_template(template,product_recomment = product_recomment,
                           hot_product = hot_product,
                           news = news)

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
    mysqlhandle = MysqlHandle(**mysqlconfig)
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
        products = mysqlhandle.select("select * from product where cate1={cate1}  order by addtime desc limit {start},{step}".format(
            cate1 = cid,
            start = (page-1)*limit,
            step = limit
        ))
    else:
        products = mysqlhandle.select("select * from product order by addtime desc limit {start},{step}".format(
            start = (page-1)*limit,
            step = limit
        ))
    count = len(products)
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
    mysqlhandle = MysqlHandle(**mysqlconfig)
    productinfo = mysqlhandle.select("select * from product where pid = {pid}".format(pid = pid))
    if productinfo:
        productinfo = productinfo[0]
    mysqlhandle.other_op("update product set hot=hot+1 where pid = {pid}".format(pid=pid))

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
    page = int(request.args.get("page",1))
    limit = 10
    mysqlhandle = MysqlHandle(**mysqlconfig)
    news = mysqlhandle.select("select * from news order by addtime desc limit {start},{limit}".format(
        start = (page-1)*limit,
        limit = limit
    ))
    for i in news:
        i['addtime'] = time.strftime("%Y-%m-%d",time.localtime(i['addtime']))
    return render_template(template,news=news)


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
    mysqlhandle = MysqlHandle(**mysqlconfig)
    newsinfo = mysqlhandle.select("select * from news where nid = {nid}".format(nid=nid))
    if newsinfo:
        newsinfo = newsinfo[0]
        newsinfo['addtime'] = time.strftime("%Y-%m-%d", time.localtime(newsinfo['addtime']))
    return render_template(args[0],newsinfo = newsinfo)

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


@index.route("/example/<int:cid>/")
@pc_and_m_transform({"m-template":"home/m-success-example.html","pc-template":"home/success-example.html"})
def sexample(*args,**kwargs):
    '''
     成功案例分类页
    :param args:
    :param kwargs:
    :return:
    '''
    cid = kwargs.get('cid')
    cid = cid if cid else 0
    template = args[0]
    mysqlhandle = MysqlHandle(**mysqlconfig)
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
        examples  = mysqlhandle.select("select * from cases where cate1 = {cid} ORDER  by addtime DESC limit {start},{step}".format(
                                                cid=cid,start=(page-1)*limit,
                                                        step = limit))
    else:
        examples = mysqlhandle.select("select * from cases  ORDER  by addtime DESC limit {start},{step}".format(start=(page-1)*limit,
                                                        step = limit))
    count = len(examples)
    return render_template(template,examples = examples,previous_page = previous_page,
                           next_page = next_page,
                           count =count,
                           cid=cid,page = page)


@index.route("/example/<int:cid>.html")
@pc_and_m_transform({"m-template":"home/m-example-detail.html","pc-template":"home/success-example.html"})
def sexample_desc(*args,**kwargs):
    '''
     成功案例详情页
    :param args:
    :param kwargs:
    :return:
    '''
    cid = kwargs.get('cid')
    template = args[0]
    mysqlhandle = MysqlHandle(**mysqlconfig)
    exampleinfo = mysqlhandle.select("select * from cases where cid = {cid}".format(cid=cid))
    if exampleinfo:
        exampleinfo = exampleinfo[0]
    return render_template(template,exampleinfo = exampleinfo)



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

@index.route("/customization")
def customization():
    '''
    客户留言页
    :return:
    '''
    return render_template("home/m-pc-customization-html.html")
@index.route("/sitemap.xml")
def sitemap():
    mysqlhandle = MysqlHandle(**mysqlconfig)
    _productids = mysqlhandle.select("select pid,addtime from product")
    idlist = [(i.pid,time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(i.addtime)))
              for i in _productids]
    sitemap_xml = render_template('sitemap/sitemap.xml', idlist=idlist)
    response = make_response(sitemap_xml)
    response.headers["Content-Type"] = "application/xml"
    return response


@index.route("/buyuser",methods=['POST'])
def buyuser():
    data = {}
    params = request.form
    if not params:
        params = json.loads(request.data)
    mysqlhandle = MysqlHandle(**mysqlconfig)
    mysqlhandle.other_op("insert into d_customer "
                         "(`tel`,`name`,`email`,`address`,`desc`,`addtimes`) "
                         "VALUES ('{tel}','{name}','{email}','{address}','{desc}',{addtimes})".format(
                            tel=params.get('telnumber'), name=params.get('username'),
                            email=params.get("email"), address=params.get('address'),
                            desc=params.get("userdesc"), addtimes=int(time.time())
                        ))
    data['code'] = 0
    data['msg'] = '提交成功，稍后会有专业的售前工程师与您联系，敬请留意接听电话。'
    return jsonify(data)