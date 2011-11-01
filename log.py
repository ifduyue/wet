#coding: utf-8

import logging
from lib import get_path

_logger = None

def _init():
    global _logger
    _logger = logging.getLogger('wet')
    _handler = logging.FileHandler(get_data_path('log'))
    _formatter = logging.Formatter('[%(asctime)s]%(message)s', '%Y-%m-%d %H:%M:%S')
    _handler.setFormatter(_formatter)
    _logger.addHandler(_handler)
    _handler = logging.StreamHandler()
    _handler.setFormatter(_formatter)
    _logger.addHandler(_handler)
    _logger.setLevel(logging.DEBUG)
    

def log(msg, *args):
    if _logger is None:
        _init()
    _logger.debug(msg, *args)
    
    
def poor_log(msg, *args):
    from time import strftime
    from lib import get_path
    timestamp = strftime("%Y-%m-%d %H:%M:%S")
    log_file = get_path('log')
    with open(log_file, 'a+b', 0) as f:
        format = "[%s]" % timestamp + msg + "\n"
        f.write(format % args)
