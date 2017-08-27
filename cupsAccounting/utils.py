#!/usr/bin/env python

from pwd import getpwnam

from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.encoders import encode_base64
from os.path import basename

u_black = ['Administrador', 'administrador', 'root', 'admin']
u_white = ['marie']


class objetoBase(object):
    pass


def validarUsuario(user):
    """Verifica que el usuario exista en LDAP"""
    if user in u_black:
        return 1
    if user in u_white:
        return 0

    try:
        getpwnam(user)
        return 0
    except:
        return 2

    return -1


def enviarCorreo(correo):

    msg = MIMEMultipart()
    msg['From'] = correo['usuario']
    msg['To'] = correo['to']
    msg['Subject'] = correo['subject']
    msg.attach(MIMEText(correo['contenido'], 'html'))

    if "attachment" in correo:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(open(correo['attachment'], 'rb').read())
        encode_base64(part)
        part.add_header('Content-Disposition',
                        'attachment; filename="%s"' %
                        basename(correo['attachment']))
        msg.attach(part)

    mailServer = SMTP(correo['config']['smtp_serv'],
                      correo['config']['smtp_port'])
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(correo['config']['smtp_user'],
                     correo['config']['smtp_pass'])
    mailServer.sendmail(
        correo['usuario'],
        "%s@%s" % (correo['usuario'], correo['dominio']),
        msg.as_string())
    mailServer.close()
