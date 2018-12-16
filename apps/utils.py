# -*- coding: utf-8 -*-
# @author: chenhuachao
# @time: 2018/11/22

from flask import request
from functools import wraps

intcheck = lambda x: int(x) if x else 1
limitcheck = lambda x: int(x) if x else 10

def pc_and_m_transform(params):
    '''
    M站和PC站的切换装饰器
    :param params:
    :return:
    '''
    def wrapper(func):
        @wraps(func)
        def _logic(*args,**kwargs):
            host = request.host
            _check = lambda x: x.startswith('192.168') or x.startswith('10') or x.startswith("m.")
            if _check(host):
                args = args.__add__((params.get('m-template'),))
                return func(*args,**kwargs)
            else:
                args = args.__add__((params.get('pc-template'),))
                return func(*args,**kwargs)
        return _logic
    return wrapper
