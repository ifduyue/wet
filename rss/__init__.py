#!/usr/bin/env python
#coding: utf8

def get_rss_entries(url, prevtime=None):
    import feedparser
    import sys
    sys.path.insert(0, '..')
    from lib import mb_code, strip_tags
    
    try:
        d = feedparser.parse(url)
    except:
        return []
        
    statuses = []
    for e in d.entries:
        title = mb_code(e.title)
        href = mb_code(e.links[0]['href'])
        try:
            content = mb_code(e.content[0].value)
            content = strip_tags(content) 
        except:
            content = ''
        try:
            publishtime = e.published_parsed 
        except:
            publishtime = e.updated_parsed
        msg = {
            'title': title, 
            'url': href,
            'content': content,
        }
        
        if prevtime is None or publishtime > prevtime:
            statuses.append((msg, publishtime))            
    
    return statuses

