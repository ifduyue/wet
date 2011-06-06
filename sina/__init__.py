def pub2sina(status):
    from lib import get_api
    o = get_api()
    o.update_status(status)