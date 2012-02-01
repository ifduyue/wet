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
    return dumpto(id, s)
    
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

def unshortenurl(short, retries=3):
    from urlfetch import get
    while retries:
        retries -= 1
        try:
            # if we use a browser's user-agent
            # t.co will not send location head
            # it just output:
            # <noscript><META http-equiv="refresh" content="0;URL=http://j.mp/zaycIO"></noscript><script>location.replace("http:\/\/j.mp\/zaycIO")</script>
            # that's awkward!!
            response = get(short, randua=False, timeout=3)
            long_ = response.getheader('location')
            if long_ is None:
                break
            short = long_
        except: pass 

    return short

def unshortenstatus(status, regex, retries=3):
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

def shurl_status(status):
    from shurl import shurl
    urls = re.findall(
        'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+~]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', 
        status,
    )
    for url in urls:
        short = shurl(url)
        if short != url:
            status = status.replace(url, short)
    return status
        

def strip_tags(html):
    html = re.sub("<.*?>", " ", html)
    return re.sub("\s+", " ", html)
