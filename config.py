# This file will normally not be shown for any public use buut serves as an example. 
from datetime import timedelta
from celery.schedules import crontab
import os
_basedir = os.path.abspath(os.path.dirname(__file__))

## CELERY CONFIG ##
#REDIS
BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_TASK_SERIALIZER = 'json'
CELERYBEAT_SCHEDULE = {
	'reset_game_database': {
		'task':'scheduler.reset_game_db',
		'schedule': crontab(minute=0, hour=2), #resets db every day at 2:00 AM
		'args': ()
	},
	'send_game_alerts': {
		'task':'scheduler.send_game_alerts',
		'schedule': crontab(minute=0, hour=12), #sends alerts every day at noon
		'args': ()
	}
}

### WTF configuration ###
WTF_CSRF_ENABLED = True   #activates CSRF prevention
                          # http://en.wikipedia.org/wiki/Cross-site_request_forgery     

SECRET_KEY = 'change_this_later'
SECURITY_SALT = 'change_this_later_also'

### SQLAlchemy configuration ###
#local-repo dev setting:
SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/steamscout'
# Production setting
# SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

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
