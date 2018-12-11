#coding:utf-8
import  sys
reload(sys)
sys.setdefaultencoding("utf-8")
from fake import Fake
item={'title':'重新运行安装程序' ,'content':'里面一般都会记载着怎么安装和怎么使用。部分关于windows系统安装的重要信息翻译后截图如下'}
aaa=Fake(item)
print type(aaa)


