#coding:utf-8

import scrapy
import sys
import MySQLdb.cursors
import MySQLdb
import re
import upyun
import time
import requests

reload(sys)
sys.setdefaultencoding('utf-8')

UPYUN_BUCKETNAME = 'doors'
UPYUN_USERNAME = 'doors360'
UPYUN_PASSWORD = 'doors360.cn'
UPYUN_BASE_URL = "https://upyun.doors360.cn"

def upload_img(_imgdata,extname):
    def up_to_upyum(key, value):
        up_conn = upyun.UpYun(UPYUN_BUCKETNAME, UPYUN_USERNAME, UPYUN_PASSWORD)
        up_headers = {}
        up_conn.put(key, value, checksum=True, headers=up_headers)
        return UPYUN_BASE_URL + key
    try:
        _file = _imgdata
        filename = str(time.time()).replace('.', '_') + extname
        image_key = "/image_upload/" + filename
        url = up_to_upyum(image_key, _file)
        return {"status": True, "filename": filename, "imgurl": url}
    except Exception:
        return {"status": False, "message": 'Err'}

def Transfer(_url):
    response = requests.get(_url)
    _imgdata = response.content
    extname="." + _url.split(".")[-1].split("?")[0]
    if "/" in extname:
        extname = ".jpg"
    new_name = upload_img(_imgdata, extname)
    return new_name

