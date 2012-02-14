#coding: utf8

from urlfetch import fetch, sc2cs
import re

class Fanfou(object):
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.cookies = ''
        
    def login(self):
        response = fetch(
            "http://m.fanfou.com/"
        )
        token = re.search('''name="token".*?value="(.*?)"''', response.body).group(1)
        
        response = fetch(
            "http://m.fanfou.com/",
            data = {
                'loginname': self.username,
                'loginpass': self.password,
                'action': 'login',
                'token': token,
                'auto_login': 'on',
            },
            headers = {
                "Referer": "http://m.fanfou.com/",
            }
        )
        set_cookie = response.getheader('Set-Cookie')
        self.cookies = sc2cs(set_cookie)
        return response.body

    def update(self, status):
        response = fetch(
            "http://m.fanfou.com/home",
            headers = {
                'Cookie': self.cookies,
                'Referer': "http://m.fanfou.com/home",
            }
        )
        token = re.search('''name="token".*?value="(.*?)"''', response.body).group(1)
        response = fetch(
            "http://m.fanfou.com/",
            data = {
                'content': status,
                'token': token,
                'action': 'msg.post',
            },
            headers = {
                'Cookie': self.cookies,
                'Referer': "http://m.fanfou.com/home",
            }
        )
        return response.body

_instance = None

def pub2fanfou(username, password, status):
    global _instance
    if _instance is None:
        fanfou = Fanfou(username, password)
        fanfou.login()
        _instance = fanfou
    _instance.update(status)

if __name__ == '__main__':
    import sys
    pub2fanfou(*sys.argv[1:4])

