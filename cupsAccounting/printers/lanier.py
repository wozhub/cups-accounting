#!/usr/bin/env python

from cupsAccounting.printers.printer import Printer


from easysnmp import Session


class LanierMp3352(Printer):
    marca = 'lanier'

    def __init__(self, c):  # Se inicializa con un Config
        self.ip = c.config.ip
        self.oid_estado = "iso.3.6.1.2.1.43.17.6.1.2.1.3"
        self.oid_contador = 'iso.3.6.1.2.1.43.10.2.1.4.1.1'
        # oid_contador = 'iso.3.6.1.2.1.43.10.2.1.5.1.1'

    def _getSnmpValue(self, oid):
        session = Session(hostname=self.ip, community='public', version=2)
        return session.get(oid).value

    @property
    def estado(self):
        return self._getSnmpValue(self.oid_estado)

    @property
    def idle(self):
        if self.estado == '0':
            return True
        return False

    @property
    def printing(self):
        if self.estado == '500':
            return True
        return False

    @property
    def contador(self):
        return int(self._getSnmpValue(self.oid_contador))
