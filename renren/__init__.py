#coding: utf8

from urlfetch import fetch, sc2cs
import re

class Renren(object):
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
        
    def login(self):
        response = fetch(
            'http://3g.renren.com/login.do?autoLogin=true',
            headers = {
                'Referer': 'http://m.renren.com/'
            },
            data = {
                'email': self.username,
                'password': self.password,
                'origURL': '',
                'login': '登录',
            },
        )

        self.update_url = "http://3g.renren.com/status/wUpdateStatus.do?"
        self.update_url += response.getheader('location').split('?', 1)[-1]
        self.cookies = sc2cs(response.getheader('Set-Cookie'))
        
        return response
        

    def update(self, status):
        response = fetch(
            #"http://3g.renren.com/status/wUpdateStatus.do",
            self.update_url,
            headers = {
                'Referer': "http://3g.renren.com/home.do",
            },
            data = {
                'empty': 1,
                'pid': '',
                'sour': 'home',
                'status': status,
                'update': '发布',
            },
        )

        return response 
        
        

def pub2renren(username, password, status):
    renren = Renren(username, password)
    renren.login()
    renren.update(status)


if __name == '__main__':
    import sys
    pub2renren(*sys.argv[1:4])
