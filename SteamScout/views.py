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
    msg = Message("Hey it's working now", # apprently the header
                sender="steam.scout.15@gmail.com",
                recipients=["steam.scout.15@gmail.com"]) # send to self for testing
                # sender hopefully will use the default set
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
    # page that shows all the games.
    all_games = Games.query.order_by(Games.game_name)
    game_search_form = GamesSearch()
    if request.method == "POST" and game_search_form.validate(): #validate_on_submit() didn't work?
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
    # percent_form = PercentPref()
    amount_form = AmountPref() 

    price_info = get_price_info(id_num)
    if price_info != None:
        current_price = format_price(price_info['current_price'])
        initial_price = format_price(price_info['initial_price'])
        discount = price_info['discount_percent']
        header_image = price_info['header_image']
    else:
        current_price, initial_price, discount, header_image = None, None, None, None

    # if percent_form.validate_on_submit():
    #     percent = percent_form.threshold_percent.data
    #     final_amt = percent_to_price(percent, initial_price)
    #     #overwrites previous preference data if there is any
    #     if Preferences.query.filter_by(game_name=game_name).first():
    #         old_pref = Preferences.query.filter_by(game_name=game_name).first()
    #         # update function
    #         db.session.delete(old_pref)
    #         db.session.commit()
    #     new_pref = Preferences(session['user_id'],
    #                           id_num,
    #                           game_name,
    #                           final_amt)
    #     db.session.add(new_pref)
    #     db.session.commit()
    #     return redirect(url_for('settings'))

    if amount_form.validate_on_submit():
        #overwrites previous preference data if there is any
        if Preferences.query.filter_by(game_name=game_name).first():
            # change to update()
            old_pref = Preferences.query.filter_by(game_name=game_name).first()
            db.session.delete(old_pref)
            db.session.commit()
            
        new_pref = Preferences(session['user_id'],
                               id_num,
                               title,
                               amount_form.threshold_amount.data)
        db.session.add(new_pref)
        db.session.commit()
        return redirect(url_for('settings'))
    
    return render_template('game_page.html', current_price=current_price,
                                             initial_price=initial_price,
                                             discount=discount,
                                             game_title=title,
                                             id_num=id_num,
                                             header_image=header_image,
                                             # percent_form=percent_form,
                                             amount_form=amount_form)

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



        
