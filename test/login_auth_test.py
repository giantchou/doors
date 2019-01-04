# -*- coding: utf-8 -*-
# @author: chenhuachao
# @time: 2019/1/4
import time
from hashlib import sha1
import requests
api_key = '123456'
security_key = 'qykgkajogajjgaiagjlagjl'


def main():
    timestrap = str(int(time.time()))
    random_str = 'qwerasdfzxcvbgty'
    sort_str = ''.join(sorted([api_key, timestrap, random_str, security_key], reverse=False))
    _sha1= sha1()
    _sha1.update(sort_str.encode())
    sign = _sha1.hexdigest()
    url ='http://127.0.0.1:5000/api/test/?api_key='+api_key+"&timestrap="+timestrap+"&random_str="+random_str+"&sign="+sign
    resq = requests.get(url)
    print(resq.json())


if __name__ == '__main__':
    main()