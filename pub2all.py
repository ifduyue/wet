#!/usr/bin/env python
#coding: utf8

from lib import *

def pub2all(status):
    from renren import pub2renren
    from sina import pub2sina
    from douban import pub2douban
    from facebook import pub2facebook
    from qq import pub2qq
    from fanfou import pub2fanfou
    from _42qu import pub2_42qu
    import conf
    
    flag = False
    
    if conf.renren_user and conf.renren_passwd:
        try:
            pub2renren(conf.renren_user, conf.renren_passwd, status)
            flag = True
        except Exception, e:
            log('pub2renren error: %s' % str(e))
        
    if conf.sina_user and conf.sina_passwd:
        try:
            pub2sina(status)
            flag = True
        except Exception, e:
            log('pub2sina error: %s' % str(e))
            
    if conf.facebook_user and conf.facebook_passwd:
        try:
            pub2facebook(conf.facebook_user, conf.facebook_passwd, status)
            flag = True
        except Exception, e:
            log('pub2facebook error: %s' % str(e))
            
    if conf.douban_user and conf.douban_passwd:
        try:
            pub2douban(conf.douban_user, conf.douban_passwd, status)
            flag = True
        except Exception, e:
            log('pub2douban error: %s' % str(e))

    if conf.qq_user and conf.qq_passwd:
        try:
            pub2qq(status)
            flag = True
        except Exception, e:
            log('pub2qq error: %s' % str(e))
    
    if conf.fanfou_user and conf.fanfou_passwd:
        try:
            pub2fanfou(conf.fanfou_user, conf.fanfou_passwd, status)
            flag = True
        except Exception, e:
            log('pub2fanfou error: %s' % str(e))

    if conf._42qu_user and conf._42qu_passwd:
        try:
            pub2_42qu(conf._42qu_user, conf._42qu_passwd, status)
            flag = True
        except Exception, e:
            log('pub2_42qu error: %s' % str(e))

    return flag

            
if __name__ == '__main__':
    from sys import argv
    status = argv[1]
    pub2all(mb_code(status))
    



