#!/usr/bin/env python3

from sqlalchemy import Column
from sqlalchemy import Integer, String
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import relationship

from cupsAccounting.database import Base
from cupsAccounting.database.usuario import Usuario
from cupsAccounting.database.impresion import Impresion


class Responsable(Base):
    __tablename__ = 'responsable'
    __table_args__ = (UniqueConstraint('name'),)

    uid = Column(Integer, primary_key=True)
    name = Column(String)

    # usuarios = relationship("Usuario", back_populates='responsable')
    impresiones = relationship("Impresion", back_populates='responsable')

    def __repr__(self):
        return "Responsable (%d): %s" % (self.uid or -1, self.name)
