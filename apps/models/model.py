# -*- coding: utf-8 -*-
# @author: chenhuachao
# @time: 2018/11/21

from flask_sqlalchemy import SQLAlchemy
from Doors import app
import time


db = SQLAlchemy(app)



class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


class Cate(db.Model):
    __tablename__ = "cate"

    cateid = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50))
    level = db.Column(db.Integer)
    parentid = db.Column(db.Integer)



class Products(db.Model):
    __tablename__ = "product"
    pid = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100))
    keyword = db.Column(db.String(100))
    abstract = db.Column(db.String(255))
    content = db.Column(db.Text())
    addtime = db.Column(db.Integer)
    from_web = db.Column(db.String(255))
    title_img = db.Column(db.String(255))
    material = db.Column(db.String(100))
    cate1 = db.Column(db.Integer)
    cate2 = db.Column(db.Integer)
    hot = db.Column(db.Integer)
    def format_date(self):
        return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(self.addtime))