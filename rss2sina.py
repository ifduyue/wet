#!/usr/bin/env python
#coding: utf8

from lib import *
from time import sleep, gmtime
from sina import pub2sina
import conf
from conf import feeds

def rss2sina():
    from rss import get_rss_entries
    lasttimes = loadfrom('rss_lasttimes')
    if lasttimes is None:
        lasttimes = {}
        
    for url in feeds:
        lasttime = lasttimes.get(url, gmtime(-3600*24))
        statuses = get_rss_entries(url, lasttime)
        maxtime = lasttime
        
        for status, publishtime in statuses:
            if conf.sina_user and conf.sina_passwd:
                try:
                    pub2sina(status)
                    print status
                    if maxtime < publishtime:
                        maxtime = publishtime
                    sleep(10)
                except Exception, e:
                    log('pub2sina error: %s' % str(e))
        
        lasttimes[url] = maxtime
        dumpto('rss_lasttimes', lasttimes)
            
if __name__ == '__main__':
    rss2sina()
    
