# -*- coding: utf-8 -*-
from flask import Flask
from app.routes.main import main_bp
from app.extensions import init_extensions

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")
    init_extensions(app)
    app.register_blueprint(main_bp)
    return app





