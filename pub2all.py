#!/usr/bin/env python
#coding: utf8

from lib import *
from log import log

def pub2all(status, entry=None):
    from renren import pub2renren
    from sina import pub2sina
    from douban import pub2douban
    from facebook import pub2facebook
    from qq import pub2qq
    from fanfou import pub2fanfou
    from _42qu import pub2_42qu
    from v2ex import pub2v2ex
    import conf
    
    flag = False
    
    if conf.renren_user and conf.renren_passwd:
        try:
            pub2renren(conf.renren_user, conf.renren_passwd, status)
            flag = True
        except Exception, e:
            log('[pub2renren error][%s] %s', e, status)
        
    if conf.sina_user and conf.sina_passwd:
        try:
            pub2sina(status)
            flag = True
        except Exception, e:
            log('[pub2sina error][%s] %s', e, status)
            
    if conf.facebook_user and conf.facebook_passwd:
        try:
            pub2facebook(conf.facebook_user, conf.facebook_passwd, status)
            flag = True
        except Exception, e:
            log('[pub2facebook error][%s] %s', e, status)
            
    if conf.douban_user and conf.douban_passwd:
        try:
            pub2douban(conf.douban_user, conf.douban_passwd, status)
            flag = True
        except Exception, e:
            log('[pub2douban error][%s] %s', e, status)

    if conf.qq_user and conf.qq_passwd:
        try:
            pub2qq(status)
            flag = True
        except Exception, e:
            log('[pub2qq error][%s] %s', e, status)
    
    if conf.fanfou_user and conf.fanfou_passwd:
        try:
            pub2fanfou(conf.fanfou_user, conf.fanfou_passwd, status)
            flag = True
        except Exception, e:
            log('[pub2fanfou error][%s] %s', e, status)
            
    if conf._42qu_user and conf._42qu_passwd:
        try:
            pub2_42qu(conf._42qu_user, conf._42qu_passwd, status)
            flag = True
        except Exception, e:
            log('[pub2_42qu error][%s] %s', e, status)

    if conf.v2ex_user and conf.v2ex_passwd:
        if entry is None:
            title = status
            content = ''
        else:
            title = entry['title']
            content = status

        try:
            pub2v2ex(conf.v2ex_user, conf.v2ex_passwd, title, content, conf.v2ex_node)
            flag = True
        except Exception, e:
            log('[pub2v2ex error][%s] %s', e, status)

    return flag

            
if __name__ == '__main__':
    from sys import argv
    status = argv[1]
    pub2all(mb_code(status))
    



