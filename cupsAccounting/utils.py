#!/usr/bin/env python

from pwd import getpwnam


u_black = ['Administrador', 'administrador', 'root', 'admin']
u_white = ['marie']


class objetoBase(object):
    pass


def validarUsuario(user):
    """Verifica que el usuario exista en LDAP"""

    if user in u_black:
        logging.error('El usuario [%s] esta en la lista nok', user)
        return False

    if user in u_white:
        logging.debug('El usuario [%s] se verifico correctamente', user)
        return True

    try:
        if getpwnam(user):
            logging.debug('El usuario [%s] se verifico correctamente', user)
            return True
        else:
            logging.error('El usuario [%s] no pudo verificarse', user)
            return False
    except:
        logging.error('El usuario [%s] no pudo verificarse', user)
        return 0


