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
from wtforms import (
    TextField, PasswordField, BooleanField, IntegerField, DecimalField,
    RadioField
    )
from wtforms.validators import Required, Length, Email, EqualTo, NumberRange

#### Logins #####
from flask.ext.login import (
    LoginManager, UserMixin, login_user, logout_user, login_required
    )
        #login_user() takes a user object as arg. 
        #logout_user doesn't require a user object
from get_games import get_price_info


############################### INITIALIZATION #################################

app = Flask(__name__)
app.config.from_object('config')        #specify your own database root
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/ubuntu/workspace/SteamScout/steamscout.db'
db = SQLAlchemy(app)
Bootstrap(app)

#Required for sessions
# urlsafe64 needed 
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
    game_name = db.Column(db.String, unique=True)
    threshold_amount=db.Column(db.Float)
    
    def __init__(self, user_id, game_id, game_name, threshold_amount):    
        self.user_id = user_id
        self.game_id = game_id
        self.game_name = game_name
        self.threshold_amount = threshold_amount

class Games(db.Model):
    __tablename__='games'
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, unique=True)
    game_name = db.Column(db.String, unique=True)
    
    def __init__(self, game_id, game_name):
        self.game_id = game_id
        self.game_name = game_name
        
#db.create_all() 

## Populate the Games database:
def fill_game_db():
    """Fills the games table with the id numbers and titles of all the games 
        in the steam library.""" 
    game_list = r.get('http://api.steampowered.com/ISteamApps/GetAppList/v0001')
    for game in game_list.json()['applist']['apps']['app']:
        if Games.query.filter_by(game_name=game['name']).first():
            pass
        else:
            new_game=Games(game['appid'],game['name'])
            db.session.add(new_game)
    db.session.commit()


#fill_game_db()

#Some helpers:
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
     
class PercentPref(Form):
    threshold_percent = IntegerField('percent threshold', validators=[Required("Please enter a number between 1-100"),
                                                                      NumberRange(min=1, max=100)])
class AmountPref(Form):
    threshold_amount = DecimalField('amount threshold', validators=[Required("Please enter an amount between .01 and 1000.00"),
                                                                    NumberRange(min=.01, max=1000.0)])
class GamesSearch(Form):
    search_term = TextField('Enter a Game', validators=[Required("Please enter a game to search for")])

################################# VIEWS ########################################

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/games', methods=['GET','POST'])
def games():
    # page that shows all the games.
    all_games = Games.query.order_by(Games.game_name)
    game_search_form = GamesSearch()
    if request.method == "POST" and game_search_form.validate(): #validate_on_submit() didn't work?
        search_term = game_search_form.search_term.data
        games_found = Games.query.filter(Games.game_name.like("%{}%".format(search_term)))
        game_search_form = GamesSearch() # Re renders search form
        return render_template('games_search.html',game_search_form=game_search_form,
                                                   games_found=games_found)
    else:
        return render_template('games.html', all_games=all_games,
                                             game_search_form=game_search_form)

@app.route('/games/<game_name>', methods=['GET','POST'])
def game_name(game_name):
    title = game_name
    game = Games.query.filter_by(game_name=game_name).first()
    id_num=game.game_id
    percent_form = PercentPref()
    amount_form = AmountPref() 

    price_info = get_price_info(id_num)
    if price_info != None:
        current_price = format_price(price_info['current_price'])
        initial_price = format_price(price_info['initial_price'])
        discount = price_info['discount_percent']
    else:
        current_price, initial_price, discount = None, None, None

    if percent_form.validate_on_submit():
        percent = percent_form.threshold_percent.data
        final_amt = percent_to_price(percent, initial_price)
        #overwrites previous preference data if there is any
        if Preferences.query.filter_by(game_name=game_name).first():
            old_pref = Preferences.query.filter_by(game_name=game_name).first()
            # update function
            db.session.delete(old_pref)
            db.session.commit()
        new_pref = Preferences(session['user_id'],
                               id_num,
                               game_name,
                               final_amt)
        db.session.add(new_pref)
        db.session.commit()
        return redirect(url_for('settings'))

    elif amount_form.validate_on_submit():
        #overwrites previous preference data if there is any
        if Preferences.query.filter_by(game_name=game_name).first():
            old_pref = Preferences.query.filter_by(game_name=game_name).first()
            db.session.delete(old_pref)
            db.session.commit()
        new_pref = Preferences(session['user_id'],
                               id_num,
                               game_name,
                               amount_form.threshold_amount.data)
        db.session.add(new_pref)
        db.session.commit()
        return redirect(url_for('settings'))
    
    return render_template('game_page.html', current_price=current_price,
                                             initial_price=initial_price,
                                             discount=discount,
                                             game_title=title,
                                             id_num=id_num,
                                             percent_form=percent_form,
                                             amount_form=amount_form)


@app.route('/developers')
def show_developors():
    # page that shows all the games.
    return render_template('developers.html')

@app.route('/contact')
def contact():
    users = User.query.all() # This works despite the error? C9Issue? - Martin
    return render_template('contact.html', users=users)

@login_required
@app.route('/settings', methods=['GET','POST'])
def settings():
    pref_data= Preferences.query.filter_by(user_id=session['user_id'])
    return render_template('settings.html', pref_data=pref_data)

# Log in / Log out
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None:
            # flash message
            return render_template('login.html', form=form)
        if user.password != form.password.data:
            return render_template('login.html', form=form)
        login_user(user)   
        session['logged_in'] = True
        session['username'] = user.username
        session['user_id'] = user.id
        #session['preferences'] = Preferences.query.filter_by(user_id=user.id)
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
    app.run(host='0.0.0.0', port=8080, debug=False)
    # site url: https://002-pyp-demoday-g1-chanchar.c9.io
    
    # server error: Port being used ... yada yada
    
    # terminal: "lsof -i :8080" looks for a process that using port 8080.
    #           "kill {process number}", it's usually the first one listing using the second number in the listing. 
    # Rerun the serve to see if it works. 
    
