#!/usr/bin/env python3

from cupsAccounting.database.responsable import Responsable
from cupsAccounting.database.usuario import Usuario
from cupsAccounting.database.impresion import Impresion
from cupsAccounting.database.impresora import Impresora

from flask import Flask, request, render_template
from flask_bootstrap import Bootstrap
from flask_navigation import Navigation

from functools import partial

from os.path import dirname

# https://stackoverflow.com/questions/25925217/object-oriented-python-with-flask-server
registered_routes = {}


def register_route(route=None):
    # simple decorator for class based views
    def inner(fn):
        registered_routes[route] = fn
        return fn
    return inner


class Webserver(Flask):

    def __init__(self, *args, **kwargs):
        if not args:
            kwargs.setdefault('import_name', __name__)

        Flask.__init__(self,
                       template_folder= "%s/templates" % dirname(__file__),
                       *args,
                       **kwargs)
        self.bs = Bootstrap(self)

        self.nav = Navigation()
        self.nav.init_app(self)

        self.nav.Bar('top', [
            self.nav.Item('Home', 'index'),
            self.nav.Item('Responsables', 'responsables'),
            self.nav.Item('Usuarios', 'usuarios'),
            self.nav.Item('Impresoras', 'impresoras'),
            self.nav.Item('Impresiones', 'impresiones'),
        ])

        # register the routes from the decorator
        for route, fn in registered_routes.items():
            partial_fn = partial(fn, self)
            partial_fn.__name__ = fn.__name__
            self.route(route)(partial_fn)

    def setDatabase(self, db):
        self.db = db

    @register_route("/")
    def index(self):
        return render_template(
            "base.html",
        )

    @register_route("/responsables")
    def responsables(self):
        return "r"

    @register_route("/usuarios")
    def usuarios(self):
        usuarios = self.db.session.query(Usuario).all()
        return render_template(
            "usuarios.html",
            usuarios=usuarios
        )

    @register_route("/impresoras")
    def impresoras(self):
        impresoras = self.db.session.query(Impresora).all()
        return render_template(
            "impresoras.html",
            impresoras=impresoras
        )

    @register_route("/impresiones")
    def impresiones(self):
        impresiones = self.db.session.query(Impresion).all()
        return render_template(
            "impresiones.html",
            impresiones=impresiones
        )
