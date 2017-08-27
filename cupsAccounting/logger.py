#!/usr/bin/env python

import logging

from logging import Formatter, FileHandler, StreamHandler

# https://stackoverflow.com/questions/15780151/how-to-use-python-logging-in-multiple-modules


class Logger(object):
    @property
    def logger(self):
        return logging.getLogger('cupsAccounting')


log_fmt = "%(asctime)s | %(levelname)s | %(module)s.%(funcName)s | %(message)s"

logging.basicConfig(
  level=logging.DEBUG,
  filename='/tmp/cups-accounting.log', filemode='a',
  format=log_fmt,
  datefmt="%Y-%m-%d %H:%M:%S")

formato = Formatter(log_fmt, "%Y-%m-%d %H:%M:%S")

#fh = FileHandler('/tmp/cups-accounting.log')
#fh.setLevel(logging.DEBUG)
#fh.setFormatter(formato)

ch = StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formato)

#logging.getLogger('cupsAccounting').addHandler(fh)
logging.getLogger('cupsAccounting').addHandler(ch)
