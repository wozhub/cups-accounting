#!/usr/bin/env python

import cupsAccounting.logger
from cupsAccounting.manager import Manager

from config import p, p_name


def main():
    m = Manager(p_name, p)
    print(m.status())
    m.procesar()
    print(m.status())


if __name__ == '__main__':
    main()
