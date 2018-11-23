#coding=utf-8
from flask import Flask
from apps.index.index import index
from apps.news.news import news
from apps.case.case import case
from apps.product.product import product

app = Flask(__name__)
app.register_blueprint(index, url_prefix = '/')
app.register_blueprint(news, url_prefix = '/news')
app.register_blueprint(case, url_prefix = '/case')
app.register_blueprint(product, url_prefix = '/product')

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5555)
