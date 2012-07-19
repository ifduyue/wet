#coding: utf8

import urlfetch
import re

class V2ex(object):
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session = urlfetch.Session(headers={'Referer': 'http://v2ex.com/'})
        
    def login(self):
        self.session.post('http://v2ex.com/signin', data={'u': self.username, 'p': self.password})
        print self.session.cookies
        return 'auth' in self.session.cookies
    
    def update(self, title, content='', node="blog"):
        r = self.session.post(
            "http://v2ex.com/new/" + node,
            data = {'title': title, 'content': content}
        )
        return r
        

_instance = None

def pub2v2ex(username, password, title, content='', node=None):
    global _instance
    if _instance is None:
        v2ex = V2ex(username, password)
        v2ex.login()
        _instance = v2ex
    if node is not None:
        _instance.update(title, content, node)
    else:
        _instance.update(title, content)

if __name__ == '__main__':
    import sys
    pub2v2ex(*sys.argv[1:4])

