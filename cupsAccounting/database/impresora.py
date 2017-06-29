#!/usr/bin/env python3

from sqlalchemy import Column
from sqlalchemy import Integer, String
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import relationship

from cupsAccounting.database import Base
from cupsAccounting.database.impresion import Impresion


class Impresora(Base):
    __tablename__ = 'impresora'
    __table_args__ = (UniqueConstraint('name'),)

    impresora_id = Column(Integer, primary_key=True)
    name = Column(String)

    impresiones = relationship("Impresion", back_populates='impresora')

    def __repr__(self):
        return "Impresora (%d): %s" % (self.uid or -1, self.name)
