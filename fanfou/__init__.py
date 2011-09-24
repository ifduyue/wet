#coding: utf8
import sys
sys.path.insert(0, '..')
from bc import BC
import re
import urllib
import pycurl

class Fanfou(BC):
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.cookie_file = '/dev/null'
        BC.__init__(self)
        self.reset()
        
    def login(self):
        b, c = self.reset()
        c.setopt(pycurl.URL, "http://m.fanfou.com/")
        c.setopt(pycurl.REFERER, 'http://m.fanfou.com/')
        c.perform()
        data = b.getvalue()
        token = re.search('''name="token".*?value="(.*?)"''', data).group(1)
        
        b, c = self.reset()
        c.setopt(pycurl.COOKIEJAR, self.cookie_file)
        c.setopt(pycurl.URL, "http://m.fanfou.com/home")
        c.setopt(pycurl.REFERER, 'http://m.fanfou.com/')
        c.setopt(pycurl.POST, True)
        c.setopt(pycurl.POSTFIELDS, urllib.urlencode({
            'loginname': self.username,
            'loginpass': self.password,
            'action': 'login',
            'token' : token,
            'auto_login': 'on',
        }))
        c.perform()
        return b.getvalue()

    def update(self, status):
        b, c = self.reset()
        c.setopt(pycurl.COOKIEJAR, self.cookie_file)
        c.setopt(pycurl.URL, "http://m.fanfou.com/home")
        c.setopt(pycurl.REFERER, 'http://m.fanfou.com/home')
        c.perform()
        data = b.getvalue()
        token = re.search('''name="token".*?value="(.*?)"''', data).group(1)
        
        b, c = self.reset()
        c.setopt(pycurl.COOKIEJAR, self.cookie_file)
        c.setopt(pycurl.URL, "http://m.fanfou.com/home")
        c.setopt(pycurl.REFERER, 'http://m.fanfou.com/home')
        c.setopt(pycurl.POST, True)
        c.setopt(pycurl.POSTFIELDS, urllib.urlencode({
            'content': status,
            'token' : token,
            'action': 'msg.post',
        }))
        c.perform()
        return b.getvalue()


def pub2fanfou(username, password, status):
    fanfou = Fanfou(username, password)
    fanfou.login()
    return fanfou.update(status)

