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
        return self._contador
