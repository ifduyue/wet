#!/usr/bin/env python
#coding: utf8

def twitter2all():
    from time import sleep
    from pub2all import pub2all
    from conf import twitter_user, exclude
    from lib import load_prev_time
    from twitter import get_twitter_status
    
    prevtime = load_prev_time(twitter_user)
    statuses = get_twitter_status(twitter_user, prevtime)
    
    for status, pubdate in statuses:
        if status[0] in exclude:
            continue
        print pubdate, status
        pub2all(status, pubdate)
        sleep(10)


if __name__ == '__main__':
    twitter2all()
