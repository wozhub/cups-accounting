#!/usr/bin/env python

from os import system
from time import sleep


from config import p, p_name, conf_mail, conf_db
from cupsAccounting.manager import Manager


def main():
    m = Manager(p_name, p, conf_mail, conf_db)

    while True:
        system('clear')
        print(m.status())
        sleep(1)
        m.procesarEntrada()
        system('clear')
        print(m.status())
        sleep(1)
        m.procesarSalida()

        m.db.status()


if __name__ == '__main__':
    main()
