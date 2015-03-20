# 002-pyp-demoday-g1
Charlie's angels

## Purpose
Steam sales are a daily occurance but there are way too many games to keep track of. Use SteamScout to alert you
when a game that you're interested in drops down to the price you set. 

~~1) format price data. Currently "$4.99" displays as "499" - .format() or create a price_format() and place in between {{ }}~~
2) Ideally, figure a way to only put games into the gamesDB. 
3) if not 2, protect the site from apps that dont have a price_info section. -FINISHED
4) set up user preferences
5) build way to search through games library # Currently working on it - Charlie
6) configure a way for steamscout to email users. - Flask-Mail
7) set up the gamesDB to automatically refresh every 24 hours. - Cron Job
8) set the price monitoring for users to refresh price data every x hours. 

optional:

1)make the individual games look pretty
2) see if theres a way to include game cover art, trailers, etc in the individual game page
3) divide games library to only display 20 or so games at a time
4) Change generic variables to be more specific. Ex. form should should be login_form