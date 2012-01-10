#coding: utf8

from urlfetch import fetch, sc2cs
import re

class Facebook(object):
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.cookies = ''
        
    def login(self):
        response = fetch(
            "http://m.facebook.com/"
        )
        
        m = re.search('''name="post_form_id" value="([^"]+?)"''', response.body)
        self.post_form_id = m.group(1)
        
        response = fetch(
            "https://www.facebook.com/login.php?m=m&refsrc=http%3A%2F%2Fm.facebook.com%2F&refid=0",
            data = {
                'lsd': 'off',
                'charset_test': "€,´,€,´,水,Д,Є",
                'version': '1',
                'ajax': '1',
                'width': '1280',
                'pxr': '1',
                'email': self.username,
                'pass': self.password,
                'submit': 'Log In',
                'post_form_id': self.post_form_id,
            },
            headers = {
                'Referer': 'http://m.facebook.com/',
            }
        )

        set_cookie = response.getheader('Set-Cookie')
        self.cookies = sc2cs(set_cookie)
        
        url = response.getheader('location')
        response = fetch(
            url,
            headers = {
                'Referer': 'http://m.facebook.com/',
                'Cookie': self.cookies,
            },
        )

        self.post_form_id = re.search(
            '''name="post_form_id" value="([^"]+?)"''',
            response.body
        ).group(1)
        self.fb_dtsg = re.search(
            '''name="fb_dtsg" value="([^"]+?)"''',
            response.body
        ).group(1)

        return response
        
    def update(self, status):
        response = fetch(
            "http://m.facebook.com/a/home.php?refid=7",
            data = {
                'post_form_id': self.post_form_id,
                'charset_test': "€,´,€,´,水,Д,Є",
                'status': status,
                'fb_dtsg': self.fb_dtsg,
                'update': 'Share',
                'r2a': '1',
            },
            headers = {
                'Referer': 'http://m.facebook.com/',
                'Cookie': self.cookies,
            }
        )
        return response

def pub2facebook(username, password, status):
    facebook = Facebook(username, password)
    facebook.login()
    facebook.update(status)

if __name__ == '__main__':
    import sys
    pub2facebook(*sys.argv[1:4])
