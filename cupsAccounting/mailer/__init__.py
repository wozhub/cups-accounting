#!/usr/bin/env python

from cupsAccounting.utils import objetoBase
from cupsAccounting.logger import Logger

# from threading import Thread
# from multiprocessing import Queue
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.encoders import encode_base64
from os.path import basename


class Mailer(objetoBase, Logger):

    def __init__(self, config):
        self.logger.debug('Iniciando Mailer con configuración: %s' % config)
        self.config = config

    def _enviarCorreo(self, correo):
        self.logger.debug('Enviando Correo: %s' % correo['subject'])

        msg = MIMEMultipart()
        msg['From'] = correo['usuario']
        msg['To'] = correo['to']
        msg['Subject'] = correo['subject']

        if "contenido" in correo:
            msg.attach(MIMEText(correo['contenido'], 'html'))

        if "attachment" in correo:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(open(correo['attachment'], 'rb').read())
            encode_base64(part)
            part.add_header('Content-Disposition',
                            'attachment; filename="%s"' %
                            basename(correo['attachment']))
            msg.attach(part)

        try:
            mailServer = SMTP(self.config['smtp_serv'],
                              self.config['smtp_port'])
            mailServer.ehlo()
            mailServer.starttls()
            mailServer.ehlo()
            mailServer.login(self.config['smtp_user'],
                             self.config['smtp_pass'])
            mailServer.sendmail(
                correo['usuario'],
                "%s@%s" % (correo['usuario'], correo['dominio']),
                msg.as_string())
            mailServer.close()
        except Exception as err:
            self.logger.error("No pude enviar el mail: %s" % err)

    def notificar(self, j, tipo):

        # algunos usuarios no reciben notificaciones porque no tienen mail
        if j.usuario in self.config['excluidos']:
            return

        correo = {}  # Voy a armar un dict para pasarselo al worker

        if j.usuario in self.config['aliases']:
            correo['to'] = self.config['aliases'][j.usuario]
        elif "@" in j.usuario:
            correo['to'] = j.usuario.split('@')  # Aca deberia ir el nombre
            correo['usuario'], correo['dominio'] = j.usuario.split('@')
        else:
            correo['usuario'] = j.usuario
            correo['dominio'] = self.config['dominio']
            correo['to'] = "%s@%s" % (j.usuario, self.config['dominio'])

        if tipo == "received":  # Determino el subject
            correo['subject'] = "Impresion Recibida: %s" % j.nombre
        elif tipo == "cancelled":
            correo['subject'] = "Impresion Cancelada: %s" % j.nombre
        elif tipo == "started":
            correo['subject'] = "Impresion Iniciando: %s" % j.nombre
        elif tipo == "ended":
            correo['subject'] = "Impresion Finalizada: %s" % j.nombre

        # if j.paginas != -1:
        #    correo['contenido'] = j.paginas
        # else:
        # correo['contenido'] = j.mail_repr()
        # correo['contenido'] = mail['subject']

        self._enviarCorreo(correo)

    # for admin in self.m['admins']:
        # enviarMail(admin, subject, self.config)
