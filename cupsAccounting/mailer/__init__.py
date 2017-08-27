#!/usr/bin/env python

from cupsAccounting.utils import objetoBase, enviarCorreo
from cupsAccounting.logger import Logger

from threading import Thread
from multiprocessing import Queue


class Mailer(objetoBase, Logger):

    def __init__(self, config):
        self.logger.debug('Iniciando Mailer con configuración: %s' % config)
        self.config = config
        self.queue = Queue()
        self.thread = Thread(target=self._enviarMail)
        self.thread.start()

    def __del__(self):
        self.queue.join()

    def _enviarMail(self):
        while True:
            mail = self.queue.get()
            if mail:
                try:
                    self.logger.debug('Enviando Correo: %s' % mail['subject'])
                    enviarCorreo(mail)
                except:
                    self.logger.error('No pude enviar un correo')
                finally:
                    pass
                # self.queue.task_done()

    def notificar(self, j, tipo):
        if j.usuario in self.config['excluidos']:
            return

        mail = {}  # Voy a armar un dict para pasarselo al worker
        mail['config'] = self.config['smtp_config']

        if j.usuario in self.config['aliases']:
            mail['to'] = self.config['aliases'][j.usuario]
        elif "@" in j.usuario:
            mail['to'] = j.usuario.split('@')  # Aca deberia ir el nombre
            mail['usuario'], mail['dominio'] = j.usuario.split('@')
        else:
            mail['usuario'] = j.usuario
            mail['dominio'] = self.config['dominio']
            mail['to'] = "%s@%s" % (j.usuario, self.config['dominio'])

        if tipo == "received":  # Determino el subject
            mail['subject'] = "Impresion Recibida: %s" % j.nombre
        elif tipo == "cancelled":
            mail['subject'] = "Impresion Cancelada: %s" % j.nombre
        elif tipo == "started":
            mail['subject'] = "Impresion Iniciando: %s" % j.nombre
        elif tipo == "ended":
            mail['subject'] = "Impresion Finalizada: %s" % j.nombre

        if j.paginas != -1:
            mail['contenido'] = j.paginas
        else:
            mail['contenido'] = j.mail_repr()
        # mail['contenido'] = body.encode('ascii', 'ignore')
        self.queue.put(mail)

    # enviarMail(j.usuario, subject, self.config)
    # enviarMail(j.usuario+'@agro.uba.ar', subject, self.config)
    # enviarMail(j.usuario+'@agro.uba.ar', subject, self.config)
    # for admin in self.m['admins']:
        # enviarMail(admin, subject, self.config)
    # def enviarMail(to, subject, c, body=False, attachment=None):
    # http://stackoverflow.com/questions/7437455/python-smtplib-using-gmail-messages-with-a-body-longer-than-about-35-characters
    # algunos usuarios no reciben notificaciones porque no tienen mail
