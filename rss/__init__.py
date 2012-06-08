#!/usr/bin/env python
#coding: utf8

def get_rss_entries(url, prevtime=None, nhead=0):
    import feedparser
    import sys
    import time
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

        publishtime = getattr(
            e, 'published_parsed',  getattr(
                e, 'updated_parsed', None,
            )
        )

        msg = {
            'title': title, 
            'url': href,
            'content': content,
            'entry': e,
        }
        for i in e:
            msg[i] = mb_code(e[i]) if isinstance(e[i], basestring) else e[i]
        
        if prevtime is None or publishtime is None or publishtime > prevtime:
            statuses.append((msg, publishtime))            
    
    if nhead > 0:
        statuses = statuses[:nhead]

    return statuses


if __name__ == '__main__':
    import sys
    nhead = int(sys.argv[2]) if len(sys.argv) >= 2 else 0
    for msg, publishtime in get_rss_entries(sys.argv[1], None, nhead):
        print msg['title'], msg['url'], msg['content']
        print msg['comments']
