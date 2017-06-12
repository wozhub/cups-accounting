#!/usr/bin/env python

from cupsAccounting.logger import Logger

from pwd import getpwnam

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

    return False


