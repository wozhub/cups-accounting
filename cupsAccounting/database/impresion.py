#!/usr/bin/env python3

from datetime import datetime
from sqlalchemy import Column
from sqlalchemy import Integer, String, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from cupsAccounting.database import Base


class Impresion(Base):
    __tablename__ = 'impresion'

    iid = Column(Integer, primary_key=True)
    nombre= Column(String)
    paginas = Column(Integer, nullable=False)
    fecha = Column(DateTime, default=datetime.now)
    ip = Column(String, nullable=False)

    usuario_uid = Column(Integer,
                         ForeignKey('usuario.uid'),
                         nullable=False)
    usuario = relationship("Usuario", back_populates="impresiones")

    responsable_uid = Column(Integer, ForeignKey('responsable.uid'))
    responsable = relationship("Responsable", back_populates="impresiones")

    impresora_id = Column(Integer, ForeignKey('impresora.impresora_id'))
    impresora = relationship("Impresora", back_populates="impresiones")

    def __repr__(self):
        #return "Impresion (%d): %s" % (self.iid or -1, self.name)
        return """<{clase} {jid}: {user}@{ip} "{nombre}" {impresora}@{fecha}>""".format(
            clase=self.__class__.__name__,
            jid=self.iid or -1, user=self.usuario, ip=self.ip,
            nombre=self.nombre, impresora=self.impresora, fecha=self.fecha)
