#coding: utf8
import sys
sys.path.insert(0, '..')
from bc import BC
import re
import urllib
import pycurl

class Douban(BC):
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.cookie_file = '/dev/null'
        BC.__init__(self)
        self.reset()
        
    def login(self):
        b, c = self.reset()
        c.setopt(pycurl.COOKIEJAR, self.cookie_file)
        c.setopt(pycurl.URL, "http://m.douban.com/")
        c.setopt(pycurl.REFERER, 'http://m.douban.com/')
        c.setopt(pycurl.USERAGENT, 'Opera/9.60')
        c.setopt(pycurl.FOLLOWLOCATION, True)
        c.perform()
        m = re.search('''href="/\?session=([^'"]+?)"''', b.getvalue())
        self.session = m.group(1)
        print self.session
        
        b, c = self.reset()
        c.setopt(pycurl.COOKIEJAR, self.cookie_file)
        c.setopt(pycurl.URL, "http://m.douban.com/")
        c.setopt(pycurl.REFERER, 'http://m.douban.com/')
        c.setopt(pycurl.USERAGENT, 'Opera/9.60')
        c.setopt(pycurl.FOLLOWLOCATION, True)
        c.setopt(pycurl.POST, True)
        c.setopt(pycurl.POSTFIELDS, urllib.urlencode({
            'form_email': self.username,
            'form_password': self.password,
            'redir': '',
            'user_login': '登录',
            'session': self.session
        }))
        c.perform()
        return b.getvalue()
        
    def update(self, status):
        b, c = self.reset()
        c.setopt(pycurl.COOKIEJAR, self.cookie_file)
        c.setopt(pycurl.URL, "http://m.douban.com/")
        c.setopt(pycurl.REFERER, 'http://m.douban.com/')
        c.setopt(pycurl.USERAGENT, 'Opera/9.60')
        c.setopt(pycurl.POST, True)
        c.setopt(pycurl.FOLLOWLOCATION, True)
        c.setopt(pycurl.POSTFIELDS, urllib.urlencode({
            'mb_text': status,
            'session': self.session
        }))
        c.perform()
        return b.getvalue()
        

def pub2douban(username, password, status):
    douban = Douban(username, password)
    douban.login()
    douban.update(status)
    
