#!/usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from cupsAccounting.database.responsable import Responsable
from cupsAccounting.database.usuario import Usuario
from cupsAccounting.database.impresion import Impresion

from cupsAccounting.utils import objetoBase
from cupsAccounting.logger import Logger


class Database(objetoBase, Logger):
    _session = None
    base = Base

    def __init__(self, engine_url):
        self.logger.info("Creando %s" % (engine_url))
        self.engine = create_engine(engine_url)

    @property
    def session(self):
        if self._session is None:
            builder = sessionmaker()
            builder.configure(bind=self.engine)
            self._session = builder()
            Base.metadata.create_all(self.engine)

        return self._session

    def getUser(self, name):
        u = self.session.query(Usuario).filter_by(name=name).first()
        if u:
            return u
        else:
            u = Usuario(name=name)
            self.session.add(u)
            try:
                self.session.commit()
                return u
            except Exception as e:
                print(e)
                self.session.rollback()

    def job2db(self, job):
        usuario = self.getUser(job.usuario)
        i = Impresion()
        i.name = job.nombre
        i.usuario = usuario
        i.ip = job.ip
        i.paginas = job.paginas
        i.responsable = self.session.query(Responsable).\
            filter_by(uid=usuario.responsable_uid).first()
        self.session.add(i)
        try:
            self.session.commit()
        except Exception as e:
            self.logger.error(e)
            self.session.rollback()
