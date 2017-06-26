#!/usr/bin/env python

from config import p, p_name, conf_mail, conf_db

from cupsAccounting.manager import Manager

from os import system
from time import sleep


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


if __name__ == '__main__':
    main()
