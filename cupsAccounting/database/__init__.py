#!/usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy import desc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from cupsAccounting.database.responsable import Responsable
from cupsAccounting.database.usuario import Usuario
from cupsAccounting.database.impresion import Impresion
from cupsAccounting.database.impresora import Impresora

from cupsAccounting.utils import objetoBase
from cupsAccounting.logger import Logger


class Database(objetoBase, Logger):
    _session = None
    base = Base

    def __init__(self, config):
        self.logger.info("Creando %s" % (config['db_url']))
        self.engine = create_engine(config['db_url'])
        self.base.metadata.create_all(self.engine)

    @property
    def session(self):
        if self._session is None:
            builder = sessionmaker()
            builder.configure(bind=self.engine)
            self._session = builder()

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

    def getImpresora(self, i_name):
        i = self.session.query(Impresora).filter_by(name=i_name).first()
        if i:
            return i
        else:
            i = Impresora(name=i_name)
            self.session.add(i)
            try:
                self.session.commit()
                return i
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
        impresora = self.getImpresora(job.impresora)
        i = Impresion()
        i.nombre = job.nombre
        i.usuario = usuario
        i.ip = job.ip
        i.paginas = job.paginas
        i.responsable = self.session.query(Responsable).\
            filter_by(uid=usuario.responsable_uid).first()
        i.impresora = impresora
        self.session.add(i)
        try:
            self.session.commit()
        except Exception as e:
            self.logger.error(e)
            self.session.rollback()

    def status(self):
        for i in self.session.query(Impresion)\
                .order_by(desc(Impresion.iid))\
                .limit(5).all():
            print(i)
