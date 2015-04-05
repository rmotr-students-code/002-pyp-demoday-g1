import requests as r
import json
from SteamScout import app, mail, db
from SteamScout.models import Preferences, User
from flask.ext.mail import Message
from itsdangerous import URLSafeTimedSerializer
from flask import render_template, url_for
from jinja2 import Environment, PackageLoader

# Email Game Alerts
def send_game_alert(user_id):
    """Checks to see if any of the user's preferences have met the set threshold
    prices and sends an email with the complete list of those preferences."""
    user_preferences = Preferences.query.filter_by(user_id=user_id)
    user_email = User.query.filter_by(id=user_id).first().email

    if user_preferences.first():
        game_alerts = []
        for preference in user_preferences:
            current_game_info = get_price_info(preference.game_id)
            if preference.threshold_amount >= current_game_info["current_price"]/100.0:
                game_alerts.append([preference.game_name, "${:.2f}".format(preference.threshold_amount)])
        if game_alerts:
            with app.app_context():
            # find_template = Environment(loader=PackageLoader("SteamScout", "templates/email"))
            # template = find_template.get_template("scout_alert.html")
            # preferences_url = url_for('settings', _external=True)
            # html = template.render(game_alerts=game_alerts)
                html = render_template("email/scout_alert.html", game_alerts=game_alerts)
                subject = "Scout Report"
                send_mail(user_email, subject, html)

# User Validations and Token Generation
def generate_email_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    token = serializer.dumps(email, salt=app.config['SECURITY_SALT'])
    return token

def confirm_email_token(token, expiration=86400):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt=app.config['SECURITY_SALT'], max_age=expiration)
    except: # should be watching for specifically BadTimeSignature and SignatureExpired
        # add a separate template for failed or expired confirmations
        return False
    return email

# Email and Messaging
def send_mail(to, subject, template, sender=app.config['DEFAULT_MAIL_SENDER']):
    new_email = Message(
        subject, recipients=[to], html=template,
        sender=sender)
    mail.send(new_email)

def percent_to_price(percent, initial_price):
    """Convert percent preference to discounted amount for db storage"""
    decimal_percent = percent / 100.0
    amount = initial_price - (initial_price*decimal_percent)
    return round(amount, 2)

def format_price(price):
    """Formats price by inserting a decimal point in the appropriate place."""
    return "${:.2f}".format(float(price)/100.0)

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
    game_json = game_page.json()
    if game_json[str(game_id)]['data']['is_free']:
        free_game = dict(
            current_price=0,
            initial_price=0,
            discount_percent=0,
            header_image=game_json[str(game_id)]['data']['header_image'])
        return free_game
    else:
        try:
            price_info = dict(
                current_price=game_json[str(game_id)]['data']['price_overview']['final'],
                initial_price=game_json[str(game_id)]['data']['price_overview']['initial'],
                discount_percent=game_json[str(game_id)]['data']['price_overview']['discount_percent'],
                header_image=game_json[str(game_id)]['data']['header_image'])
            return price_info
        except KeyError:
            return None
