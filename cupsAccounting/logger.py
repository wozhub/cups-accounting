#!/usr/bin/env python

import logging

# https://stackoverflow.com/questions/15780151/how-to-use-python-logging-in-multiple-modules


class Logger(object):
    @property
    def logger(self):
        return logging.getLogger('cupsAccounting')


log_fmt = "%(asctime)s | %(levelname)s | %(module)s.%(funcName)s | %(message)s"

logging.basicConfig(
  level=logging.INFO,
  filename='/tmp/cups-accounting.log', filemode='w',
  format=log_fmt,
  datefmt="%Y-%m-%d %H:%M:%S")
