#!/usr/bin/env python
#coding: utf8

def get_rss_entries(url, prevtime=None):
    import feedparser
    import sys
    sys.argv.insert(0, '..')
    from lib import mb_code
    
    try:
        d = feedparser.parse(url)
    except:
        return []
        
    statuses = []
    for e in d.entries:
        title = mb_code(e.title)
        href = mb_code(e.links[0]['href'])
        publishtime = e.updated_parsed
        msg = {'title': title, 'url': href}
        
        if prevtime is None or publishtime > prevtime:
            statuses.append((msg, publishtime))            
    
    return statuses
