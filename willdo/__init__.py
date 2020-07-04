from flask import Flask
from os import urandom
from .extensions import init_app as extensions_init_app
from .db import init_app as db_init_app
from .routes import init_app as routes_init_app


def create_secret_key():
    return urandom(16)


def create_app(config_object=None, config_mapping=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_pyfile('config.py', silent=True)
    if config_object:
        app.config.from_object(config_object)
    if config_mapping:
        app.config.from_mapping(config_mapping)

    if app.secret_key is None:
        app.secret_key = create_secret_key()

    extensions_init_app(app)
    db_init_app(app)
    routes_init_app(app)
    return app
