#!/usr/bin/env python
#coding: utf8
import conf
from lib import *
from log import log
from time import sleep, gmtime, strftime
from pub2all import pub2all

def twitter2all():
    from twitter import get_twitter_status
    
    prevtime = load_prev_time(conf.twitter_user)
    statuses = get_twitter_status(conf.twitter_user, prevtime)
    
    if prevtime is None:
        log("first time fetch %s's tweets, skip", conf.twitter_user)
        save_prev_time(conf.twitter_user, statuses[-1][1])
        return
    
    maxtime = prevtime
    for status, pubdate in statuses:
        if conf.exclude:
            if status[0] in conf.exclude:
                continue
                
        if conf.include:
            to_include = False
            for i in conf.include:
                if status.find(i) != -1:
                    to_include = True
                    break
            if not to_include:
                continue

        log("[publishing] %s : %s",
            pubdate,
            status,
        )
        
        if pub2all(status) and maxtime < pubdate:
            maxtime = pubdate
            sleep(10)
    save_prev_time(conf.twitter_user, maxtime)
        
def feeds2all():
    from rss import get_rss_entries
    
    lasttimes = read_rss_lasttimes()
    if lasttimes is None:
        lasttimes = {}
        
    for format_, url in conf.feeds:
        lasttime = lasttimes.get(url, None)
        if lasttime is None:
            log("first time fetching %s, skip", url)
            lasttimes[url] = gmtime()
            save_rss_lasttimes(lasttimes)
            continue
        
        statuses = get_rss_entries(url, lasttime)
        maxtime = lasttime
        
        for status, publishtime in statuses:
            status = format_ % status
            
            log("[publishing] %s : %s",
                strftime("%Y-%m-%d %H:%M:%S", publishtime),
                status,
            )

            if pub2all(status) and maxtime < publishtime:
                maxtime = publishtime
                sleep(10)
            
        lasttimes[url] = maxtime
        save_rss_lasttimes(lasttimes)

if __name__ == '__main__':
    log("start...")
    twitter2all()
    feeds2all()
    log("finish...")
