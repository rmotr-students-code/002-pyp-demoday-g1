#from apscheduler.scheduler import Scheduler
from SteamScout import app, db, Games
import requests as r
import json
from celery import Celery
from datetime import timedelta
from celery.schedules import crontab
import os
_basedir = os.path.abspath(os.path.dirname(__file__))

job = Celery(broker = 'sqla+sqlite:///' + os.path.join(_basedir, 'steamscout.sqlite'),
    backend = 'sqla+sqlite:///' + os.path.join(_basedir, 'steamscout.sqlite')
    )

#test script, when we get celery to work, we would add the decorator to the func we want to run
@job.task
def test():
    result = "WORKING"
    test = open("test.txt", 'w')  
    test.write(result)
    test.close()
