# 002-pyp-demoday-g1
Charlie's angels

## Purpose
Steam sales are a daily occurance but there are way too many games to keep track of. Use SteamScout to alert you
when a game that you're interested in drops down to the price you set. 

### Required

+ Paginate games library, currently causes significant lag.
+ set up user preferences
+ configure a way for steamscout to email users. - Flask-Mail
+ set up the gamesDB to automatically refresh every 24 hours. - Cron Job
+ set the price monitoring for users to refresh price data every x hours. 
+ Add percentage threshold option for preferences
+ Improve Settings page.
+ Improve Navbar in base (log out column adding problems)

### Optional

+ make the individual games look pretty - Improved it, but it could be better..
+ see if theres a way to include game cover art, trailers, etc in the individual game page - added cover image on top.
+ Change generic variables to be more specific. Ex. form should should be login_form
+ Add to the settings page when no preferences are set. 

### Completed:
- format price data. Currently "$4.99" displays as "499" - changed format_prices to make it easier
- Ideally, figure a way to only put games into the gamesDB. 
    - if not 2, protect the site from apps that dont have a price_info section.
- build way to search through games library - Basic Functionality
- Changes amount format, list view on settings 