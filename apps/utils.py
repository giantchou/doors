# -*- coding: utf-8 -*-
# @author: chenhuachao
# @time: 2018/11/22

from flask import request
from functools import wraps



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
            _check = lambda x: x.startswith('192.168') or x.startswith("m.")
            if _check(host):
                args = args.__add__((params.get('m-template'),))
                return func(*args,**kwargs)
            else:
                args = args.__add__((params.get('pc-template'),))
                return func(*args,**kwargs)
        return _logic
    return wrapper
