#!/usr/bin/env python

from os import system
from time import sleep

from cupsAccounting.printers import loadPrinter
from cupsAccounting.config import Config
from cupsAccounting.manager import Manager

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter


def main():
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("--manager", "-m",
                        default="config.manager.yaml",
                        help="Archivo de configuración general")
    parser.add_argument("--printer", "-p",
                        default="config.printer.yaml",
                        help="Archivo de configuración de la impresora")
    args = parser.parse_args()

    p = loadPrinter(Config(args.printer))
    m = Manager(Config(args.manager), p)

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
