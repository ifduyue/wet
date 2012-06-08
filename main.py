#!/usr/bin/env python
#coding: utf8
import conf
from conf import re_type
from lib import *
from log import log
from time import sleep, gmtime, strftime
from pub2all import pub2all


def can_pub(status):
    to_exclude = to_include = False

    for i in conf.exclude:
        if isinstance(i, re_type):
            if i.match(status):
                to_exclude = True
                break
        elif isinstance(i, basestring):
            if status.find(i) != -1:
                to_exclude = True
                break
        else:
            if i(status):
                to_exclude = True
                break

    if to_exclude:
        return False
            
    for i in conf.include:
        if isinstance(i, re_type):
            if i.match(status):
                to_include = True
                break
        elif isinstance(i, basestring):
            if status.find(i) != -1:
                to_include = True
                break
        else:
            if i(status):
                to_include = True
                break

    if not conf.include:
        to_include = True

    if not to_include:
        return False

    return True


def twitter2all():
    from twitter import get_twitter_status
    
    prevtime = load_prev_time(conf.twitter_user)
    statuses = get_twitter_status(conf.twitter_user, prevtime)
    
    if not statuses: return
    
    if prevtime is None:
        log("first time fetch %s's tweets, skip", conf.twitter_user)
        save_prev_time(conf.twitter_user, statuses[-1][1])
        return
    
    maxtime = prevtime
    for status, pubdate in statuses:

        if not can_pub(status):
            log("[skipping] %s can not be published because of include and exlucde conf", status)
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
        format_, url = feed[0:2]
        nhead = feed[2] if feed[2:] else 0
        lasttime = lasttimes.get(url, None)
        if lasttime is None:
            log("first time fetching %s, skip", url)
            lasttimes[url] = gmtime()
            lasttimes['entries_' + url] = []
            save_rss_lasttimes(lasttimes)
            continue
        
        statuses = get_rss_entries(url, lasttime, nhead=nhead)
        maxtime = lasttime
        
        for entry, publishtime in statuses:
            status = format_ % entry

            if not can_pub(status):
                log("[skipping] %s can not be published because of include and exlucde conf", status)
                continue

            if entry in lasttimes['entries_' + url]:
                log("[skipping] %s can not be published because it has already bean published",  status)
                continue

            log("[publishing] %s : %s",
                strftime("%Y-%m-%d %H:%M:%S", publishtime) if publishtime is not None else 'None',
                status,
            )

            if pub2all(status):
                if publishtime is not None and maxtime < publishtime:
                    maxtime = publishtime
                
                lasttimes['entries_' + url].append(entry)

                sleep(10)
            
        lasttimes[url] = maxtime if maxtime != lasttime else gmtime()
        lasttimes['entries_' + url] = lasttimes['entries_' + url][-100:]

        save_rss_lasttimes(lasttimes)


if __name__ == '__main__':
    log("start...")
    twitter2all()
    feeds2all()
    log("finish...")
