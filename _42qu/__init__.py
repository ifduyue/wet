#coding: utf8

from urlfetch import fetch, sc2cs
import re
from urlparse import urljoin

class _42qu(object):
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.cookies = ''
        
    def login(self):
        response = fetch(
            "http://42qu.com/auth/login",
            headers = {
                'Referer': 'http://42qu.com/',
                'User-Agent': 'Opera/9.60',
            }
        )
        self.xsrf = re.search(
            '''name="_xsrf".*?value="(.*?)"''',
            response.body
        ).group(1)
        set_cookie = response.getheader('Set-Cookie')
        self.cookies = sc2cs(set_cookie)
        
        response =fetch(
            "http://42qu.com/auth/login",
            data = {
                '_xsrf': self.xsrf,
                'mail': self.username,
                'password': self.password,
            },
            headers = {
                'Referer': 'http://42qu.com/auth/login',
                'User-Agent': 'Opera/9.60',
                'Cookie': self.cookies,
            }
        )

        if response.getheader('location'):
            self.eurl = urljoin(
                "http://42qu.com/auth/login",
                response.getheader('location')
            )
        else:
            raise Exception("Unknown error")
            
        set_cookie = response.getheader('Set-Cookie')
        self.cookies += "; " + sc2cs(set_cookie)
        print self.cookies
            
        return response

    def update(self, status):
        url = self.eurl.replace('/live', '/po/word')
        response = fetch(
            url,
            data = {
                'txt': status,
                '_xsrf': self.xsrf,
            },
            headers = {
                'Referer': self.eurl,
                'Cookie': self.cookies,
            }
        )
        return response


def pub2_42qu(username, password, status):
    o = _42qu(username, password)
    o.login()
    o.update(status)

if __name__ == '__main__':
    import sys
    pub2_42qu(*sys.argv[1:4])