###采集金洋九峰官网的数据###
class tbSpider(scrapy.Spider):
    name = "tbSpider"
    allowed_domains = ["jyjf.com.cn"]
    start_urls = ['http://www.jyjf.com.cn/Product/']
    global Mysql_conf, My_cxn, My_cur
    Mysql_conf = {
        'host': '47.92.116.232',
        'user': 'mha_user',
        'passwd': 'gc895316',
        'db': 'doors',
        'charset': 'utf8',
        'init_command': 'set autocommit=0',
        'cursorclass': MySQLdb.cursors.DictCursor
    }
    My_cxn = MySQLdb.connect(**Mysql_conf)
    My_cur = My_cxn.cursor()

    def parse(self, response):
        a = [{'url': u'www.jyjf.com.cn/xfzdm.htm', 'cate2': 16L, 'cate1': 1L},
             {'url': u'www.jyjf.com.cn/wgxfm.htm', 'cate2': 17L, 'cate1': 1L},
             {'url': u'www.jyjf.com.cn/sspym.htm', 'cate2': 18L, 'cate1': 1L},
             {'url': u'www.jyjf.com.cn/lhjddssm.htm', 'cate2': 19L, 'cate1': 2L},
             {'url': u'www.jyjf.com.cn/bxgddssm.htm', 'cate2': 20L, 'cate1': 2L},
             {'url': u'www.jyjf.com.cn/tytydm.htm', 'cate2': 21L, 'cate1': 3L},
             {'url': u'www.jyjf.com.cn/lybsdm.htm', 'cate2': 22L, 'cate1': 3L},
             {'url': u'www.jyjf.com.cn/bxgtydm.htm', 'cate2': 23L, 'cate1': 3L},
             {'url': u'www.jyjf.com.cn/zndz.htm', 'cate2': 29L, 'cate1': 5L},
             {'url': u'www.jyjf.com.cn/rxtdz.htm', 'cate2': 30L, 'cate1': 5L},
             {'url': u'www.jyjf.com.cn/cpzdsbtcgl.htm', 'cate2': 31L, 'cate1': 5L},
             {'url': u'www.jyjf.com.cn/scstccglxt.htm', 'cate2': 32L, 'cate1': 5L},
             {'url': u'www.jyjf.com.cn/lywl.htm', 'cate2': 33L, 'cate1': 6L}]

        urls = response.xpath('//div[@class="sedNav"]/p/a')
        for _url in urls:
            item = self.get_cate(_url.xpath('text()').extract()[0], My_cxn, My_cur)
            url = _url.xpath('@href').extract()[0]
            if 'jyjf.com' not in url:
                url = 'www.jyjf.com.cn' + url
            item['url'] = url
            print item['url'], item
            yield scrapy.Request(item['url'], callback=self.page_list, dont_filter=True, meta={'item': item})

    def page_list(self, response):
        print response.url, '~~~123~~~'
        item = response.meta['item']
        urls = response.xpath('//ul[@class="cpshow"]/li/a')
        for index, _url in enumerate(urls):
            item['title'] = urls[index].xpath('@title').extract()[0]
            item['url'] = 'www.jyjf.com.cn'+urls[index].xpath('@href').extract()[0]
            if self.check_url(item, My_cxn, My_cur):
                continue
            yield scrapy.Request(item['url'], callback=self.page_desc, dont_filter=True, meta={'item': item})

    def page_desc(self, response):
        item = response.meta['item']
        item['url'] = response.url
        INFO, img_check_list = [], []
        item['material'] = response.xpath('//div[@id="protop"]/ul[@class="ul_prodinfo"]/li[@class="li_normalprice"]/text()').extract()[0]
        INFO = response.xpath('//div[@id="contentvalue100"]/p/node()').extract()
        item['addtime'] = int(time.time())
        '''
        info = response.xpath('//div[@class="text-main"]//node()').extract()
        _info = [re.sub(r'<.*?>', r'', _i).replace(' ', '') for _i in info]
        for index, i in enumerate(info):
            if self.check_stop_wird(i.strip()) or _info[index] in img_check_list:
                continue
            else:
                img_check_list.append(_info[index])
            i = re.sub(r'<img(.*?)src="(.*?)".*?>', r'<img src="\2">', i)
            i = re.sub(r'<span(.*?)>', r'<span>', i)
            i = re.sub(r'<p(.*?)>', r'<p>', i)
            try:
                img_url = re.search(r'<img src="(.*?)">', i).group()
            except :
                pass
            else:
                if img_url in img_check_list:
                    continue
                else:
                    img_check_list.append(img_url)
                    """将图片放入到又拍云上"""
                    src_img_url = img_url[10:-2]
                    new_img = Transfer(src_img_url)
                    if new_img['status']:
                        i = re.sub(r'<img src="(.*?)">', '<img src="'+new_img['imgurl'] + '">', i)

            INFO.append(i.replace(r'threebao.com', r'bao361.cn').strip())
        '''
        item['content'] = "".join(INFO)
        return item

    ###检测 文章URL 是否已经采集过,防止重复采集###
    def check_url(self, item, My_cxn, My_cur):
        try:
            My_cxn.ping()
        except:
            My_cxn = MySQLdb.connect(**Mysql_conf)
            My_cur = My_cxn.cursor()
        SQL = "SELECT pid FROM product WHERE from_web='%s'"
        My_cur.execute(SQL % item['url'])
        result = My_cur.fetchall()
        if result:
            return True
        else:
            My_cur.execute("SELECT pid FROM product WHERE title='%s'" % item['title'])
            result = My_cur.fetchall()
            if result:
                return True
        return False

    ###检测###
    def get_cate(self, catename, My_cxn, My_cur):
            try:
                My_cxn.ping()
            except:
                My_cxn = MySQLdb.connect(**Mysql_conf)
                My_cur = My_cxn.cursor()
            SQL = "SELECT cateid AS cate2,parentid AS cate1 FROM cate WHERE `name` LIKE '%%%s%%'"
            My_cur.execute(SQL % catename)
            result = My_cur.fetchone()
            if result:
                return result
            else:
                return {'cate1': 0, 'cate2': 0}

    ###检测是否存在需要过滤的词###
    def check_stop_wird(self, Str):
        stopword_list = ['</script', '<script ', 'var sogou_ad', 'm.threebao.com/',
                       'class="digg PageSListPage">', '<div class="newsDaoDu">', u'导读：',
                       'threebao.com/uploadfile/2017/0225/20170225010322749.gif',
                       'threebao.com/uploadfile/2018/0613/20180613110251847.gif',
                       'threebao.com/uploadfile/2018/0613/20180613113626232.gif',
                       'threebao.com/uploadfile/2016/1018/20161018045542139.png',
                       'threebao.com/index.php?m=formguide&c=index&a=show&formid=12&siteid=1',
                       'threebao.com/index.php?']
        for sw in stopword_list:
            if sw in Str:
                return True
        else:
            return False
