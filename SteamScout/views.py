from SteamScout import app, db, login_manager, mail
from forms import LoginForm, SignUpForm, AmountPref, PercentPref, GamesSearch
from flask import (
    Flask, request, render_template, redirect, 
    session, json, g, flash, url_for
    )
from models import Games, Preferences, User
from helpers import percent_to_price, format_price, get_price_info
from flask.ext.login import (
    LoginManager, UserMixin, login_user, logout_user, login_required
    )
from flask.ext.mail import Message

@app.route('/mail')
def test_email():
    msg = Message("Hey it's working now",
                sender="steam.scout.15@gmail.com",
                recipients=["steam.scout.15@gmail.com"])
    msg.body = "This is a test email. Check it out in views.py"
    mail.send(msg)
    return "Mail sent!"
    
@login_manager.user_loader
def load_user(id):
    return User.query.get(id)
    
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/games', methods=['GET','POST'])
def games():
    all_games = Games.query.order_by(Games.game_name)
    game_search_form = GamesSearch()
    if request.method == "POST" and game_search_form.validate():
        search_term = game_search_form.search_term.data
        games_found = Games.query.filter(Games.game_name.like("%{}%".format(search_term)))
        found_count = games_found.count()
        game_search_form = GamesSearch() # Re renders search form
        return render_template('games_search.html',game_search_form=game_search_form,
                                                   games_found=games_found,
                                                   found_count=found_count)
    else:
        return render_template('games.html', all_games=all_games,
                                             game_search_form=game_search_form)

@app.route('/games/<game_name>', methods=['GET','POST'])
def game_name(game_name):
    title = game_name
    game = Games.query.filter_by(game_name=game_name).first()
    id_num=game.game_id
    amount_form = AmountPref()
    if 'user_id' in session.keys():
        preference = Preferences.query.filter_by(game_name=game_name, user_id=session['user_id']).first() 
    else:
        preference =  None

    price_info = get_price_info(id_num)
    if price_info != None:
        current_price = format_price(price_info['current_price'])
        initial_price = format_price(price_info['initial_price'])
        discount = price_info['discount_percent']
        header_image = price_info['header_image']
    else:
        current_price, initial_price, discount, header_image = None, None, None, None
    if amount_form.validate_on_submit():
        if preference:
            old_preference = Preferences.query.filter_by(game_name=game_name).first()
            db.session.delete(old_preference)
            db.session.commit()
            
        new_preference = Preferences(session['user_id'],
                           id_num,
                           title,
                           amount_form.threshold_amount.data)
        db.session.add(new_preference)
        db.session.commit()
        return redirect(url_for('settings'))
    
    return render_template('game_page.html', current_price=current_price,
                                             initial_price=initial_price,
                                             discount=discount,
                                             game_title=title,
                                             id_num=id_num,
                                             header_image=header_image,
                                             amount_form=amount_form,
                                             preference=preference)

@app.route('/developers')
def show_developors():
    # page that shows all the games.
    return render_template('developers.html')

@app.route('/contact')
def contact():
    users = User.query.all() 
    preferences = Preferences.query.all()
    return render_template('contact.html', users=users,
                                           preferences=preferences)

@login_required
@app.route('/settings', methods=['GET','POST'])
def settings():
    pref_data= Preferences.query.filter_by(user_id=session['user_id'])
    preferences_count = Preferences.query.filter_by(user_id=session['user_id']).count()
    return render_template('settings.html', pref_data=pref_data,
                                            preferences_count=preferences_count)

@login_required
@app.route('/delete', methods=['POST'])
def delete():
    preference = Preferences.query.filter_by(user_id=session['user_id'], game_name=request.form['delete']).first()
    db.session.delete(preference)
    db.session.commit()
    return redirect(url_for('settings'))

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
        msg = Message("Welcome to SteamScout!", # apprently the header
                sender="steam.scout.15@gmail.com",
                recipients=[form.email.data])
        msg.body = """Hello, welcome to SteamScout. You're just about ready
                    to start tracking all of your favorite games! Your login information
                    is:
                        Username: {}
                        Email: {}
                        Password: {}
                    """.format(form.username.data, form.email.data, form.password.data)
        #Uncomment to have emails sent upon registration     
     #   mail.send(msg)
        return redirect(url_for('login'))
    else:                                                   
        return render_template('signup.html', form=form)