#coding: utf-8

import logging
from lib import get_data_path

def log(msg, *args): 
    def init():
        logger = logging.getLogger('wet')
        handler = logging.FileHandler(get_data_path('log'))
        formatter = logging.Formatter('[%(asctime)s]%(message)s', '%Y-%m-%d %H:%M:%S')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
        log.logger = logger
    logger = getattr(log, 'logger', init())
    logger.debug(msg, *args)

