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
	try: 
		price_info = dict(
			current_price=formatted[str(game_id)]['data']['price_overview']['final'],
			initial_price=formatted[str(game_id)]['data']['price_overview']['initial'],
			discount_percent=formatted[str(game_id)]['data']['price_overview']['discount_percent'],
			header_image=formatted[str(game_id)]['data']['header_image'])
		return price_info
	except KeyError:
		return None	


