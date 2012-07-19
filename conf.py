#coding: utf8

import re
re_type = type(re.compile('foo'))

#short url starts with i, for i in unshorten_prefix, will be unshortened
unshorten_prefix = [
    'http://t.co/',
    'http://bit.ly/',
    'http://goo.gl/',
    'http://j.mp/',
]

# use http://shurl.im/ to shorten url in the status
# this make sure the status is less than 140 characters
use_shurl = True

# including status which meets the conditions in `include tuple`
# leave empty to turn this feature off
include = ()

# excluding status which meets the conditions in `exclude tuple`
# leave empty to turn this feature off
exclude = (re.compile(r'^\.'), re.compile(r'^@'), )

'''
feeds example:
feeds = [
    ('[Blog] %(title)s %(url)s', 'http://lyxint.com/feed'),
    ('[GR] %(title)s %(url)s', 'http://www.google.com/reader/public/atom/user/15661637287258318760/state/com.google/broadcast'),
]
'''
feeds = [

]

#Accounts
twitter_user = ''
sina_user = ''
sina_passwd = ''
renren_user = ''
renren_passwd =''
douban_user = ''
douban_passwd = ''
facebook_user = ''
facebook_passwd = ''
qq_user = ''
qq_passwd = ''
fanfou_user = ''
fanfou_passwd = ''
_42qu_user = ''
_42qu_passwd = ''
v2ex_user = ''
v2ex_passwd = ''
