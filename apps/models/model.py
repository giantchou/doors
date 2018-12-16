# -*- coding: utf-8 -*-
# @author: chenhuachao
# @time: 2018/11/21

# from flask_sqlalchemy import SQLAlchemy
from Doors import app
import time
# from sqlalchemy.pool import NullPool
from apps.setting import  sqlurl
from sqlalchemy import Column, String, create_engine,Integer,Text,MetaData
# from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

Base = declarative_base()
# db = SQLAlchemy(app)



class User(Base):#test table
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


class Cate(Base):
    '''
    分类表
    '''
    __tablename__ = "cate"
    cateid = Column(Integer,primary_key=True)
    name = Column(String(50))
    level = Column(Integer)
    parentid = Column(Integer)



class Products(Base):
    '''
    产品表
    '''
    __tablename__ = "product"
    pid = Column(Integer,primary_key=True)
    title = Column(String(100))
    keyword = Column(String(100))
    abstract = Column(String(255))
    content = Column(Text())
    addtime = Column(Integer)
    from_web = Column(String(255))
    title_img = Column(String(255))
    material = Column(String(100))
    cate1 = Column(Integer)
    cate2 = Column(Integer)
    hot = Column(Integer)
    def format_date(self):
        return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(self.addtime))

class Customer(Base):
    '''
    意向用户留言表
    '''
    __tablename__ = "d_customer"
    id = Column(Integer,primary_key=True)
    tel = Column(String(11),nullable=True)
    name = Column(String(20))
    email = Column(String(30))
    desc = Column(Text)
    address = Column(String(150))
    addtimes = Column(Integer)


class Cases(Base):
    '''
     成功案例表
    '''
    __tablename__ = "cases"
    cid = Column(Integer,primary_key=True)
    title = Column(String(100))
    keyword = Column(String(100))
    abstract = Column(String(255))
    content = Column(Text())
    addtime = Column(Integer)
    from_web = Column(String(255))
    title_img = Column(String(255))
    cate1 = Column(Integer)
    cate2 = Column(Integer)
    area = Column(String(20))

# 初始化数据库连接:
# engine = create_engine(sqlurl,convert_unicode=True,poolclass=NullPool)
# # 创建DBSession类型:
# DBSession = sessionmaker(bind=engine)
# session = DBSession()



metadata = MetaData()
engine = create_engine(sqlurl, encoding='utf-8', pool_recycle=3600)
session = scoped_session(sessionmaker(autocommit=False,
                                      expire_on_commit = False,
                                      autoflush=True,
                                      bind=engine))
metadata.create_all(bind=engine)