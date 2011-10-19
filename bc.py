#!/usr/bin/env python
#coding: utf8

import pycurl
try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO

class BC:

    def __init__(self):
        self.c = pycurl.Curl()
        self.b = StringIO()
        self.h = ''

    def reset(self):
        b, c = self.b, self.c
        self.h = '' 
        b.truncate(0)
        c.reset()
        c.setopt(pycurl.WRITEFUNCTION, b.write)
        c.setopt(pycurl.CONNECTTIMEOUT, 5)
        c.setopt(pycurl.TIMEOUT, 10)
        c.setopt(pycurl.USERAGENT, 'Opera/9.60')
        c.setopt(pycurl.FOLLOWLOCATION, True)
        c.setopt(pycurl.MAXREDIRS, 5)
        '''
        c.setopt(pycurl.HEADERFUNCTION, self.headerfunction)
        c.setopt(pycurl.HTTPHEADER, [
            "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            'Accept-Language: en-US, zh-CN',
        ])
        '''
        return b, c

    def headerfunction(self, h):
        self.h += h
