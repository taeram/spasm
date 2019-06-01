from os import getenv, \
               path

class Config(object):
    API_KEY = getenv('API_KEY')
    DEBUG = getenv('DEBUG', False)
    MAILGUN_API_KEY = getenv('MAILGUN_API_KEY')
    MAILGUN_API_URL = "https://api.mailgun.net/v2"
    SQLALCHEMY_DATABASE_URI = getenv('DATABASE_URL', 'sqlite:///' + path.dirname(__file__) + '/app/app.db').replace('mysql2:', 'mysql:')
    SQLALCHEMY_ECHO = getenv('SQLALCHEMY_ECHO', False)
    SQLALCHEMY_POOL_RECYCLE = 60
    TESTING = False
