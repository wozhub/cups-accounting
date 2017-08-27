#!/usr/bin/env python

from cupsAccounting.printers.printer import Printer


from easysnmp import Session


class LanierMp3352(Printer):
    marca = 'lanier'

    def __init__(self, c):  # Se inicializa con un Config
        self.logger.debug("Inicializando Impresora: ", c.config.nombre)

        self.nombre = c.config.nombre
        self.ip = c.config.ip
        self.oid_estado = "iso.3.6.1.2.1.43.17.6.1.2.1.3"
        self.oid_contador = "iso.3.6.1.2.1.43.10.2.1.4.1.1"

        # Alerta cuando mandaron a imprimir en otro formato.
        # No se si en ese momento puedo cancelar el trabajo
        self.oid_alerta_papel = "iso.3.6.1.2.1.43.18.1.1.8.1.27"

        # Alerta cuando se queda sin papel
        self.oid_bandejas = [
            "iso.36.1.2.1.43.18.1.1.8.1.22",   # tray 1
            "iso.36.1.2.1.43.18.1.1.8.1.23",   # tray 2
            "iso.36.1.2.1.43.18.1.1.8.1.24",   # tray 3
            "iso.36.1.2.1.43.18.1.1.8.1.31"    # tray 4
        ]
        # oid_contador = 'iso.3.6.1.2.1.43.10.2.1.5.1.1'

    def _getSnmpValue(self, oid):
        session = Session(hostname=self.ip, community='public', version=2)
        value = session.get(oid).value
        self.logger.debug("%s: %s" % (oid, value))
        return value

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
        self._contador = int(self._getSnmpValue(self.oid_contador))
        self.logger.info("El contador está en: ", self._contador)
        return self._contador
