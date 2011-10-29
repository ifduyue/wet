#coding: utf-8

import logging
from lib import get_path

_logger = None
_handler = None
_formatter = None

def _init():
    global _logger, _handler, _formatter
    _logger = logging.getLogger('wet')
    _handler = logging.FileHandler(get_path('log'))
    _formatter = logging.Formatter('[%(asctime)s]%(message)s', '%Y-%m-%d %H:%M:%S')
    _handler.setFormatter(_formatter)
    _logger.addHandler(_handler)
    _logger.addHandler(logging.StreamHandler())
    _logger.setLevel(logging.DEBUG)
    

def log(msg, *args):
    if _logger is None:
        _init()
    _logger.debug(msg, *args)