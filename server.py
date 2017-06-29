#!/usr/bin/env python

from os import system
from time import sleep

from cupsAccounting.printers import loadPrinter
from cupsAccounting.config import Config
from cupsAccounting.manager import Manager

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter


def main():
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("--nombre", default='test',
                        help='Nombre de la impresora a administrar en CUPS.')
    parser.add_argument("--marca", default='generica',
                        help='Nombre de la impresora a administrar en CUPS.')
    parser.add_argument("--modelo", default='generico',
                        help='Nombre de la impresora a administrar en CUPS.')
    parser.add_argument("--ip", default='127.0.0.1',
                        help='Nombre de la impresora a administrar en CUPS.')
    args = parser.parse_args()

    c = Config('config.yaml')  # Configuracion
    p = loadPrinter(args)
    m = Manager(c, p)

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
        sleep(1)


if __name__ == '__main__':
    main()
