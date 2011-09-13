#coding: utf8
import sys
sys.path.insert(0, '..')
from bc import BC
import re
import urllib
import pycurl

class _42qu(BC):
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.cookie_file = '/dev/null'
        BC.__init__(self)
        self.reset()
        
    def login(self):
        b, c = self.reset()
        c.setopt(pycurl.URL, "http://42qu.com/auth/login")
        c.setopt(pycurl.REFERER, 'http://42qu.com/')
        c.setopt(pycurl.COOKIEJAR, self.cookie_file)
        c.perform()
        data = b.getvalue()
        xsrf = re.search('''name="_xsrf".*?value="(.*?)"''', data).group(1)
        self.xsrf = xsrf

        b, c = self.reset()
        c.setopt(pycurl.COOKIEJAR, self.cookie_file)
        c.setopt(pycurl.URL, "http://42qu.com/auth/login")
        c.setopt(pycurl.POST, True)
        c.setopt(pycurl.POSTFIELDS, urllib.urlencode({
            '_xsrf': xsrf,
            'mail': self.username,
            'password': self.password,
        }))
        try:
            c.perform()
        except pycurl.error, e:
            if e.args[0] != 47: raise
        self.eurl = c.getinfo(pycurl.EFFECTIVE_URL) 
        self.eurl = self.eurl.replace('42qu.com//','')
        #self.eurl = self.eurl.replace('/live', '')
        return b.getvalue()

    def update(self, status):
        b, c = self.reset()
        c.setopt(pycurl.COOKIEJAR, self.cookie_file)
        c.setopt(pycurl.URL, self.eurl.replace('/live', '/po/word'))
        c.setopt(pycurl.REFERER, self.eurl)
        c.setopt(pycurl.POST, True)
        c.setopt(pycurl.POSTFIELDS, urllib.urlencode({
            'txt': status,
            '_xsrf' : self.xsrf,
        }))
        c.perform()
        return b.getvalue()


def pub2_42qu(username, password, status):
    o = _42qu(username, password)
    o.login()
    o.update(status)
