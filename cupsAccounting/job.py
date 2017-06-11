#!/usr/bin/env python

from cupsAccounting.utils import objetoBase, validarUsuario


class Job(objetoBase):
    def __init__(self, c, jid):
        self.jid = jid
        self.c = c  # referencia al servidor

        self.usuario = self.attr['job-originating-user-name'].lower()
        self.nombre = self.attr['job-name'].lower()

        if 'smbprn' in self.nombre:
            self.nombre = self.nombre.split(' ', 1)[1]

    @property
    def attr(self):
        return self.c.getJobAttributes(self.jid)

    def validar(self):
        if not validarUsuario(self.usuario):
            return False
        return True

    def mover(self, queue):
        self.logger.debug(
            '%d: Moviendo a [%s]' % (self.jid, queue.name))
        self.c.moveJob(job_id=self.jid,
                       job_printer_uri=queue.uri)

    def __repr__(self):
        return """{clase} {jid}: {user} "{nombre}" """.format(
            clase=self.__class__.__name__,
            jid=self.jid,
            user=self.usuario,
            nombre=self.nombre)
