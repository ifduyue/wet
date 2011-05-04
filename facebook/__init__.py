#coding: utf8
import StringIO
import re
import urllib
import pycurl

class Facebook:
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.cookie_file = username + '.facebook_cookie'
        self.b = StringIO.StringIO()
        self.c = pycurl.Curl()
        self.reset()
    
    def reset(self):
        b = self.b
        c = self.c
        b.truncate(0)
        c.reset()
        c.setopt(pycurl.WRITEFUNCTION, b.write)
        return b,c
        
    def login(self): 
        b, c = self.reset()
        c.setopt(pycurl.COOKIEJAR, self.cookie_file)
        c.setopt(pycurl.URL, "http://m.facebook.com/")
        c.setopt(pycurl.REFERER, 'http://m.facebook.com/')
        c.setopt(pycurl.USERAGENT, 'Opera/9.60')
        c.setopt(pycurl.FOLLOWLOCATION, True)
        c.setopt(pycurl.COOKIEJAR, self.cookie_file)
        c.perform()
        m = re.search('''name="post_form_id" value="([^"]+?)"''', b.getvalue())
        self.post_form_id = m.group(1)

        b, c = self.reset()
        c.setopt(pycurl.COOKIEJAR, self.cookie_file)
        c.setopt(pycurl.URL, "https://www.facebook.com/login.php?m=m&refsrc=http%3A%2F%2Fm.facebook.com%2F&refid=0")
        c.setopt(pycurl.REFERER, 'http://m.facebook.com/')
        c.setopt(pycurl.USERAGENT, 'Opera/9.60')
        c.setopt(pycurl.FOLLOWLOCATION, True)
        c.setopt(pycurl.COOKIEJAR, self.cookie_file)
        c.setopt(pycurl.POST, True)
        c.setopt(pycurl.POSTFIELDS, urllib.urlencode({
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
        }))
        c.perform()
        self.post_form_id = re.search('''name="post_form_id" value="([^"]+?)"''', b.getvalue()).group(1)
        self.fb_dtsg = re.search('''name="fb_dtsg" value="([^"]+?)"''', b.getvalue()).group(1)
        print self.post_form_id
        print self.fb_dtsg
        return b.getvalue()
        
    def update(self, status):
        b, c = self.reset()
        c.setopt(pycurl.COOKIEJAR, self.cookie_file)
        c.setopt(pycurl.URL, "http://m.facebook.com/a/home.php?refid=7")
        c.setopt(pycurl.REFERER, 'http://m.facebook.com/')
        c.setopt(pycurl.USERAGENT, 'Opera/9.60')
        c.setopt(pycurl.POST, True)
        c.setopt(pycurl.FOLLOWLOCATION, True)
        c.setopt(pycurl.POSTFIELDS, urllib.urlencode({
            'post_form_id': self.post_form_id,
            'charset_test': "€,´,€,´,水,Д,Є",
            'status': status,
            'fb_dtsg': self.fb_dtsg,
            'update': 'Share',
            'r2a': '1',
        }))
        c.perform()
        return b.getvalue()
