#coding:utf-8
import sys
import requests
import jieba.posseg as pseg
from snownlp import SnowNLP
import json
import js2py
import re
import time
reload(sys)
sys.setdefaultencoding("utf-8")

'''
word_len:文本长度
zhaiyao:摘要信息
titile:标题
kw:关键词
before_content:处理前的文本
later_content:经过翻译之后拼接后的文本
data:{"src":要翻译的词,"tgt:翻译之后转换的结果}
'''

class Fake(object):
    '''
    item 形式{title:xxxx ,content:xxx}

    '''
    def __init__(self,item):
        if isinstance(item,dict):
            s = requests.session()
            result = s.get('http://fanyi.baidu.com/')
            cookie = result.cookies.values()
            T = int(time.time())

            self.headers = {
                "Accept-Language": 'zh-CN,zh;q=0.9,en;q=0.8',
                "Connection": 'keep-alive',
                "Content-Length": '162',
                "Content-Type": 'application/x-www-form-urlencoded; charset=UTF-8',
                "Referer": 'http://fanyi.baidu.com/',
                "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
                "X-Requested-With": 'XMLHttpRequest',
                "Origin": 'http://fanyi.baidu.com',
                "Host": 'fanyi.baidu.com',
                "Cookie":"%s=%s:%s=%s"%('BAIDUID',result.cookies.values()[0],'locale',result.cookies.values()[1])
                #"Cookie":'''BAIDUID=%s; BIDUPSID=%s; PSTM=%d; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; H_PS_PSSID=1427_21095_18559_20928; BDUSS=JaN3ltUmNGcTN4UDNkMjg2eUJHaTVrYnRyWldMRnZRanZldUJCbXpjRn4wT05hQVFBQUFBJCQAAAAAAAAAAAEAAABky88Qc2hvcmluZ2Nob3cAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAH9DvFp~Q7xac2; PSINO=5; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; locale=zh; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=%d; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=%d,%d,%d'''%(cookie[0],cookie[0][:-5],T-36000,T,T-72000,T-7200,T)
            }
            print self.headers.get('Cookie')
            a = js2py.eval_js('function a(r,o){for(var t=0;t<o.length-2;t+=3){var a=o.charAt(t+2);a=a>="a"?a.charCodeAt(0)-87:Number(a),a="+"===o.charAt(t+1)?r>>>a:r<<a,r="+"===o.charAt(t)?r+a&4294967295:r^a}return r}var C=null;var hash=function(r,_gtk){var o=r.length;o>30&&(r=""+r.substr(0,10)+r.substr(Math.floor(o/2)-5,10)+r.substr(-10,10));var t=void 0,t=null!==C?C:(C=_gtk||"")||"";for(var e=t.split("."),h=Number(e[0])||0,i=Number(e[1])||0,d=[],f=0,g=0;g<r.length;g++){var m=r.charCodeAt(g);128>m?d[f++]=m:(2048>m?d[f++]=m>>6|192:(55296===(64512&m)&&g+1<r.length&&56320===(64512&r.charCodeAt(g+1))?(m=65536+((1023&m)<<10)+(1023&r.charCodeAt(++g)),d[f++]=m>>18|240,d[f++]=m>>12&63|128):d[f++]=m>>12|224,d[f++]=m>>6&63|128),d[f++]=63&m|128)}for(var S=h,u="+-a^+6",l="+-3^+b+-f",s=0;s<d.length;s++)S+=d[s],S=a(S,u);return S=a(S,l),S^=i,0>S&&(S=(2147483647&S)+2147483648),S%=1e6,S.toString()+"."+(S^h)}')
            self.token = re.findall(r"token: '(.*)'", result.text)[0]
            gtk = re.findall(r"gtk = '(.*)';",result.text)[0]
            self.sign = a(gtk, u'处理前的文本')
            self.title = item.get('title')
            self.content = item.get('content')
            print cookie
            print gtk,result.cookies.keys()

        else:
            self.title = ''
            self.content = ''
        content = self.get_result()
    def get_result(self):
        kw = []
        if self.content:
            print "~~~~~~~~1~~~~2~~~~3~~~~~~~~~"
            summary = SnowNLP(self.content).summary()
            words = pseg.cut(self.content)
            for word,flag in words:
                # print word,flag
                if flag== 'v':
                    pass
                else:
                    kw.append(word)
            if not isinstance(self.content,unicode):
                self.content  = unicode(self.content,'utf-8')
            #是否对特殊字符进行处理？
            # for i  in ' n!"#$%&()*+,-./:;<=>?@[\]^_`{|}~':
            #     self.content.replace('', i)
            #content = self.content.encode('gbk').decode('gbk')
            content=self.content
            word_len = len(content)
            sign=self.sign
            token=self.token
            headers=self.headers
        else:
            print "~~~~~~~~1~2~3~~~~~~~~~"
            content = ''
            summary = ''
            word_len = 0
        if  content:
            original_percent = 0.5
            cut_words = content[int(round(word_len * original_percent)):]
            #print "截取后的词",cut_words
            try:
                print "~~~~~~~~1===2===3~~~~~~~~~"
                #中文转韩文zh_to_kor
                data = requests.post("http://fanyi.baidu.com/v2transapi",data={"from": "zh", "to": "kor","sign":sign,"token":token,
                                                                                     "query": cut_words, "transtype": "translang",
                                                                                 "simple_means_flag": "3"},timeout=10,headers=headers)
                response = data.text
                print response
                translate_result_kor = json.loads(response).get("trans_result").get("data")[0].get("dst")
                if translate_result_kor:
                    # 韩文转化为中文kor_to_zh
                    data = requests.post("http://fanyi.baidu.com/v2transapi", data={"from": "kor", "to": "zh","sign":sign,"token":token,
                                                                            "query": translate_result_kor,
                                                                            "transtype": "translang",
                                                                            "simple_means_flag": "3"},timeout=10,headers=headers)
                    response = data.text
                    translate_result = json.loads(response).get("trans_result").get("data")[0].get("dst")
                else:
                    translate_result = ''
            except Exception as  e:
                translate_result = ''
                print str(e)
            if translate_result:
                #对翻译后对文章进行拼接
                join_content=content[:int(round(word_len * original_percent))]+translate_result
                print join_content
                print self.url
            else:
                join_content=content
        else:
            join_content,cut_words,translate_result=content,'',''
        return {'title':self.title,'kw':set(kw),'zhaiyao':summary,'later_content':join_content,'before_content':self.content,'word_len':word_len,"data":[{'src':cut_words,"tgt":translate_result}]}
