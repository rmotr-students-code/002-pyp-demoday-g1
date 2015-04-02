# This file will normally not be shown for any public use buut serves as an example. 
from datetime import timedelta
from celery.schedules import crontab
import os

_basedir = os.path.abspath(os.path.dirname(__file__))

### DB CONFIG ###
class Config(object):
    
    WTF_CSRF_ENABLED = True   #activates CSRF prevention # http://en.wikipedia.org/wiki/Cross-site_request_forgery
    SECRET_KEY = 'change_this_later'
    SECURITY_SALT = 'change_this_later_also'
    
    ### MAIL CONFIG ###
    #Send Mail From : steam.scout.15@gmail.com    PW: steamdeals 
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465 # 587 trying port 465
    MAIL_USE_TLS = False #The example from the guy who uses Gmail SMPT has this set to True This being true = port number 587
    MAIL_USE_SSL = True
    MAIL_DEBUG = False
    MAIL_USERNAME = "steam.scout.15@gmail.com"
    MAIL_PASSWORD = "steamdeals"
    DEFAULT_MAIL_SENDER = 'Admin <steam.scout.15@gmail.com>'
    
    ### CELERY CONFIG ###
    # BROKER_URL=os.environ['REPLACE_URL']
    # CELERY_RESULT_BACKEND=os.environ['REPLACE_URL']
    
    ### Other Config ###
    STEAM_API_KEY = "D7BC71E91BD7E9A204C48BD83EFD29BB"
    
    DEBUG = False
    TESTING = False
    PORT = 8080
    HOST = '0.0.0.0'

class ProductionConfig(Config):
    # SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    PORT = None
    HOST = None

class DevelopmentConfig(Config):
    DEBUG = True
    # Need to start the postgresql server for c9 using: "sudo service postgresql start"
    # Then need to connect to it using: sudo sudo -u postgres psql
    # Quit out of the postgres bash thing using "\q" and the service should still be running the background.
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:steamdeals@localhost/steamscout_db'
    

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, 'test_db.sqlite')
