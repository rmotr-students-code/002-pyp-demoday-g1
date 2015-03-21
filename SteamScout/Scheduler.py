#from apscheduler.scheduler import Scheduler
from app import app, db, Games
import requests as r
import json

#def refresh_games_table(app):

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
    
game_db_reset()    