#!/usr/bin/env python3

from cupsAccounting.database.impresion import Impresion

from flask import Flask, request, render_template
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
                       template_folder=dirname(__file__),
                       *args,
                       **kwargs)
        # register the routes from the decorator
        for route, fn in registered_routes.items():
            partial_fn = partial(fn, self)
            partial_fn.__name__ = fn.__name__
            self.route(route)(partial_fn)

    def setDatabase(self, db):
        self.db = db

    @register_route("/")
    def index(self):
        impresiones = self.db.session.query(Impresion).all()
        return render_template("index.jinja",
                               impresiones=impresiones
                               )
