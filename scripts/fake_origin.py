#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     test002
   Description :
   Author :       chou
   date：          2018/12/27
-------------------------------------------------
   Change Activity:
                   2018/12/27:
-------------------------------------------------
创建中文的伪原创函数，可以通过外部调用直接使用该函数，方便快捷
"""
import requests
import hashlib
import time
import sys
import json
import random
reload(sys)
sys.setdefaultencoding('utf8')

def md(Str):
    md = hashlib.md5()
    md.update(Str.encode())
    return md

def fake_origin_youdao(origin_word):
    appkey_list = [{'appid': '350c1b23eec0e75a', 'Key': 'i10wUwuDLZzYNlc8ePABLCzaLdAJ16fV'},
                   {'appid': '32e261c4f0887ede', 'Key': 'J7go9vxOwXbYsqyIkbt2BhD5ej5ZXKHe'},
                   {'appid': '6eef5c5df08c16a5', 'Key': 'pXSEhA5syXrsbhxxsQxHTbPkLIE94i33'}]
    appkey = random.choice(appkey_list)
    fromLang = 'zh-CHS'
    toLang = 'ko'
    salt = int(time.time())
    data = requests.post("http://openapi.youdao.com/api",
                         data={"from": fromLang, "to": toLang, "q": origin_word, "appKey": appkey['appid'], "salt": str(salt),
                               "sign": md(appkey['appid'] + origin_word + str(salt) + appkey['Key']).hexdigest()},
                         timeout=10)
    response = data.text
    print(response)
    translate_result = json.loads(response)['translation'][0]
    if translate_result:
        _data = requests.post("http://openapi.youdao.com/api",
                             data={"from": toLang, "to": fromLang, "q": translate_result, "appKey": appkey['appid'], "salt": str(salt),
                                   "sign": md(appkey['appid'] + translate_result + str(salt) + appkey['Key']).hexdigest()},
                             timeout=10)
        Response = _data.text
        Translate_result = json.loads(Response)['translation'][0]
    else:
        Translate_result = origin_word
    return Translate_result

def fake_origin_baidu(origin_word):
    appkey_list=[{'appid': 20181227000252607, 'Key': 'na5bNsNBPweyEi1XuXyJ'},
                 {'appid': 20181227000252702, 'Key': 'I4dzITywGgDkIxY9PBfl'},
                 {'appid': 20181227000252810, 'Key': 'p6VIKrCeV4jeOxI4mbUs'},
                 {'appid': 20181227000252827, 'Key': 'e4P6gYmD_Y0BiXu5_Eug'}]
    appkey=random.choice(appkey_list)
    salt = int(time.time())
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    }
    try:
        # 中文转韩文zh_to_kor
        data = requests.post("http://api.fanyi.baidu.com/api/trans/vip/translate",
                             data={"from": "zh", "to": "kor", "q": origin_word, "appid": appkey['appid'], "salt": salt,
                                   "sign": md(str(appkey['appid'])+origin_word+str(salt)+appkey['Key']).hexdigest()},
                             headers=headers, timeout=10)
        response = data.text
        translate_result_kor = json.loads(response).get("trans_result")[0].get("dst")
        if translate_result_kor:
            # 韩文转化为中文kor_to_zh
            _data = requests.post("http://api.fanyi.baidu.com/api/trans/vip/translate",
                                 data={"from": "kor", "to": "zh", "q": translate_result_kor, "appid": appkey['appid'],
                                       "salt":salt,"sign": md(str(appkey['appid'])+translate_result_kor+str(salt)+appkey['Key']).hexdigest()},
                                 headers=headers, timeout=10)
            Response = _data.text
            translate_result = json.loads(Response).get("trans_result")[0].get("dst")
        else:
            print('翻译成韩语失败~~~')
            translate_result = origin_word
    except Exception as e:
        translate_result = origin_word
        print(e)
    return translate_result

def main():
    origin_word = '包含了中英翻译和小语种翻译功能,如有其它疑问，可在此提交意见和反馈'
    fake_word = fake_origin_youdao(origin_word)
    #fake_word = fake_origin_baidu(origin_word)
    print(fake_word)

if __name__ == '__main__':
    main()

