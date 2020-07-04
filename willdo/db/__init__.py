from flask import Flask, g
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from .models import Base, AvailableTasklist, IndividualTask


def init_app(app):
    engine = make_db_engine(app)
    Session = make_session(engine)

    @app.before_request
    def get_db():
        # pylint: disable=unused-variable
        if 'db_session' not in g:
            g.db_session = Session()

    @app.before_first_request
    def init_db():
        # pylint: disable=unused-variable
        Base.metadata.create_all(engine)

    app.teardown_appcontext(teardown_db)


def teardown_db(exception=None):
    db_session = g.pop('db_session', None)

    if db_session is not None:
        db_session.close()

    if exception:
        raise exception


def make_db_engine(app):
    will_echo = False
    if app.config.get('DEBUG') or app.config.get('TESTING') or (app.env == 'development'):
        will_echo = True

    engine = create_engine(
        app.config['SQLALCHEMY_DATABASE_URI'], echo=will_echo)
    return engine


def make_session(engine):
    Session = scoped_session(sessionmaker(
        bind=engine, autocommit=False, autoflush=False))
    return Session
