#coding: utf8

import sys
sys.path.insert(0, '..')
from bc import BC
import re
import urllib
import pycurl

class QQ(BC):
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.cookie_file = username + '.qq_cookie'
        BC.__init__(self)
        self.reset()
        
    def login(self): 
        b, c = self.reset()
        c.setopt(pycurl.URL, 'http://pt.3g.qq.com/microblogLogin')
        c.setopt(pycurl.COOKIEJAR, self.cookie_file)
        c.setopt(pycurl.FOLLOWLOCATION, True)
        c.perform()
        data = b.getvalue()

        post_url = re.search(r'''<go\s+href="(.*?)"''', data).group(1) 
        sid = re.search(r'''name="sid"\s+value="(.*?)"''', data).group(1)
        
        b, c = self.reset()
        c.setopt(pycurl.URL, post_url)
        c.setopt(pycurl.REFERER, 'http://pt.3g.qq.com/microblogLogin')
        c.setopt(pycurl.FOLLOWLOCATION, True)
        c.setopt(pycurl.COOKIEJAR, self.cookie_file)
        c.setopt(pycurl.POST, True)
        c.setopt(pycurl.POSTFIELDS, urllib.urlencode({
            'qq': self.username,
            'pwd': self.password,
            'sid': sid
        })) 
        c.perform()
        data = b.getvalue()
        self.sid = re.search(r'''sid=(.*?)&amp''', data).group(1)
        return data
        
    def update(self, status):
        b, c = self.reset()
        c.setopt(pycurl.COOKIEJAR, self.cookie_file)
        c.setopt(pycurl.URL, "http://ti.3g.qq.com/g/s?sid=%s&aid=h" % self.sid)
        c.setopt(pycurl.REFERER, 'http://ti.3g.qq.com/')
        c.perform()
        data =  b.getvalue()

        post_url = re.search(r'''广播<go\s+href="(.*?)"''', data).group(1)
        post_url = post_url.replace('&amp;', '&')
        msg_id = re.search(r'''name="msg(\d+)"''', data).group(1) 

        b, c = self.reset()
        c.setopt(pycurl.URL, 'http://ti.3g.qq.com' + post_url)
        c.setopt(pycurl.COOKIEJAR, self.cookie_file)
        c.setopt(pycurl.POST, True)
        c.setopt(pycurl.FOLLOWLOCATION, True)
        c.setopt(pycurl.REFERER, "http://ti.3g.qq.com/g/s?sid=%s&aid=h" % self.sid)
        c.setopt(pycurl.POSTFIELDS, urllib.urlencode({
            'msg'+msg_id: status,
            'msg': status,
            'ac': '51',
        }))
        c.perform()
        return b.getvalue()

def pub2qq(username, password, status):
    qq = QQ(username, password)
    qq.login()
    qq.update(status)

