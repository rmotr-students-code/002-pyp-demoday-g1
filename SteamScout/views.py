from flask import (
    request, render_template, redirect,
    session, flash, url_for)
from SteamScout import app, db, login_manager, flask_bcrypt
from SteamScout.forms import LoginForm, SignUpForm, AmountPref, GamesSearch, ContactForm
from SteamScout.models import Games, Preferences, User
from SteamScout.helpers import (
    percent_to_price, format_price, get_price_info,
    generate_email_token, confirm_email_token, send_mail)
from flask.ext.login import login_user, logout_user, login_required
import datetime

@login_manager.user_loader
def load_user(id):
    return User.query.get(id)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/games', methods=['GET', 'POST']) # <int:page>
def games(page=1):
    
    game_search_form = GamesSearch()
    # all_games = Games.query.order_by(Games.game_name).paginate(page, 10, False)

    if request.method == "POST" and game_search_form.validate():
        search_term = game_search_form.search_term.data
        games_found = Games.query.filter(Games.game_name.ilike("%{}%".format(search_term)))
        found_count = games_found.count()
        game_search_form = GamesSearch()
        return render_template(
            'games_search.html', game_search_form=game_search_form,
            games_found=games_found, found_count=found_count)
    else:
        return render_template(
            'games.html', game_search_form=game_search_form)
            # add all_games here if pagination is wanted.

@app.route('/games/<game_name>', methods=['GET', 'POST'])
def game_name(game_name):
    title = game_name
    game = Games.query.filter_by(game_name=game_name).first()

    id_num = game.game_id
    amount_form = AmountPref()
    if 'user_id' in session.keys():
        try:
            preference = Preferences.query.filter_by(
                game_name=game_name, user_id=session['user_id']).first()
            existing_treshold = "{:.2f}".format(preference.threshold_amount)
        except:
            existing_treshold = None
    else:    
        existing_treshold = None

    price_info = get_price_info(id_num)
    if price_info != None:
        current_price = format_price(price_info['current_price'])
        initial_price = format_price(price_info['initial_price'])
        discount = price_info['discount_percent']
        header_image = price_info['header_image']
    else:
        current_price, initial_price, discount, header_image = None, None, None, None
    if amount_form.validate_on_submit():
        user = User.query.filter_by(id=session['user_id']).first()
        if not user.validated:
            flash("You will not receieve any email alerts until you activate your account.", "danger")
        if preference:
            old_preference = Preferences.query.filter_by(
                game_name=game_name).first()
            db.session.delete(old_preference)
            db.session.commit()

        new_preference = Preferences(
            session['user_id'], id_num, title, amount_form.threshold_amount.data)
        db.session.add(new_preference)
        db.session.commit()
        return redirect(url_for('settings'))

    return render_template(
        'game_page.html', current_price=current_price, initial_price=initial_price,
        discount=discount, game_title=title, id_num=id_num, header_image=header_image,
        amount_form=amount_form, preference=existing_treshold)

@app.route('/developers')
def show_developors():
    # page that shows all the games.
    return render_template('developers.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        steam_email = app.config["MAIL_USERNAME"]
        html = render_template(
            "email/contact.html", message=form.message.data)
        subject = form.header.data
        send_mail(steam_email, subject, html, form.email.data, sender=form.email.data)
        flash("Message Sent!", "success")
        return redirect(url_for('games'))
    else:
        return render_template('contact.html', form=form)

@login_required
@app.route('/settings', methods=['GET', 'POST'])
def settings():
    pref_data = Preferences.query.filter_by(user_id=session['user_id'])
    preferences_count = pref_data.count()
    return render_template(
        'settings.html', pref_data=pref_data, preferences_count=preferences_count)

@login_required
@app.route('/delete', methods=['POST'])
def delete():
    preference = Preferences.query.filter_by(
        user_id=session['user_id'], game_name=request.form['delete']).first()
    db.session.delete(preference)
    db.session.commit()
    flash("That scout has been dismissed.", "success")
    return redirect(url_for('settings'))

# Log in / Log out
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data.lower()).first()
        if user is None:
            flash("User not found", "danger")
            return render_template('login.html', form=form)
        if flask_bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            session['logged_in'] = True
            session['username'] = user.username
            session['user_id'] = user.id
            return redirect(url_for('home'))
        else:
            return render_template('login.html', form=form)
    else:
        return render_template('login.html', form=form)

@login_required
@app.route('/logout')
def logout():
    logout_user()
    session.pop('username')
    session.pop('logged_in', None)
    flash("You have successfully logged out", "success")
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm(request.form)
    if request.method == 'POST' and form.validate():
        new_user = User(form.username.data.lower(), form.email.data, form.password.data)
        db.session.add(new_user)
        db.session.commit()

        token = generate_email_token(form.email.data)
        confirmation_url = url_for('.confirm_user', token=token, _external=True)
        html = render_template(
            "email/email_confirmation.html", confirmation_url=confirmation_url)
        subject = "Confirm your email"
        send_mail(new_user.email, subject, html)

        flash('We sent you an email to activate your account!', 'info')
        return redirect(url_for('login'))
    else:
        return render_template('signup.html', form=form)

@app.route('/confirm/<token>')
def confirm_user(token):
    try:
        email = confirm_email_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
    current_user = User.query.filter_by(email=email).first_or_404()
    if current_user.validated:
        flash('Your account has already been validated!', 'info')
    else:
        current_user.validated = True
        current_user.validated_on = datetime.datetime.now()
        db.session.add(current_user)
        db.session.commit()
        flash('You have confirmed your account', 'success')
    return redirect(url_for('login'))
