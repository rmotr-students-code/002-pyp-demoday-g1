import requests as r
import json

#http://api.steampowered.com/ISteamApps/GetAppList/v0001

def get_game_id(game_title):
	games = r.get('http://api.steampowered.com/ISteamApps/GetAppList/v0001')
	for game in games.json()['applist']['apps']['app']:
		if game_title in game['name']:
			game_id = game['appid']
			break
	return game_id

def get_price_info(game_id):
	game_page = r.get('http://store.steampowered.com/api/appdetails?appids={}'.format(game_id))
	formatted = game_page.json()
	price_info = {}
	price_info['current_price']=formatted[str(game_id)]['data']['price_overview']['final']
	price_info['inital_price']=formatted[str(game_id)]['data']['price_overview']['initial']
	price_info['discount_percent']=formatted[str(game_id)]['data']['price_overview']['discount_percent']
	return price_info

