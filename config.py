from os import getenv

class Config(object):
    DEBUG = False
    TESTING = False
    API_KEY = getenv('API_KEY')
    SQLALCHEMY_DATABASE_URI = getenv('DATABASE_URL')
    MAILGUN_API_URL = "https://api.mailgun.net/v2"
    MAILGUN_API_KEY = getenv('MAILGUN_API_KEY')

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'

class TestingConfig(Config):
    TESTING = True
