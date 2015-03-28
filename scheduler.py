#from apscheduler.scheduler import Scheduler
from SteamScout import app, db, Games
import requests as r
import json
from celery import Celery
from datetime import timedelta
from celery.schedules import crontab

#note the is some stuff in the config file    
job = Celery('scheduler')

#test script, when we get celery to work, we would add the decorator to the func we want to run
@job.task
def test():
    result = "WORKING"
    test = open("test.txt", 'w')  
    test.write(result)
    test.close()



if __name__ == '__main__':    
    job.worker_mail()