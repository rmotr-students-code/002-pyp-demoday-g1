from SteamScout import app, db, Games
import requests as r
import json
from celery import Celery
from datetime import timedelta
from celery.schedules import crontab
import os

#local settings using redis
#app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
#app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

#Instantiate celery object
celery = Celery('tasks') # broker=app.config['CELERY_BROKER_URL'])
celery.config_from_object('config')
celery.conf.update(app.config)

@celery.task
def test_celery():
	print "this works"


	
