#!/usr/bin/env python

from cupsAccounting.utils import objetoBase
from cupsAccounting.logger import Logger

from random import randint


class Printer(objetoBase, Logger):
    marca = 'generica'

    def __init__(self, nombre='default'):
        self.nombre = nombre
        self._contador = 0

    @property
    def contador(self):
        self._contador += randint(1, 20)
        self.logger.info("El contador está en: %d" % self._contador)
        return self._contador

    @property
    def idle(self):
        return True

    def __repr__(self):
        return "%s.%s" % (self.marca, self.nombre)
