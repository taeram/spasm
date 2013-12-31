from app import app
from flask import request

def is_authenticated():
    if 'Authorization' not in request.headers:
        return False

    return app.config['API_KEY'] == request.headers['Authorization'].strip()
