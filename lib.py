def decodeHtmlentities(string):
    import re
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
    import os.path
    HERE = os.path.dirname(os.path.abspath(__file__))
    if filename is not None:
        HERE = os.path.join(HERE, filename)
    return HERE   

def load_prev_time(id):
    id = get_path(id)
    try:
        return open(id, 'r').read().strip()
    except:
       	open(id, 'w').write('Thu, 10 Feb 2011 10:08:49 +0000')
    return 'Thu, 10 Feb 2011 10:08:49 +0000'

def save_prev_time(id, s):
    open(get_path(id), 'w').write(s)

def mb_code(string, coding="utf-8"):
    if isinstance(string, unicode):
        return string.encode(coding)
    for c in ('utf-8', 'gb2312', 'gbk', 'gb18030'):
        try:
            return string.decode(c).encode(coding)
        except:
            pass
    return string
    
def log(string):
    log_file = get_path('log')
    with open(log_file, 'a+') as f:
        f.write(string)
        if not string.endswith('\n'):
            f.write('\n')
    



