import StringIO
import re
import urllib
import pycurl
class Renren:
    origURL = "http://www.renren.com/SysHome.do"
    domain = "renren.com"
    login_action = "http://www.renren.com/PLogin.do"
    update_action = "http://status.renren.com/doing/updateNew.do"
    comment_action = "http://gossip.renren.com/gossip.do"
    log_comment_action = "http://blog.renren.com/PostComment.do"
    cookie_file = "renren_cookie"
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.cookie_file = username + '.renren_cookie'
        
    def login(self):
        b = StringIO.StringIO()
        c = pycurl.Curl()
        c.setopt(pycurl.WRITEFUNCTION, b.write)
        c.setopt(pycurl.COOKIEJAR, self.cookie_file)
        c.setopt(pycurl.URL, self.login_action)
        c.setopt(pycurl.POST, True)
        c.setopt(pycurl.FOLLOWLOCATION, True)
        c.setopt(pycurl.POSTFIELDS, urllib.urlencode({'email':self.username, 'password':self.password, 'autoLogin':'true', 'origURL':self.origURL, 'domain':self.domain}))
        c.perform()
        m = re.search("get_check:'([^']*)'", b.getvalue())
        self.token = m.group(1)
        
    def update(self, status):
        b = StringIO.StringIO()
        c = pycurl.Curl()
        c.setopt(pycurl.WRITEFUNCTION, b.write)
        c.setopt(pycurl.URL, self.update_action)
        c.setopt(pycurl.POST, True)
        c.setopt(pycurl.POSTFIELDS, urllib.urlencode({'content':status, 'isAtHome':'1', 'requestToken': self.token}))
        c.setopt(pycurl.COOKIEFILE, self.cookie_file)
        c.setopt(pycurl.FOLLOWLOCATION, True)
        c.setopt(pycurl.REFERER, 'http://status.renren.com/ajaxproxy.htm')
        c.perform()
        return b.getvalue()
        
    def comment(self, guest_id, msg):
        b = StringIO.StringIO()
        c = pycurl.Curl()
        c.setopt(pycurl.WRITEFUNCTION, b.write)
        c.setopt(pycurl.URL, self.comment_action)
        c.setopt(pycurl.POST, True)
        post = urllib.urlencode({
            'requestToken': self.token,
            'only_to_me': '0',
            'id': guest_id,
            'cc': guest_id,
            'body': msg,
            'ak': 'fd72dd7cef6104812bfeaad1c74fe9d2',
            'profilever': '2008',
            'ref': 'http://www.renren.com/profile.do',
            'mode': '',
            'largeUrl': '',
            'headUrl': '',
            'curpage': '',
            'color': '',
            'cccc': '',
            'from': 'main',
            'tsc': '',
        })
        c.setopt(pycurl.POSTFIELDS, post)
        c.setopt(pycurl.COOKIEFILE, self.cookie_file)
        c.setopt(pycurl.FOLLOWLOCATION, True)
        c.setopt(pycurl.REFERER, 'http://www.renren.com/profile.do')
        c.setopt(pycurl.USERAGENT, '	Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.13) Gecko/20101209 Fedora/3.6.13-1.fc14 Firefox/3.6.13')
        c.perform()
        return b.getvalue()
        
    def log_comment(self, owner, log_id, msg):
        b = StringIO.StringIO()
        c = pycurl.Curl()
        c.setopt(pycurl.WRITEFUNCTION, b.write)
        c.setopt(pycurl.URL, self.log_comment_action)
        c.setopt(pycurl.POST, True)
        post = urllib.urlencode({
            'requestToken': self.token,
            'to': '0',
            'only_to_me': '0',
            'id': log_id,
            'body': msg,
            'owner': owner,
        })
        c.setopt(pycurl.POSTFIELDS, post)
        c.setopt(pycurl.COOKIEFILE, self.cookie_file)
        c.setopt(pycurl.FOLLOWLOCATION, True)
        c.setopt(pycurl.REFERER, 'http://www.renren.com/profile.do')
        c.setopt(pycurl.USERAGENT, '	Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.13) Gecko/20101209 Fedora/3.6.13-1.fc14 Firefox/3.6.13')
        c.perform()
        return b.getvalue()
        
