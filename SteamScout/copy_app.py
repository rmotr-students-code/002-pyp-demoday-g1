from flask import (
    Flask, request, render_template, redirect, 
    session, json, g, flash
    )
from flask.ext.sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask.ext.openid import OpenID
from flask.ext.login import LoginManager
import requests
import re


app = Flask(__name__)
app.config.from_object('config')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/steamscout.db'
Bootstrap(app)
db = SQLAlchemy(app)
oid = OpenID(app)

_steam_id_re = re.compile('steamcommunity.com/openid/id/(.*?)$')

# def get_steam_userinfo(steam_id):
#     options = {
#         'key': app.config['STEAM_API_KEY'],
#         'steamids': steam_id
#     }
#     url = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0001/?'
#     rv = (requests.get(url, params=options)).json()
#     return rv['response']['players']['player'][0] or {}

@app.before_request
def lookup_current_user():
    g.user = None
    if 'openid' in session:
        openid = session['openid']
        g.user = User.query.filter_by(openid=openid).first()

# Routes

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/games')
def games():
    # page that shows all the games.
    return render_template('games.html')

@app.route('/developers')
def show_developors():
    # page that shows all the games.
    return render_template('developers.html')

@app.route('/contact')
def contact():
    # page that shows all the games.
    return render_template('contact.html')

@app.route('/settings')
def settings():
    pass

# Log in / Log out
@app.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    if g.user is not None:
        return(oid.get_next_url())
    
    return oid.try_login('http://steamcommunity.com/openid')

@oid.after_login
def create_or_login(player):
    match = _steam_id_re.search(player.identity_url)
    g.user = User.get_or_create(match.group(1))
    steamdata = get_steam_userinfo(g.user.steam_id)
    g.user.nickname = steamdata['personaname']
    # db.session.commit() # uncomment once models are complete
    session['user_id'] = g.user.id
    flash("You have logged in as {}".format(g.user.nickname))
    return redirect(oid.get_next_url())

@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        g.user = User.query.get(session['user_id'])

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(oid.get_next_url())

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template('signup.html')        

    
    
################################### MODELS #####################################################    
#A model which will store the users steam ID for Sign in
class User(db.Model):
    __tablename__= 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    nickname = db.String(80)
    preferences = db.relationship('Preferences', backref='user_pref', lazy='dynamic')
    
    def __init__(self, steam_id, nickname):
        self.nickname = nickname
    
    def __repr__(self):
        return '<nickname: {}>'.format(self.nickname)
        
class Preferences(db.Model):
    __tablename__= 'preferences'
    perf_id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey('user.user_id'))
    game_id=db.Column(db.Integer)
    thresh_amt=db.Column(db.Float)
    thresh_pct=db.Column(db.Float)
    alert_type=db.Column(db.String(120))
    
    def __init__(self, user_id, game_id, thresh_amt, thresh_pct, alert_type):
        self.user_id = user_id
        self.game_id = game_id
        self.thresh_amt = thresh_amt
        self.thresh_pct = thresh_pct
        self.alert_type = alert_type
     
#Add user to db if he does not exist in db    
""""@staticmethod
    def get_or_create(steam_id):
        rv = User.query.filter_by(steam_id=steam_id).first() # not quite sure what the issue is here
        if rv is None:
            rv = User()
            rv.steam_id = steam_id
            db.session.add(rv)
        return rv
        """

if __name__ == "__main__":
    # create_app().run(host='0.0.0.0', port=8080, debug=True) # We have to remember to change debug = True back to False if we deply to heruku    
    app.run(host='0.0.0.0', port=8080, debug=True)
    # site url: https://002-pyp-demoday-g1-chanchar.c9.io
    db.create_all()