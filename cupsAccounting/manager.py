#!/usr/bin/env python

from cups import Connection

from cupsAccounting.queue import Queue
from cupsAccounting.logger import Logger


class Manager(objetoBase, Logger):

    def __init__(self, name, printer):
        self.name = name
        self.c = Connection()
        self.p = printer
        self._initQueues()

    def _initQueues(self):
        self.q = {}

        self.q['entrada'] = Queue(self.c, '%s-entrada' % self.name)
        self.q['espera'] = Queue(self.c, '%s-espera' % self.name)
        self.q['salida'] = Queue(self.c, '%s-salida' % self.name)

    def procesar(self):
        self.logger.info('Procesando %s' % self.q['entrada'].name)
        for j in self.q['entrada'].jobs:
            j.mover(self.q['espera'])

        self.logger.info('Procesando %s' % self.q['espera'].name)
        for j in self.q['espera'].jobs:

            if not self.q['salida'].empty:
                self.logger.info('Se está imprimiendo algo')
                break

            if not self.p.idle:
                self.logger.info('La impresora no esta lista')
                break

            j.mover(self.q['salida'])
            break

    def status(self):
        q_brief = ""
        for key in self.q.keys():
            q_brief += "\t%s\n" % self.q[key].status()

        return """{clase} {name}:\n{q_brief}""".format(
            clase=self.__class__.__name__, name=self.name, q_brief=q_brief)
