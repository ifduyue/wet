import re
import os

def decodeHtmlentities(string):
    entity_re = re.compile("&(#?)(\d{1,5}|\w{1,8});")

    def substitute_entity(match):
        from htmlentitydefs import name2codepoint as n2cp
        ent = match.group(2)
        if match.group(1) == "#":
            return unichr(int(ent))
        else:
            cp = n2cp.get(ent)

            if cp:
                return unichr(cp)
            else:
                return match.group()

    return entity_re.subn(substitute_entity, string)[0]
    
def fetch(url):
    from socket import setdefaulttimeout
    setdefaulttimeout(10.0)
    import urllib2
    from random import choice
    uas = (
        'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100920 Fedora/3.6.10-1.fc13 Firefox/3.6.10',
        'Mozilla/5.0 (X11; U; Linux i686; zh-CN; rv:1.8.1.19) Gecko/20081202 Firefox (Debian-2.0.0.19-0etch1)',
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; ro; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8',
        'Mozilla/5.0 (X11; U; Gentoo Linux x86_64; pl-PL) Gecko Firefox',
        'Opera/9.99 (Windows NT 5.1; U; pl) Presto/9.9.9',
        'Opera/9.70 (Linux i686 ; U; zh-CN) Presto/2.2.0',
        'Opera 9.7 (Windows NT 5.2; U; en)',
        'Mozilla/5.0 (Windows; U; MSIE 9.0; WIndows NT 9.0; zh-CN))',
        'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.2; Trident/4.0; Media Center PC 4.0; SLCC1; .NET CLR 3.0.04320)',
        'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; zh-CN)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0;)',
        'Mozilla/4.0 (compatible; MSIE 6.1; Windows XP)',
        'Mozilla/4.0 (compatible; MSIE 6.01; Windows NT 6.0)',
        'Mozilla/5.0 (Windows; U; Windows NT 6.0; zh-CN) AppleWebKit/533.1 (KHTML, like Gecko) Maxthon/3.0.8.2 Safari/533.1',
        'sogou spider',
        'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
        'Googlebot/2.1 (+http://www.googlebot.com/bot.html)',
        'Googlebot/2.1 (+http://www.google.com/bot.html)',
        'Mozilla/5.0 (compatible; Yahoo! Slurp China; http://misc.yahoo.com.cn/help.html)',
    )
    headers = {
        'Accept': ' text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'User-Agent': choice(uas)
    }
    request = urllib2.Request(url, headers=headers)
    opener = urllib2.build_opener()
    try:
        f = opener.open(request)
    except Exception, e:
        return False
    if f.getcode() != 200:
        return False
    try:
        data = f.read()
    except Exception, e:
        return False
    if f.headers.get('Content-Encoding', '') == 'gzip':
        try:
            from cStringIO import StringIO
        except ImportError:
            from StringIO import StringIO
        gzipdata = StringIO(data)
        import gzip
        gzipper = gzip.GzipFile(fileobj=gzipdata)
        try:
            data = gzipper.read()
        except (IOError, ValueError), e:
            return False
        except Exception, e:
            return False
    return data
    
def get_path(filename=None):
    HERE = os.path.dirname(os.path.abspath(__file__))
    if filename is not None:
        HERE = os.path.join(HERE, filename)
    return HERE

def get_data_path(filename=None):
    data_dir = get_path("data")
    if not os.path.isdir(data_dir):
        os.makedirs(data_dir)
    return os.path.join(data_dir, filename) if filename is not None else data_dir

def load_prev_time(id):
    id = get_data_path(id)
    return loadfrom(id)

def save_prev_time(id, s):
    id = get_data_path(id)
    return dumpto(id)
    
def read_rss_lasttimes():
    return loadfrom( get_data_path('rss_lasttimes') )
    
def save_rss_lasttimes(obj):
    dumpto( get_data_path('rss_lasttimes'), obj)

def mb_code(string, coding="utf-8"):
    if isinstance(string, unicode):
        return string.encode(coding)
    for c in ('utf-8', 'gb2312', 'gbk', 'gb18030', 'big5'):
        try:
            return string.decode(c).encode(coding)
        except:
            pass
    return string

from log import log
        
def str2js_str(str):
    str = mb_code(str)
    str = unicode(str)
    str = repr(str)
    if str:
        str[2:-1]
    return str

def joinpath(d, f):
    from os.path import sep
    return sep.join([d, f])

def writeto(path, data):
    fh = open(path, 'w')
    fh.write(data)
    fh.close()
    
def readfrom(path):
    fh = open(path, 'r')
    data = fh.read()
    fh.close()
    return data
    
def dumpto(path, obj):
    import pickle
    fh = open(path, 'wb')
    pickle.dump(obj, fh)
    fh.close()
    
def loadfrom(path):
    import pickle
    fh = None
    try:
        fh = open(path, 'rb')
        obj = pickle.load(fh)
    except Exception, e:
        obj = None
    finally:
        if fh: fh.close()
    return obj
    
def isreadablefile(path):
    return os.access(path, os.R_OK)
    
def touch(path):
    try:
        os.utime(path, None)
    except:
        open(path, 'a').close()
        
def mv(f, t):
    import shutil
    shutil.move(f, t)

def unshortenurl(short):
    from urllib import URLopener
    opener = URLopener()
    try:
        opener.open(short)
    except IOError, e:
        f = e
    try:
        f = e.args[3]
        return f.dict['location']
    except:
        return short

def unshortenstatus(status, regex=re.compile(r'''(http://t\.co/\w+|http://bit\.ly/\w+)'''), retries=3):
    while retries:
        retries -= 1
        shortens = regex.findall(status)
        if not shortens:
            break
        for s in shortens:
            url = unshortenurl(s)
            if url != s:
                status = status.replace(s, url)
    return status

def strip_tags(html):
    html = re.sub("<.*?>", " ", html)
    return re.sub("\s+", " ", html)
