from renren import Renren
from sina import pub2sina
from douban import Douban
from facebook import Facebook
from twitter import get_twitter_status
from lib import *
from conf import *

def pub2renren(status):
    renren = Renren(renren_user, renren_passwd)
    renren.login()
    renren.update(status)

def pub2douban(status):
    douban = Douban(douban_user, douban_passwd)
    douban.login()
    douban.update(status)

def pub2facebook(status):
    facebook = Facebook(facebook_user, facebook_passwd)
    facebook.login()
    facebook.update(status)


def main():
    from time import sleep
    prevtime = load_prev_time(twitter_user)
    statuses = get_twitter_status(twitter_user, prevtime)
    for status, pubdate in statuses:
        if status.startswith('.') or status.startswith('@'):
            continue
        print pubdate, status
        if sina_user and sina_passwd:
            try:
                pub2sina(status)
                save_prev_time(twitter_user, pubdate)
            except Exception, e:
                log('pub2sina error: %s' % str(e))
        
        if douban_user and douban_passwd:
            try:
                pub2douban(status)
                save_prev_time(twitter_user, pubdate)
            except Exception, e:
                log('pub2douban error: %s' % str(e))

        if facebook_user and facebook_passwd:
            try:
                pub2facebook(status)
                save_prev_time(twitter_user, pubdate)
            except Exception, e:
                log('pub2facebook error: %s' % str(e))
        
        if renren_user and renren_passwd:
            try:
                pub2renren(status)
                save_prev_time(twitter_user, pubdate)
            except Exception, e: 
                log('pub2renren error: %s' % str(e))
        sleep(10)


if __name__ == '__main__':
    main()
