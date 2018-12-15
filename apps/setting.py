# -*- coding: utf-8 -*-
# @author: chenhuachao
# @time: 2018/11/21

# 数据库配置信息
# engine = ''
# username = ''
# password = ''
# port = 3306
# db_name = ''
import socket
debug = True
if debug:
    sqlurl = 'mysql+pymysql://root:123456@127.0.0.1:3306/doors' #测试
else:
    sqlurl = 'mysql+pymysql://mha_user:gc895316@127.0.0.1:3306/doors' #正式