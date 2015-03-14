from flask import (
    Flask, request, render_template, redirect, 
    session, json, g, flash
    )
from flask.ext.sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask.ext.login import LoginManager
import requests

app = Flask(__name__)
app.config.from_object('config')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/steamscout.db'
db = SQLAlchemy(app)
Bootstrap(app)

################################### MODELS #####################################
#A model which will store the users steam ID for Sign in
class User(db.Model):
    __tablename__= 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))

    def __init__(self,name, email, password):
        self.name = name
        self.email = email
        self.password = password
        
    def __repr__(self):
        return '<name: {}>'.format(self.name)

class Preferences(db.Model):
    __tablename__= 'preferences'
    preference_id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey('user.user_id'))
    game_id=db.Column(db.Integer)
    threshold_amount=db.Column(db.Float)
    threshold_percent=db.Column(db.Float)
    
    def __init__(self, user_id, game_id, threshold_amount, threshold_percent):
        self.user_id = user_id
        self.game_id = game_id
        self.threshhold_amountt = threshold_amount
        self.threshold_percent = threshold_percent

class Games(db.Model):
    __tablename__='games'
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, unique=True)
    game_name = db.Column(db.String, unique=True)
    
    def __init__(self, game_id, game_name):
        self.game_id = game_id
        self.game_name = game_name

################################# VIEWS ########################################

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/games')
def games():
    # page that shows all the games.
    games_request = requests.get('http://api.steampowered.com/ISteamApps/GetAppList/v0001')
    all_games = [game for game in (games_request.json()["applist"]["apps"]["app"])]
    return render_template('games.html', all_games=all_games)

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
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     pass

# @app.before_request
# def before_request():
#     g.user = None
#     if 'user_id' in session:
#         g.user = User.query.get(session['user_id'])

# @app.route('/logout')
# def logout():
#     session.pop('user_id', None)
#     return redirect(oid.get_next_url())

# @app.route('/signup', methods=['GET', 'POST'])
# def signup():
#     return render_template('signup.html')        

    
    


if __name__ == "__main__":
    # create_app().run(host='0.0.0.0', port=8080, debug=True) # We have to remember to change debug = True back to False if we deply to heruku    
    app.run(host='0.0.0.0', port=8080, debug=True)
    # site url: https://002-pyp-demoday-g1-chanchar.c9.io
    db.create_all()