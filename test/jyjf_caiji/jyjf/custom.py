#coding:utf-8
import sys
import MySQLdb
import upyun
import random
import urllib2
from gcutils.encrypt import md5

import time
reload(sys)
sys.setdefaultencoding("utf-8")

class Yun_Img_Handle(object):
    """
    对微信群相关的图片进行处理，将采集过来的群二维码图片、群主二维码图片转存到我们自己的又拍云存储下，转存成功则返回新的图片链接地址
    需要传入的参数有：
        _url : 源站的图片链接
    """
    def __init__(self, _url):
        self._url = _url

    ###将图片传送到又拍云上###
    def img_new_url(self):
        UPYUN_BUCKETNAME = 'wximage-upyun'
        UPYUN_USERNAME = 'mm123456'
        UPYUN_PASSWORD = 'mm123456'
        UPYUN_BASE_URL = "https://upyun.91weixinqun.cn"

        _url=self._url
        request = urllib2.Request(_url)
        request.headers["Upgrade-Insecure-Requests"] = 1
        request.headers[
            "User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36 QQBrowser/4.2.4718.400"
        request.headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
        _imgdata = urllib2.urlopen(request, timeout=3).read()

        extname = "." + _url.split(".")[-1]
        if "/" in extname:
            extname = ".jpg"
        if '?' in extname:
            extname = extname.split('?')[0]

        def up_to_upyum(key, value):
            up_conn = upyun.UpYun(UPYUN_BUCKETNAME, UPYUN_USERNAME, UPYUN_PASSWORD)
            up_headers = {}
            up_conn.put(key, value, checksum=True, headers=up_headers)
            return UPYUN_BASE_URL + key

        filename = md5(str(time.time()) + str(random.random())) + extname
        image_key = "/image_upload_api/" + filename
        url = up_to_upyum(image_key, _imgdata)

        return url

class Repeat_Check(object):
    '''
    针对指定的字段内容进行重复度检测，已存在返回True 不存在返回False
    需要传入的参数有：
       host ：mysql主机ip
       user ：mysql用户名
       pwd  ：mysql密码
       db   ：mysql的库名
       table：mysql的表名
       field：需要查询的字段
       check_item:需要检测的字段内容
    '''
    def __init__(self,host,user,pwd,db,table):
        Mysql_conf = {
            'host': host,
            'user': user,
            'passwd': pwd,
            'db': db,
            'charset': 'utf8',
            'init_command': 'set autocommit=0'
        }
        self.My_cxn = MySQLdb.connect(**Mysql_conf)
        self.My_cur =self.My_cxn.cursor()
        self.table = table
    '''检测指定字段的内容，确认是否存在，存在返回True 不存在返回False'''
    def check(self,field,check_item):
        SQL = "SELECT * FROM %s WHERE %s='%s'"
        self.My_cur.execute(SQL % (self.table,field,check_item))
        result = self.My_cur.fetchall()
        if result:
            return True
        else:
            return False
    '''获取cateid 如果该分类不存在，则插入新的分类然后把新id返回'''
    def get_cateid(self,cate1_name,cate2_name):
        if len(cate2_name) == 0:
            return 4,27
        self.My_cur.execute("SELECT cateid,parentid FROM cate_info WHERE catename LIKE '%%%s%%'"%cate2_name)
        result = self.My_cur.fetchone()
        if result:
            return result[1],result[0]
        else:
            try:
                self.My_cur.execute("SELECT cateid,parentid FROM cate_info WHERE catename LIKE '%%%s%%'"%cate1_name)
                result = self.My_cur.fetchone()
                if result :
                    cate1=result[0]
                    self.My_cur.execute("INSERT INTO cate_info(cateid,catename,parentid,root,`level`) VALUES(NULL,'%s',%s,0,2)"%(cate2_name,cate1))
                    self.My_cxn.commit()
                    return cate1,self.My_cur.lastrowid
                else:
                    if len(cate1_name) == 0:
                        return 4,27
                    self.My_cur.execute("INSERT INTO cate_info(cateid,catename,parentid,root,`level`) VALUES(NULL,'%s',0,0,1)"%cate1_name)
                    self.My_cxn.commit()
                    cate1=self.My_cur.lastrowid
                    self.My_cur.execute("INSERT INTO cate_info(cateid,catename,parentid,root,`level`) VALUES(NULL,'%s',%s,0,2)"%(cate2_name, cate1))
                    self.My_cxn.commit()
                    return cate1,self.My_cur.lastrowid
            except Exception,e:
                print e
                return 4, 27

    '''获取areaid 根据县、市、区等名称获取相应的 省id、市id'''
    def get_areaid(self, province, city):
        if '不限区域' in city or '所有地区' in city:
            province_id,city_id = 0,0
        else :
            try:
                if '/' == city[-1]:
                    city = city[:-1]
            except :
                pass
            area=city.split('/')[-1]
            if len(area) > 0 :
                self.My_cur.execute("SELECT id,parentid FROM area WHERE shortname='%s'"%area)
                Area_id = self.My_cur.fetchone()
                city_id = Area_id[0] if Area_id else 0
                province_id = Area_id[1] if Area_id else city_id
            else :
                city_id=0
                self.My_cur.execute("SELECT id,parentid FROM area WHERE shortname='%s'" % province.split('/')[0])
                Area_id = self.My_cur.fetchone()
                province_id = Area_id[0] if Area_id else 0

        return province_id,city_id