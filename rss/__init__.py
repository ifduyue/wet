#!/usr/bin/env python
#coding: utf8

def get_rss_entries(url, prevtime=None):
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
            e, 'published_parsed', 
            getattr(
                e, 'updated_parsed', 
                time.strptime('1988-10-25', '%Y-%m-%d')
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
        
        if prevtime is None or publishtime > prevtime:
            statuses.append((msg, publishtime))            
    
    return statuses


if __name__ == '__main__':
    import sys
    for msg, publishtime in get_rss_entries(sys.argv[1]):
        print msg['title'], msg['url'], msg['content']
