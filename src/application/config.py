from application.util import generate

class Config(object):
    SECRET_KEY = generate(50)
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'user'
    MYSQL_PASSWORD = 'Gr33n73@mC4nG0D1e>:('
    MYSQL_DB = 'solezonsolis'

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True