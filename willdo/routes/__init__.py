from .mainpage import bp as mainpage_bp
from .tasklist import bp as tasklist_bp
from flask import Flask


def init_app(app: Flask):
    app.register_blueprint(mainpage_bp, url_prefix='/')
    app.register_blueprint(tasklist_bp, url_prefix='/within')
