#!/usr/env/python

from cupsAccounting.printers.printer import Printer


def loadPrinter(config):
    try:
        m = __import__('cupsAccounting.printers.%s' % config['marca'],
                       fromlist=[config['modelo'], ])
        p = getattr(m, config['modelo'])(config)
        return p
    except Exception as e:
        print(config)
        print(e)
        p = Printer()
        return p
