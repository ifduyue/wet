#!/usr/bin/env python

from qqweibo import OAuthHandler
from lib import *

def main():
    c = get_conf()
    o = OAuthHandler(c['consumer_key'], c['consumer_secret'])
    c['authorization_url'] = o.get_authorization_url()
    c['request_token'] = o.request_token
    print c['authorization_url']
    verifier = raw_input('click the url above, then input the verifier: ')
    verifier = verifier.strip()
    c['verifier'] = verifier
    try:
        access_token = o.get_access_token(verifier)
        c['access_token_key'] = access_token.key
        c['access_token_secret'] = access_token.secret
        c['access_token'] = access_token.to_string()
        set_conf(c)
        print 'oauth succeeded'
    except:
        print 'oauth failed'

if __name__ == '__main__':
    main()
