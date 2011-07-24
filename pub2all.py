#!/usr/bin/env python
#coding: utf8

from lib import *

def pub2all(status, savetime=False):
    from renren import pub2renren
    from sina import pub2sina
    from douban import pub2douban
    from facebook import pub2facebook
    import conf
    
    if conf.renren_user and conf.renren_passwd:
        try:
            pub2renren(conf.renren_user, conf.renren_passwd, status)
            if savetime:
                save_prev_time(conf.twitter_user, savetime)
        except Exception, e:
            log('pub2renren error: %s' % str(e))
        
    if conf.sina_user and conf.sina_passwd:
        try:
            pub2sina(status)
            if savetime:
                save_prev_time(conf.twitter_user, savetime)
        except Exception, e:
            log('pub2sina error: %s' % str(e))
            
    if conf.facebook_user and conf.facebook_passwd:
        try:
            pub2facebook(conf.facebook_user, conf.facebook_passwd, status)
            if savetime:
                save_prev_time(conf.twitter_user, savetime)
        except Exception, e:
            log('pub2facebook error: %s' % str(e))
            
    if conf.douban_user and conf.douban_passwd:
        try:
            pub2douban(conf.douban_user, conf.douban_passwd, status)
            if savetime:
                save_prev_time(conf.twitter_user, savetime)
        except Exception, e:
            log('pub2douban error: %s' % str(e))
    
if __name__ == '__main__':
    from sys import argv
    status = argv[1]
    pub2all(mb_code(status))
    



