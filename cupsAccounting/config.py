#!/usr/bin/env python

from cupsAccounting.utils import objetoBase
from cupsAccounting.logger import Logger

from yaml import load


class Config(objetoBase, Logger):

    def __init__(self, config_file):
        self.config_file = config_file
        self._readConfig()
        self._parseDict()

    def _readConfig(self):
        with open(self.config_file, 'r') as stream:
            self.config_dict = load(stream)

    def _parseDict(self):
        self.config = AttributeDict(self.config_dict)


# https://stackoverflow.com/questions/4984647/accessing-dict-keys-like-an-attribute-in-python
class AttributeDict(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
