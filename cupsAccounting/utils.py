#!/usr/bin/env python

from cupsAccounting.logger import Logger

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
    if user in u_black: return 1
    if user in u_white: return 0

    try:
        getpwnam(user)
        return 0
    except:
        return 2

    return -1


def enviarMail(to, subject, c, body=False, attachment=None):
    # http://stackoverflow.com/questions/7437455/python-smtplib-using-gmail-messages-with-a-body-longer-than-about-35-characters

    # algunos usuarios no reciben notificaciones porque no tienen mail
    usuario = to.lower().split('@')[0]
    if usuario in c.config.mail['excluidos']:
        return

    if usuario in c.config.mail['aliases']:
        to = c.config.mail['aliases'][usuario]

    contenido = subject
    if body is not False:
        contenido = body.encode('ascii', 'ignore')

    msg = MIMEMultipart()

    msg['From'] = usuario
    msg['To'] = to
    msg['Subject'] = subject
    msg.attach(MIMEText(contenido, 'html'))

    if attachment is not None:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(open(attachment, 'rb').read())
        encode_base64(part)
        part.add_header('Content-Disposition',
                        'attachment; filename="%s"' % basename(attachment))
        msg.attach(part)

    mailServer = SMTP("smtp.gmail.com", 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(c.config.mail['smtp_user'], c.config.mail['smtp_pass'])
    mailServer.sendmail(usuario, to, msg.as_string())
    mailServer.close()
