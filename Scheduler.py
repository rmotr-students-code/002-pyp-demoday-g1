#from apscheduler.scheduler import Scheduler
from SteamScout import app, db, Games
import requests as r
import json

#def refresh_games_table(app):

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

if __name__ == '__main__':           
    reset_game_db() 