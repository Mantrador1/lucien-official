# -*- coding: utf-8 -*-
from flask import Blueprint

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return 'Hello from Fly.io - Flask + Gunicorn is working!'





