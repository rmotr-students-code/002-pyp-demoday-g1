import requests as r
import json

def percent_to_price(percent, initial_price):
    """Convert percent preference to discounted amount for db storage"""
    decimal_percent = percent / 100.0
    amount = initial_price - (initial_price*decimal_percent)
    return round(amount,2)

def format_price(price):
    """Formats price by inserting a decimal point in the appropriate place."""
    # listify = list(str(price))
    # if price < 100: #.99 cents represented as 99
    #     listify.insert(0, '.')
    #     return float("".join(listify))
    # else:
    #     listify.insert(-2,'.')
    #     return float("".join(listify))
    
    return "${:.2f}".format(float(price)/100.0) 
    # For examaple 99 returns as $0.99 and
    # 199 returns as $1.99.
    # May take off "$" since currency type changes
    
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