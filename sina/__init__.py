#coding: utf8
import StringIO
import re
import urllib
import pycurl

class Sina:
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.cookie_file = username + '.sina_cookie'
        self.b = StringIO.StringIO()
        self.c = pycurl.Curl()
        self.reset()
    
    def reset(self):
        b = self.b
        c = self.c
        b.truncate()
        c.reset()
        c.setopt(pycurl.WRITEFUNCTION, b.write)
        return b,c
        
    def login(self):
        b, c = self.reset()
        c.setopt(pycurl.COOKIEJAR, self.cookie_file)
        c.setopt(pycurl.URL, "http://login.sina.com.cn/sso/login.php")
        c.setopt(pycurl.REFERER, 'http://t.sina.com.cn/')
        c.setopt(pycurl.POST, True)
        c.setopt(pycurl.FOLLOWLOCATION, True)
        c.setopt(pycurl.POSTFIELDS, urllib.urlencode({
            'entry': 'miniblog',
            'username': self.username,
            'password': self.password,
            'encoding': 'utf-8',
        }))
        c.perform()
        return b.getvalue()
        
    def update(self, status, pic=''):
        b, c = self.reset()
        c.setopt(pycurl.COOKIEJAR, self.cookie_file)
        c.setopt(pycurl.URL, "http://t.sina.com.cn/mblog/publish.php")
        c.setopt(pycurl.REFERER, 'http://t.sina.com.cn/')
        c.setopt(pycurl.POST, True)
        c.setopt(pycurl.FOLLOWLOCATION, True)
        c.setopt(pycurl.POSTFIELDS, urllib.urlencode({
            'content': status,
            'pic': pic,
            'styleid': '1',
            'retcode': ''
        }))
        c.perform()
        return b.getvalue()
