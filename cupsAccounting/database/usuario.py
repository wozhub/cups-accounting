#!/usr/bin/env python3

from sqlalchemy import Column
from sqlalchemy import Integer, String
from sqlalchemy import UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship

from cupsAccounting.database import Base
from cupsAccounting.database.impresion import Impresion


class Usuario(Base):
    __tablename__ = 'usuario'
    __table_args__ = (UniqueConstraint('name'),)

    uid = Column(Integer, primary_key=True)
    name = Column(String)

    responsable_uid = Column(Integer, ForeignKey('responsable.uid'))
    # responsable = relationship("Responsable", back_populates="usuarios")

    impresiones = relationship("Impresion", back_populates='usuario')

    def __repr__(self):
        return "Usuario:%d %s" % (self.uid or -1, self.name)
