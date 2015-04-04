import requests as r
import json
from SteamScout import app, mail, db
from SteamScout.models import Preferences, User, Games
from SteamScout.helpers import get_price_info, send_mail
from flask.ext.mail import Message
from itsdangerous import URLSafeTimedSerializer
from flask import render_template, url_for
from jinja2 import Environment, PackageLoader
from celery import Celery
from datetime import timedelta
from celery.schedules import crontab
import os

#Instantiate celery object
celery = Celery('tasks') # broker=app.config['CELERY_BROKER_URL'])
celery.config_from_object('config')
celery.conf.update(app.config)

#Runs every 24 hours
@celery.task
def reset_game_db(): 
    game_list = r.get('http://api.steampowered.com/ISteamApps/GetAppList/v0001')
    for game in game_list.json()['applist']['apps']['app']:
        try:
            if (int(game['appid']) % 10 == 0) and not Games.query.filter_by(game_name=game['name']).first():
                try:
                    new_game = Games(game['appid'],game['name'])
                    db.session.add(new_game)
                except:
                    pass
        except UnicodeEncodeError:
            pass
    db.session.commit()

#executes every 12 hours
@celery.task
def send_game_alerts():
    user_preferences = Preferences.query.all()
    user_email = User.query.filter
    
    for user in User.query.all():
        user_id = user.id
        user_email = user.email
        user_validated = user.validated
        user_preferences = Preferences.query.filter_by(user_id=user_id)

        if user_preferences.first() and user_validated:
            game_alerts = []
            for preference in user_preferences:
                current_game_info = get_price_info(preference.game_id)
                if preference.threshold_amount >= current_game_info["current_price"]/100.0:
                    game_alerts.append([preference.game_name, "${:.2f}".format(preference.threshold_amount)])
            if game_alerts:
                with app.app_context():
                    html = render_template("email/scout_alert.html", game_alerts=game_alerts)
                    subject = "Scout Report"
                    send_mail(user_email, subject, html)



	
