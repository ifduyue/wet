wet
===

By @lyxint <lyxint@gmail.com>

同步tweets和feeds更新到facebook/新浪微博/腾讯微博/豆瓣/人人/饭否等

prerequirements
===============


[urlfetch](http://pypi.python.org/pypi/urlfetch):

    easy_install -U urlfetch

使用方法
--------
- **一台墙外的server, 否则取不到twitter feed**
- 编辑conf.py, 填入twitter帐号和feeds地址
- 编辑conf.py, 填入要同步到的帐号和密码
    - 同步到腾讯微博
        * sh qq/download_qqweibo.sh
        * 去open.t.qq.com申请一个应用, 编辑qq/conf.py, 填入consumer_key和consumer_secret
        * python qq/get_oauthed.py使自己的qq微博帐号和应用绑定
    - 同步到新浪微博
        * sh sina/download_sinatpy.sh
        * 去open.weibo.com申请一个应用, 编辑sina/conf.py填入consumer_key和consumer_secret
        * python sina/get_oauthed.py使自己的weibo帐号和应用绑定
    - 把main.py加入crontab, 间隔自己掂量, 我设置的是每5分钟一次


TODO
----
 * 基于tornado写一个web端
 * 把sina的oauth改成python模拟发推, 不然xx会就被封了. 
 * [DONE] 加入douban, facebook等的支持
