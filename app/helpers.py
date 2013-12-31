from app import app
from flask import request

def is_authenticated():
    return app.config['API_KEY'] == request.headers['Authorization'].strip()
