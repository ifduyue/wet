#-*- coding: utf8 -*-
import sys
sys.path.append('..')
from lib import *
def get_twitter_status(username, prevtime):
    from datetime import datetime
    ptime = datetime.strptime(prevtime, '%a, %d %b %Y %H:%M:%S +0000')
    url = 'http://twitter.com/statuses/user_timeline/%s.rss' %  username
    data = fetch(url)
    if not data:
        return []
    from xml.dom import minidom
    try:
        tree = minidom.parseString(data)
    except:
        return []
    desc = tree.getElementsByTagName('description')[1:]
    date = tree.getElementsByTagName('pubDate')
    
    statuses = []
    lst = range(len(desc))
    lst.reverse()
    prefix = '%s: ' % username
    prefix_len = len(prefix)
    for i in lst:
        try:
            status = decodeHtmlentities(mb_code(desc[i].childNodes[0].data))
            if status.startswith(prefix): status = status[prefix_len:]
        except: continue
        pubdate = date[i].childNodes[0].data
        if datetime.strptime(pubdate , '%a, %d %b %Y %H:%M:%S +0000') > ptime:
            statuses.append((status, pubdate))
    
    return statuses
