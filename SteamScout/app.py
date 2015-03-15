from flask import (
    Flask, request, render_template, redirect, 
    session, json, g, flash, url_for
    )
from flask.ext.sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask.ext.login import LoginManager
import requests

#### WTForms #####
from flask_wtf import Form
from wtforms import TextField, PasswordField, validators

#### Logins #####
from flask.ext.login import (
    LoginManager, UserMixin, login_user, logout_user, login_required
    )
        #login_user() takes a user object as arg. 
        #logout_user doesn't require a user object

############################### INITIALIZATION #################################

app = Flask(__name__)
app.config.from_object('config')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/steamscout.db'
db = SQLAlchemy(app)
Bootstrap(app)

################################## LOGINS ######################################

login_manager = LoginManager()
login_manager.init_app(app)

#redirects users to the login view whenever they are required to be logged in.
login_manager.login_view = 'login'

#TO DO:
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))  


################################### MODELS #####################################

# UserMixin contains the properties andmethods required by flask-login 
# for our user object
class User(db.Model, UserMixin): 
    __tablename__= 'user'
    #changed user_id to id

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)  
    email = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(10))
    registered_on = db.Column(db.DateTime)

    def __init__(self,username, email, password):
        self.username = username
        self.email = email
        self.password = password
        
    def __repr__(self):
        return '<name: {}>'.format(self.name)
    
    #Methods included by UserMixin:
    """
    is_authenticated, is_active, is_anonymous, get_id()
    """
    

class Preferences(db.Model): 
    __tablename__= 'preferences'
    preference_id=db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))
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

################################# FORMS ########################################

class LoginForm(Form):
    username = TextField('Username', [validators.Required()])
    password = PasswordField('Password', [validators.Required()])
   #remember_me = BooleanField('remember_me', default=False) 

class SignUpForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=25)])
    email = TextField('email', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
        ])
    confirm = PasswordField('Repeat password')
    
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
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit(): # c9 saying form doesnt have validate_on_submit method
        login_user(user)            
        flash("Logged in successfully!")
        return redirect(url_for('/'))
    return render_template('login.html', form=form)

# @app.before_request
# def before_request():
#     g.user = None
#     if 'user_id' in session:
#         g.user = User.query.get(session['user_id'])

# @app.route('/logout')
# def logout():
#     session.pop('user_id', None)
#     return redirect(oid.get_next_url())

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if request.method == 'GET':
        return render_template('signup.html', form=form)
    
    ### create new user object ### idk if this works:
    if request.method == 'POST' and form.validate():
        user = User(form.username.data,
                    form.email.data,
                    form.password.data)
        db.session.add(user)
        db.session.commit() #not sure if this is necessary?
        flash('Registration successful!')
        return redirect(url_for('login'))
    
    


if __name__ == "__main__":
    # create_app().run(host='0.0.0.0', port=8080, debug=True) # We have to remember to change debug = True back to False if we deply to heruku    
    app.run(host='0.0.0.0', port=8080, debug=False)
    # site url: https://002-pyp-demoday-g1-chanchar.c9.io
    db.create_all()