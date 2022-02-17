import os
from dogpile.cache import make_region

basedir = os.path.abspath(os.path.dirname(__file__))

region = make_region().configure(
    'dogpile.cache.memcached',
    expiration_time=3600,
    arguments={
        'url': ["127.0.0.1"],
    }
)


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'xk9OdAYTMeSYwgLd7U6Jln35FzVj9ONE'
    SQLALCHEMY_DATABASE_URI = 'postgresql:///projector_db'


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
