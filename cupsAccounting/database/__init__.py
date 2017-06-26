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

    def getUsuario(self, u_name):
        u = self.session.query(Usuario).filter_by(name=u_name).first()
        if u:
            return u
        else:
            u = Usuario(name=u_name)
            self.session.add(u)
            try:
                self.session.commit()
                return u
            except Exception as e:
                print(e)
                self.session.rollback()

    def getResponsable(self, r_name):
        r = self.session.query(Responsable).filter_by(name=r_name).first()
        if r:
            return r
        else:
            r = Responsable(name=r_name)
            self.session.add(r)
            try:
                self.session.commit()
                return r
            except Exception as e:
                print(e)
                self.session.rollback()

    def setUsuarioResponsable(self, u_name, r_name):
        usuario = self.getUsuario(u_name)
        responsable = self.getResponsable(r_name)
        usuario.responsable_uid = responsable.uid
        try:
            self.session.commit()
        except Exception as e:
            self.logger.error(e)
            self.session.rollback()

        # En caso de que haya impresiones suyas sin responsable
        for i in self.session.query(Impresion)\
                .filter_by(usuario=usuario)\
                .filter_by(responsable=None):
            i.responsable = responsable
        self.session.commit()

    def job2db(self, job):
        usuario = self.getUsuario(job.usuario)
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
