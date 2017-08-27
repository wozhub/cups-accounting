#!/usr/env/python

# from cupsAccounting.config import Config
from cupsAccounting.printers.printer import Printer


def loadPrinter(c):
    try:
        print("Buscando %s.%s" % (c.config.marca, c.config.modelo))
        m = __import__('cupsAccounting.printers.%s' % c.config.marca,
                       fromlist=[c.config.modelo, ])
        p = getattr(m, c.config.modelo)(c, nombre=c.config.nombre)
    except Exception as e:
        print(e)
        p = Printer(c.config.nombre)

    finally:
        print(p)
        return p
