import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG=False
    TESTING=False
    CSRF_ENABLED = True
    SECRET_KEY = 'y1ou3-w4il5l6-7n8ever-gu9e0ss'

class ProductionConfig(Config):
    DEBUG=False

class DevelopmentConfig(Config):
    DEVELOPMENT=True
    DEBUG= True

OPENID_PROVIDERS = [
    {'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id'},
    {'name': 'Yahoo', 'url': 'https://me.yahoo.com'},
    {'name': 'AOL', 'url': 'http://openid.aol.com/<username>'},
    {'name': 'Flickr', 'url': 'http://www.flickr.com/<username>'},
    {'name': 'MyOpenID', 'url': 'https://www.myopenid.com'}]
