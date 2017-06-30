#!/usr/env/python

# from cupsAccounting.config import Config
from cupsAccounting.printers.printer import Printer


def loadPrinter(c):
    try:
        m = __import__('cupsAccounting.printers.%s' % c.config.marca,
                       fromlist=[c.config.modelo, ])
        p = getattr(m, c.config.modelo)(c)
        return p
    except Exception as e:
        print(e)
        p = Printer()
        return p
