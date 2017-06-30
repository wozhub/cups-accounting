#!/usr/bin/env python

from cupsAccounting.queue import Queue
from cupsAccounting.logger import Logger
from cupsAccounting.utils import objetoBase, enviarMail

from cupsAccounting.database import Database

from cups import Connection
from time import sleep


class Manager(objetoBase, Logger):

    def __init__(self, config, printer):
        self.config = config
        self.c = Connection()
        self.p = printer
        self.m = config.config.mail
        self.db = Database(config.config.db['db_url'])
        self._initQueues()

    def _initQueues(self):
        self.q = {}

        self.q['entrada'] = Queue(self.c, '%s-entrada' % self.p.nombre)
        self.q['espera'] = Queue(self.c, '%s-espera' % self.p.nombre)
        self.q['salida'] = Queue(self.c, '%s-salida' % self.p.nombre)

    def procesarEntrada(self):
        self.logger.debug('Procesando %s' % self.q['entrada'].name)
        for j in self.q['entrada'].jobs:
            if j.validar():
                j.mover(self.q['espera'])
                subject = "Impresion Recibida: %s" % j.nombre
                enviarMail(j.usuario+'@agro.uba.ar', subject, self.config)
            else:
                j.cancelar()
                subject = "Impresion Cancelada: %s" % j.nombre
                for admin in self.m['admins']:
                    enviarMail(admin, subject, self.config)

    def procesarSalida(self):
        self.logger.debug('Procesando %s' % self.q['espera'].name)
        for j in self.q['espera'].jobs:

            if not self.q['salida'].empty:
                self.logger.info('Se está imprimiendo algo')
                break

            if not self.p.idle:
                self.logger.info('La impresora no esta lista')
                break

            antes = self.p.contador
            j.mover(self.q['salida'])
            subject = "Impresion Iniciando: %s" % j.nombre
            enviarMail(j.usuario+'@agro.uba.ar', subject, self.config)

            sleep(1)  # Hago una pausa para permitir que arranque la impresora
            while not self.p.idle:
                sleep(1)  # Espero a que termine

            j.paginas = self.p.contador - antes
            self.logger.warn('%d' % j.paginas)

            subject = "Impresion Finalizada: %s" % j.nombre
            enviarMail(j.usuario+'@agro.uba.ar', subject, self.config)
            self.db.job2db(j)

            if not self.q['salida'].empty:
                self.logger.info('Paso algo raro')
                break

    def status(self):
        q_brief = ""
        for key in self.q.keys():
            q_brief += "\t%s\n" % self.q[key].status()

        return """{clase} {name}:\n{q_brief}""".format(
            clase=self.__class__.__name__, name=self.p.nombre, q_brief=q_brief)
