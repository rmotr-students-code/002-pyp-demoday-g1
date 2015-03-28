# Stand alone file to test aspects of the website.
#from apscheduler.scheduler import Scheduler
from SteamScout import app, db, models, Games, User, Preferences, helpers, views
from crontab import CronTab
import requests as r
import json
from SteamScout import mail
from flask.ext.mail import Message
import os




_basedir = os.path.abspath(os.path.dirname(__file__))
#Refresh the Games table (1 minute run time)
def reset_game_db():
    
    game_list = r.get('http://api.steampowered.com/ISteamApps/GetAppList/v0001')
    for game in game_list.json()['applist']['apps']['app']:
        if (int(game['appid']) % 10 == 0) and not Games.query.filter_by(game_name=game['name']).first():
            try:
                new_game = Games(game['appid'],game['name'])
                db.session.add(new_game)
            except:
                pass
    db.session.commit()

def reset_db():
    db.drop_all()
    db.create_all()





if __name__ == '__main__':       
    helpers.send_game_alert(1)
    #reset_db()
    #reset_game_db()


    
    



"""
def game_db_reset():
    
    game_list = r.get('http://api.steampowered.com/ISteamApps/GetAppList/v0001')
    for game in game_list.json()['applist']['apps']['app']:
        if int(game['appid']) % 10 == 0:
            game_info = (r.get('http://store.steampowered.com/api/appdetails?appids={}'.format(game['appid']))).json()
            try: 
                if game_info[str(game['appid'])]['data']['type'] == "game":
                    new_game = Games(game['appid'],game['name'])
                    db.session.add(new_game)
            except:
                pass
    db.session.commit()
"""    
    