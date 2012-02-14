#coding: utf8

from urlfetch import fetch, sc2cs
import re

class Douban(object):
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.cookies = ''
        
    def login(self):
        response = fetch(
            "http://m.douban.com/"
        )

        set_cookie = response.getheader('Set-Cookie')
        self.cookies = sc2cs(set_cookie)

        self.session = response.getheader('location').split('=', 1)[-1]

        response = fetch(
            "http://m.douban.com/",
            data = {
                'form_email': self.username,
                'form_password': self.password,
                'redir': '',
                'user_login': '登录',
                'session': self.session
            },
            headers = {
                'Referer': 'http://m.douban.com/',
                'Cookie': self.cookies,
            }
        )
        set_cookie = response.getheader('Set-Cookie')
        self.cookies += "; " + sc2cs(set_cookie)

        return response
        
    def update(self, status):
        response = fetch(
            "http://m.douban.com/",
            data = {
                'mb_text': status,
                'session': self.session
            },
            headers = {
                'Referer': 'http://m.douban.com/',
                'Cookie': self.cookies,
            }
        )
        return response
        
_instance = None

def pub2douban(username, password, status):
    global _instance
    if _instance is None:
        douban = Douban(username, password)
        douban.login()
        _instance = douban
    _instance.update(status)
    
if __name__ == '__main__':
    import sys
    pub2douban(*sys.argv[1:4])

