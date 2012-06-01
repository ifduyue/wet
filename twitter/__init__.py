#coding: utf8

import sys
sys.path.insert(0, '..')
from lib import *
import re
import urllib
from urlfetch import get

from conf import unshorten_prefix, use_shurl
unshorten_re = []
for i in unshorten_prefix:
    unshorten_re.append(re.escape(i) + r'[/\w]+')
unshorten_re = '(%s)' % '|'.join(unshorten_re)
unshorten_re = re.compile(unshorten_re)
    

def get_twitter_status(username, prevtime=None):
    from lib import mb_code
    from datetime import datetime
    ptime = prevtime if prevtime is not None else False
        
    url = 'http://twitter.com/statuses/user_timeline/%s.rss' %  username
    try:
        data = get(url).body
    except: return []

    from xml.dom import minidom
    try:
        tree = minidom.parseString(data)
    except:
        return []
    desc = tree.getElementsByTagName('description')[1:]
    date = tree.getElementsByTagName('pubDate')
    
    statuses = []
    lst = range(len(desc)-1, -1, -1)
    prefix = '%s: ' % username
    prefix_len = len(prefix)
    for i in lst:
        try:
            status = mb_code(decodeHtmlentities(desc[i].childNodes[0].data))
            if status.startswith(prefix): status = status[prefix_len:]
        except: continue
        pubdate = mb_code(date[i].childNodes[0].data)
        pubdate = datetime.strptime(pubdate , '%a, %d %b %Y %H:%M:%S +0000')
        if ptime is False or pubdate > ptime:
            if unshorten_prefix:
                status = unshortenstatus(status, unshorten_re)
            if use_shurl:
                status = shurl_status(status)
            statuses.append((status, pubdate))
    
    return statuses


if __name__ == '__main__':
    for i in get_twitter_status('newsycombinator'):
        print i

