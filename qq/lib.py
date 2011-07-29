#!/usr/bin/env python

def get_conf():
    import conf
    confs = {}
    for i in dir(conf):
        if i.startswith('__'):
            continue
        confs[i] = getattr(conf, i)
    return confs

def set_conf(confs):
    import os
    confile = os.path.join(os.path.dirname(__file__), 'conf.py')
    with open(confile, 'w') as f:
        for k, v in confs.items():
            if isinstance(v, int):
                format = "%s = %s\n"
            elif isinstance(v, basestring):
                format = "%s = '%s'\n"
            else:
                continue
            f.write(format % (k, v))
        return True
    return False

def get_api():
    import sys, os.path
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from qqweibo import OAuthHandler, API
    c = get_conf()
    try:
        o = OAuthHandler(c['consumer_key'], c['consumer_secret'])
        o.setToken(c['access_token_key'], c['access_token_secret'])
    except KeyError, e:
        sys.stderr.write("qq: you should run get_oauthed.py first.\n")
    return API(o)

