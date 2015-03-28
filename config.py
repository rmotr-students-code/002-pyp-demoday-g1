# This file will normally not be shown for any public use buut serves as an example. 
from datetime import timedelta
from celery.schedules import crontab

import os
_basedir = os.path.abspath(os.path.dirname(__file__))
### WTF configuration ###
WTF_CSRF_ENABLED = True   #activates CSRF prevention
                          # http://en.wikipedia.org/wiki/Cross-site_request_forgery     

SECRET_KEY = 'change_this_later'
SECURITY_SALT = 'change_this_later_also'

### APP CONFIG ###

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, 'steamscout.db')

### Other Config ###
STEAM_API_KEY = "D7BC71E91BD7E9A204C48BD83EFD29BB"

### Mail Config ###
# going to stick with defaults for now and use my email address as the sender and receiver 
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
CELERY_TIMEZONE = 'US/Eastern'

# my understanding is that when called upon the 'beat" will run scheduler.test (see scheduler.py)
# every minute. crontab() = " * * * * * "
CELERYBEAT_SCHEDULE = {
    'testing': {
        'task': 'scheduler.test',
        'schedule': crontab()
    },
}
#CELERY_BROKER_URL='sqla+sqlite:///' + os.path.join(_basedir, 'steamscout.db')
#CELERY_RESULT_BACKEND='sqla+sqlite:///' + os.path.join(_basedir, 'steamscout.db')