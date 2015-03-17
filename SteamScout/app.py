from flask import (
    Flask, request, render_template, redirect, 
    session, json, g, flash, url_for
    )
from flask.ext.sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
import requests as r

#### WTForms #####
from flask_wtf import Form
# from flask_wtf import Form, TextField, PasswordField, BooleanField
# from flask_wtf.validators import Required, Length, Email, EqualTo
from wtforms import TextField, PasswordField, BooleanField
from wtforms.validators import Required, Length, Email, EqualTo

#### Logins #####
from flask.ext.login import (
    LoginManager, UserMixin, login_user, logout_user, login_required
    )
        #login_user() takes a user object as arg. 
        #logout_user doesn't require a user object

############################### INITIALIZATION #################################

app = Flask(__name__)
app.config.from_object('config')        #specify your own database root
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////users/alan/desktop/steamscout.db'
db = SQLAlchemy(app)
Bootstrap(app)

#Required for sessions
app.secret_key = 'change_this_later'

################################## LOGINS ######################################

login_manager = LoginManager()
login_manager.init_app(app)

#redirects users to the login view whenever they are required to be logged in.
login_manager.login_view = 'login'

#TO DO:
@login_manager.user_loader
def load_user(id):
    return User.query.get(id)

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
        return '<name: {}>'.format(self.username)
    
    #Methods included by UserMixin:
    """
    is_authenticated, is_active, is_anonymous, get_id
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
        
db.create_all()  # Should we run this each time we run the app?


################################# FORMS ########################################

class LoginForm(Form):
    username = TextField('Username', [Required()])
    password = PasswordField('Password', [Required()])
    remember_me = BooleanField('remember_me', default=False) 

class SignUpForm(Form):
    username = TextField('Enter a Username', validators= [
            Length(min=4, max=25, 
            message=(u'You\'re username must be between 4 and 25 characters')),
            Required("Please enter a username")])
               
    email = TextField('Enter Your Email', validators= [
            Required("Please enter a valid email address"), 
            Email(message=(u'That\'s not a valid email address'))])
            
    password = PasswordField('Enter a Password', validators= [
            Required("Enter a secure password"), 
            EqualTo('confirm', message=(u'Passwords must match'))])
               
    confirm = PasswordField('Please Repeat your Password', validators= [
            Required("Please repeat your password")])
        
    # def validate(self):
    #     # need to roll out our custom validations?
    #     return True
################################# VIEWS ########################################

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/games')
def games():
    # page that shows all the games.
    games_request = r.get('http://api.steampowered.com/ISteamApps/GetAppList/v0001')
    all_games = [game for game in (games_request.json()["applist"]["apps"]["app"])]
    return render_template('games.html', all_games=all_games)

@app.route('/developers')
def show_developors():
    # page that shows all the games.
    return render_template('developers.html')

@app.route('/contact')
def contact():
    users = User.query.all() # This works despite the error? C9Issue? - Martin
    return render_template('contact.html', users=users)

@login_required
@app.route('/settings')
def settings():
    pass

# Log in / Log out
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None:
            return render_template('login.html', form=form)
        if user.password != form.password.data:
            return render_template('login.html', form=form)
        login_user(user)   
        session['logged_in'] = True
        session['username'] = user.username
        return redirect(url_for('home'))
    else:
        return render_template('login.html', form=form)

@login_required
@app.route('/logout')
def logout():
    logout_user()
    session.pop('username')
    session.pop('logged_in', None)
    return redirect(url_for('home'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm(request.form)
    if request.method == 'POST' and form.validate():
        new_user = User(form.username.data,
                         form.email.data,
                         form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful!')
        return redirect(url_for('login'))
    else:                                                   
        return render_template('signup.html', form=form)

    
    


if __name__ == "__main__":
    # create_app().run(host='0.0.0.0', port=8080, debug=True) 
    # We have to remember to change debug = True back to False if we deply to heroku
    app.run(host='0.0.0.0', port=8080, debug=True)
    # site url: https://002-pyp-demoday-g1-chanchar.c9.io
    
    # server error: Port being used ... yada yada
    
    # terminal: "lsof -i :8080" looks for a process that using port 8080.
    #           "kill {process number}", it's usually the first one listing using the second number in the listing. 
    # Rerun the serve to see if it works. 
    
