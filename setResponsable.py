#!/usr/bin/env python

from config import conf_db
from cupsAccounting.database import Database

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter


def main():
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("--usuario", required=True,
                        help='Nombre del usuario.')
    parser.add_argument("--responsable", required=True,
                        help='Nombre de su responsable.')
    args = parser.parse_args()

    db = Database(conf_db['db_url'])
    db.setUsuarioResponsable(args.usuario, args.responsable)


if __name__ == '__main__':
    main()
