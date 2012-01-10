

def shurl(url, timeout=3):
    from urlfetch import post
    try:
        response = post("http://shurl.im/", data={'url': url}, timeout=timeout)
        url = response.getheader('location', url)
    except: pass
    return url
